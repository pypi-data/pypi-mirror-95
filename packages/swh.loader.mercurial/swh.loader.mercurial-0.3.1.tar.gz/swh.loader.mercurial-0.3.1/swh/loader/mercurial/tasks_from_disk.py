# Copyright (C) 2020  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from celery import shared_task

from .from_disk import HgArchiveLoaderFromDisk, HgLoaderFromDisk


@shared_task(name=__name__ + ".LoadMercurialFromDisk")
def load_hg(*, url, directory=None, visit_date=None):
    """Mercurial repository loading

    Import a mercurial tarball into swh.

    Args: see :func:`DepositLoader.load`.

    """
    loader = HgLoaderFromDisk(url, directory=directory, visit_date=visit_date)
    return loader.load()


@shared_task(name=__name__ + ".LoadArchiveMercurialFromDisk")
def load_hg_from_archive(*, url, archive_path=None, visit_date=None):
    """Import a mercurial tarball into swh.

    Args: see :func:`DepositLoader.load`.
    """
    loader = HgArchiveLoaderFromDisk(
        url, archive_path=archive_path, visit_date=visit_date
    )
    return loader.load()
