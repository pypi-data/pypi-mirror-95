# Copyright (C) 2018-2020  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


def test_loader(
    mocker, swh_config, swh_scheduler_celery_app, swh_scheduler_celery_worker
):
    mock_loader = mocker.patch("swh.loader.mercurial.loader.HgBundle20Loader.load")
    mock_loader.return_value = {"status": "eventful"}

    res = swh_scheduler_celery_app.send_task(
        "swh.loader.mercurial.tasks.LoadMercurial",
        kwargs={"url": "origin_url", "directory": "/some/repo", "visit_date": "now",},
    )

    assert res
    res.wait()
    assert res.successful()

    assert res.result == {"status": "eventful"}
    mock_loader.assert_called_once_with()


def test_archive_loader(
    mocker, swh_config, swh_scheduler_celery_app, swh_scheduler_celery_worker
):
    mock_loader = mocker.patch(
        "swh.loader.mercurial.loader.HgArchiveBundle20Loader.load"
    )
    mock_loader.return_value = {"status": "uneventful"}

    res = swh_scheduler_celery_app.send_task(
        "swh.loader.mercurial.tasks.LoadArchiveMercurial",
        kwargs={
            "url": "another_url",
            "archive_path": "/some/tar.tgz",
            "visit_date": "now",
        },
    )
    assert res
    res.wait()
    assert res.successful()

    assert res.result == {"status": "uneventful"}
    mock_loader.assert_called_once_with()
