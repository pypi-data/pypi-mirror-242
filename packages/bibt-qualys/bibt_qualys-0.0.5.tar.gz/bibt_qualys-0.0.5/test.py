import os
import json
from bibt.qualys import Client


# def test_client(capsys):
#     with capsys.disabled():
#         c = Client(
#             os.environ["QUALYS_USER"],
#             os.environ["QUALYS_PASS"],
#             os.environ["QUALYS_URL"],
#         )
#         assert c.session
#         c.close()
#         assert not c.session


# def test_list_scan_schedules(capsys):
#     with capsys.disabled():
#         c = Client(
#             os.environ["QUALYS_USER"],
#             os.environ["QUALYS_PASS"],
#             os.environ["QUALYS_URL"],
#         )
#         scans = c.list_scan_schedules()
#         assert len(scans) > 0


# def test_list_scans(capsys):
#     with capsys.disabled():
#         c = Client(
#             os.environ["QUALYS_USER"],
#             os.environ["QUALYS_PASS"],
#             os.environ["QUALYS_URL"],
#         )
#         scans = c.list_scans()
#         assert len(scans) > 0


def test_get_scan_result(capsys):
    with capsys.disabled():
        c = Client(
            os.environ["QUALYS_USER"],
            os.environ["QUALYS_PASS"],
            os.environ["QUALYS_URL"],
        )
        scan = c.get_scan_result(os.environ["TEST_SCAN_TITLE"])
        with open("test.json", "w+") as outfile:
            json.dump(scan, outfile, indent=2)
