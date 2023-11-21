import os

from bibt.qualys import Client


def test_client():
    c = Client(
        os.environ["QUALYS_USER"], os.environ["QUALYS_PASS"], os.environ["QUALYS_URL"]
    )
    assert c.session
    c.close()
    assert not c.session


def test_list_scan_schedules():
    c = Client(
        os.environ["QUALYS_USER"], os.environ["QUALYS_PASS"], os.environ["QUALYS_URL"]
    )
    scans = c.list_scan_schedules()
    for scan in scans:
        print(scan)

    assert len(scans) > 0
