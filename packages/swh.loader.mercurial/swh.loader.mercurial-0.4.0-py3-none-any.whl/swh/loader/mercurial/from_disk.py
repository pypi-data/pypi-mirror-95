# Copyright (C) 2020-2021  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from collections import deque
from datetime import datetime
import os
from shutil import rmtree
from tempfile import mkdtemp
from typing import Deque, Dict, Optional, Tuple, TypeVar, Union

from swh.loader.core.loader import BaseLoader
from swh.loader.core.utils import clean_dangling_folders
from swh.loader.mercurial.utils import parse_visit_date
from swh.model.from_disk import Content, DentryPerms, Directory
from swh.model.hashutil import MultiHash, hash_to_bytehex
from swh.model.model import (
    ObjectType,
    Origin,
    Person,
    Release,
    Revision,
    RevisionType,
    Sha1Git,
    Snapshot,
    SnapshotBranch,
    TargetType,
    TimestampWithTimezone,
)
from swh.model.model import Content as ModelContent
from swh.storage.interface import StorageInterface

from . import hgutil
from .archive_extract import tmp_extract
from .hgutil import HgNodeId

FLAG_PERMS = {
    b"l": DentryPerms.symlink,
    b"x": DentryPerms.executable_content,
    b"": DentryPerms.content,
}  # type: Dict[bytes, DentryPerms]

TEMPORARY_DIR_PREFIX_PATTERN = "swh.loader.mercurial.from_disk"


T = TypeVar("T")


class HgDirectory(Directory):
    """A more practical directory.

    - creates missing parent directories
    - removes empty directories
    """

    def __setitem__(self, path: bytes, value: Union[Content, "HgDirectory"]) -> None:
        if b"/" in path:
            head, tail = path.split(b"/", 1)

            directory = self.get(head)
            if directory is None or isinstance(directory, Content):
                directory = HgDirectory()
                self[head] = directory

            directory[tail] = value
        else:
            super().__setitem__(path, value)

    def __delitem__(self, path: bytes) -> None:
        super().__delitem__(path)

        while b"/" in path:  # remove empty parent directories
            path = path.rsplit(b"/", 1)[0]
            if len(self[path]) == 0:
                super().__delitem__(path)
            else:
                break

    def get(
        self, path: bytes, default: Optional[T] = None
    ) -> Optional[Union[Content, "HgDirectory", T]]:
        # TODO move to swh.model.from_disk.Directory
        try:
            return self[path]
        except KeyError:
            return default


class HgLoaderFromDisk(BaseLoader):
    """Load a mercurial repository from a local repository."""

    CONFIG_BASE_FILENAME = "loader/mercurial"

    visit_type = "hg"

    def __init__(
        self,
        storage: StorageInterface,
        url: str,
        directory: Optional[str] = None,
        logging_class: str = "swh.loader.mercurial.LoaderFromDisk",
        visit_date: Optional[datetime] = None,
        temp_directory: str = "/tmp",
        clone_timeout_seconds: int = 7200,
        content_cache_size: int = 10_000,
        max_content_size: Optional[int] = None,
    ):
        """Initialize the loader.

        Args:
            url: url of the repository.
            directory: directory of the local repository.
            logging_class: class of the loader logger.
            visit_date: visit date of the repository
            config: loader configuration
        """
        super().__init__(
            storage=storage,
            logging_class=logging_class,
            max_content_size=max_content_size,
        )

        self._temp_directory = temp_directory
        self._clone_timeout = clone_timeout_seconds

        self.origin_url = url
        self.visit_date = visit_date
        self.directory = directory

        self._repo: Optional[hgutil.Repository] = None
        self._revision_nodeid_to_swhid: Dict[HgNodeId, Sha1Git] = {}
        self._repo_directory: Optional[str] = None

        # keeps the last processed hg nodeid
        # it is used for differential tree update by store_directories
        # NULLID is the parent of the first revision
        self._last_hg_nodeid = hgutil.NULLID

        # keeps the last revision tree
        # it is used for differential tree update by store_directories
        self._last_root = HgDirectory()

        # Cache the content hash across revisions to avoid recalculation.
        self._content_hash_cache: hgutil.LRUCacheDict = hgutil.LRUCacheDict(
            content_cache_size,
        )

    def pre_cleanup(self) -> None:
        """As a first step, will try and check for dangling data to cleanup.
        This should do its best to avoid raising issues.

        """
        clean_dangling_folders(
            self._temp_directory,
            pattern_check=TEMPORARY_DIR_PREFIX_PATTERN,
            log=self.log,
        )

    def cleanup(self) -> None:
        """Last step executed by the loader."""
        if self._repo_directory and os.path.exists(self._repo_directory):
            self.log.debug(f"Cleanup up repository {self._repo_directory}")
            rmtree(self._repo_directory)

    def prepare_origin_visit(self) -> None:
        """First step executed by the loader to prepare origin and visit
        references. Set/update self.origin, and
        optionally self.origin_url, self.visit_date.

        """
        self.origin = Origin(url=self.origin_url)

    def prepare(self) -> None:
        """Second step executed by the loader to prepare some state needed by
        the loader.

        """

    def fetch_data(self) -> bool:
        """Fetch the data from the source the loader is currently loading

        Returns:
            a value that is interpreted as a boolean. If True, fetch_data needs
            to be called again to complete loading.

        """
        if not self.directory:  # no local repository
            self._repo_directory = mkdtemp(
                prefix=TEMPORARY_DIR_PREFIX_PATTERN,
                suffix=f"-{os.getpid()}",
                dir=self._temp_directory,
            )
            self.log.debug(
                f"Cloning {self.origin_url} to {self.directory} "
                f"with timeout {self._clone_timeout} seconds"
            )
            hgutil.clone(self.origin_url, self._repo_directory, self._clone_timeout)
        else:  # existing local repository
            # Allow to load on disk repository without cloning
            # for testing purpose.
            self._repo_directory = self.directory

        self._repo = hgutil.repository(self._repo_directory)

        return False

    def store_data(self):
        """Store fetched data in the database."""
        for rev in self._repo:
            self.store_revision(self._repo[rev])

        branch_by_hg_nodeid: Dict[HgNodeId, bytes] = {
            hg_nodeid: name for name, hg_nodeid in hgutil.branches(self._repo).items()
        }
        tags_by_name: Dict[bytes, HgNodeId] = self._repo.tags()
        tags_by_hg_nodeid: Dict[HgNodeId, bytes] = {
            hg_nodeid: name for name, hg_nodeid in tags_by_name.items()
        }

        snapshot_branches: Dict[bytes, SnapshotBranch] = {}

        for hg_nodeid, revision_swhid in self._revision_nodeid_to_swhid.items():
            tag_name = tags_by_hg_nodeid.get(hg_nodeid)

            # tip is listed in the tags by the mercurial api
            # but its not a tag defined by the user in `.hgtags`
            if tag_name and tag_name != b"tip":
                snapshot_branches[tag_name] = SnapshotBranch(
                    target=self.store_release(tag_name, revision_swhid),
                    target_type=TargetType.RELEASE,
                )

            if hg_nodeid in branch_by_hg_nodeid:
                name = branch_by_hg_nodeid[hg_nodeid]
                snapshot_branches[name] = SnapshotBranch(
                    target=revision_swhid, target_type=TargetType.REVISION,
                )

            # The tip is mapped to `HEAD` to match
            # the historical implementation
            if hg_nodeid == tags_by_name[b"tip"]:
                snapshot_branches[b"HEAD"] = SnapshotBranch(
                    target=name, target_type=TargetType.ALIAS,
                )

        snapshot = Snapshot(branches=snapshot_branches)
        self.storage.snapshot_add([snapshot])

        self.flush()
        self.loaded_snapshot_id = snapshot.id

    def get_revision_id_from_hg_nodeid(self, hg_nodeid: HgNodeId) -> Sha1Git:
        """Return the swhid of a revision given its hg nodeid.

        Args:
            hg_nodeid: the hg nodeid of the revision.

        Returns:
            the swhid of the revision.
        """
        return self._revision_nodeid_to_swhid[hg_nodeid]

    def get_revision_parents(self, rev_ctx: hgutil.BaseContext) -> Tuple[Sha1Git, ...]:
        """Return the swhids of the parent revisions.

        Args:
            hg_nodeid: the hg nodeid of the revision.

        Returns:
            the swhids of the parent revisions.
        """
        parents = []
        for parent_ctx in rev_ctx.parents():
            parent_hg_nodeid = parent_ctx.node()
            # nullid is the value of a parent that does not exist
            if parent_hg_nodeid == hgutil.NULLID:
                continue
            parents.append(self.get_revision_id_from_hg_nodeid(parent_hg_nodeid))

        return tuple(parents)

    def store_revision(self, rev_ctx: hgutil.BaseContext) -> None:
        """Store a revision given its hg nodeid.

        Args:
            rev_ctx: the he revision context.

        Returns:
            the swhid of the stored revision.
        """
        hg_nodeid = rev_ctx.node()

        root_swhid = self.store_directories(rev_ctx)

        # `Person.from_fullname` is compatible with mercurial's freeform author
        # as fullname is what is used in revision hash when available.
        author = Person.from_fullname(rev_ctx.user())

        (timestamp, offset) = rev_ctx.date()

        # TimestampWithTimezone.from_dict will change name
        # as it accept more than just dicts
        rev_date = TimestampWithTimezone.from_dict(int(timestamp))

        extra_headers = [
            (b"time_offset_seconds", str(offset).encode(),),
        ]
        for key, value in rev_ctx.extra().items():
            # The default branch is skipped to match
            # the historical implementation
            if key == b"branch" and value == b"default":
                continue

            # transplant_source is converted to match
            # the historical implementation
            if key == b"transplant_source":
                value = hash_to_bytehex(value)
            extra_headers.append((key, value))

        revision = Revision(
            author=author,
            date=rev_date,
            committer=author,
            committer_date=rev_date,
            type=RevisionType.MERCURIAL,
            directory=root_swhid,
            message=rev_ctx.description(),
            metadata={"node": hg_nodeid.hex()},
            extra_headers=tuple(extra_headers),
            synthetic=False,
            parents=self.get_revision_parents(rev_ctx),
        )

        self._revision_nodeid_to_swhid[hg_nodeid] = revision.id
        self.storage.revision_add([revision])

    def store_release(self, name: bytes, target=Sha1Git) -> Sha1Git:
        """Store a release given its name and its target.

        A release correspond to a user defined tag in mercurial.
        The mercurial api as a `tip` tag that must be ignored.

        Args:
            name: name of the release.
            target: swhid of the target revision.

        Returns:
            the swhid of the stored release.
        """
        release = Release(
            name=name,
            target=target,
            target_type=ObjectType.REVISION,
            message=None,
            metadata=None,
            synthetic=False,
            author=Person(name=None, email=None, fullname=b""),
            date=None,
        )

        self.storage.release_add([release])

        return release.id

    def store_content(self, rev_ctx: hgutil.BaseContext, file_path: bytes) -> Content:
        """Store a revision content hg nodeid and file path.

        Content is a mix of file content at a given revision
        and its permissions found in the changeset's manifest.

        Args:
            rev_ctx: the he revision context.
            file_path: the hg path of the content.

        Returns:
            the swhid of the top level directory.
        """
        hg_nodeid = rev_ctx.node()
        file_ctx = rev_ctx[file_path]

        file_nodeid = file_ctx.filenode()
        perms = FLAG_PERMS[file_ctx.flags()]

        # Key is file_nodeid + perms because permissions does not participate
        # in content hash in hg while it is the case in swh.
        cache_key = (file_nodeid, perms)

        sha1_git = self._content_hash_cache.get(cache_key)
        if sha1_git is not None:
            return Content({"sha1_git": sha1_git, "perms": perms})

        data = file_ctx.data()

        content_data = MultiHash.from_data(data).digest()
        content_data["length"] = len(data)
        content_data["perms"] = perms
        content_data["data"] = data
        content_data["status"] = "visible"
        content = Content(content_data)

        model = content.to_model()
        if isinstance(model, ModelContent):
            self.storage.content_add([model])
        else:
            raise ValueError(
                f"{file_path!r} at rev {hg_nodeid.hex()!r} "
                "produced {type(model)!r} instead of {ModelContent!r}"
            )

        self._content_hash_cache[cache_key] = content.hash

        # Here we make sure to return only necessary data.
        return Content({"sha1_git": content.hash, "perms": perms})

    def store_directories(self, rev_ctx: hgutil.BaseContext) -> Sha1Git:
        """Store a revision directories given its hg nodeid.

        Mercurial as no directory as in git. A Git like tree must be build
        from file paths to obtain each directory hash.

        Args:
            rev_ctx: the he revision context.

        Returns:
            the swhid of the top level directory.
        """
        repo: hgutil.Repository = self._repo  # mypy can't infer that repo is not None
        prev_ctx = repo[self._last_hg_nodeid]

        # TODO maybe do diff on parents
        status = prev_ctx.status(rev_ctx)

        for file_path in status.removed:
            del self._last_root[file_path]

        for file_path in status.added:
            content = self.store_content(rev_ctx, file_path)
            self._last_root[file_path] = content

        for file_path in status.modified:
            content = self.store_content(rev_ctx, file_path)
            self._last_root[file_path] = content

        self._last_hg_nodeid = rev_ctx.node()

        directories: Deque[Directory] = deque([self._last_root])
        while directories:
            directory = directories.pop()
            self.storage.directory_add([directory.to_model()])
            directories.extend(
                [item for item in directory.values() if isinstance(item, Directory)]
            )

        return self._last_root.hash


class HgArchiveLoaderFromDisk(HgLoaderFromDisk):
    """Mercurial loader for repository wrapped within tarballs."""

    def __init__(
        self,
        storage: StorageInterface,
        url: str,
        visit_date: Optional[datetime] = None,
        archive_path: str = None,
        temp_directory: str = "/tmp",
        max_content_size: Optional[int] = None,
    ):
        super().__init__(
            storage=storage,
            url=url,
            visit_date=visit_date,
            logging_class="swh.loader.mercurial.ArchiveLoaderFromDisk",
            temp_directory=temp_directory,
            max_content_size=max_content_size,
        )
        self.archive_extract_temp_dir = None
        self.archive_path = archive_path

    def prepare(self):
        """Extract the archive instead of cloning."""
        self.archive_extract_temp_dir = tmp_extract(
            archive=self.archive_path,
            dir=self._temp_directory,
            prefix=TEMPORARY_DIR_PREFIX_PATTERN,
            suffix=f".dump-{os.getpid()}",
            log=self.log,
            source=self.origin_url,
        )

        repo_name = os.listdir(self.temp_dir)[0]
        self.directory = os.path.join(self.archive_extract_temp_dir, repo_name)
        super().prepare()


# Allow direct usage of the loader from the command line with
# `python -m swh.loader.mercurial.from_disk $ORIGIN_URL`
if __name__ == "__main__":
    import logging

    import click

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(process)d %(message)s"
    )

    @click.command()
    @click.option("--origin-url", help="origin url")
    @click.option("--hg-directory", help="Path to mercurial repository to load")
    @click.option("--visit-date", default=None, help="Visit date")
    def main(origin_url, hg_directory, visit_date):
        from swh.storage import get_storage

        storage = get_storage(cls="memory")
        return HgLoaderFromDisk(
            storage,
            origin_url,
            directory=hg_directory,
            visit_date=parse_visit_date(visit_date),
        ).load()

    main()
