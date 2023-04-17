import os.path
import unittest

from bombard.args import CAMPAIGN_FILE_NAME, INIT_EXAMPLE
from bombard.main import campaign
from tests.fake_args import FakeArgs
from tests.stdout_capture import CaptureOutput


def clean_campaign_file() -> None:
    """Removes default campaign from folder root"""
    if os.path.isfile(CAMPAIGN_FILE_NAME):
        os.remove(CAMPAIGN_FILE_NAME)


class TestInit(unittest.TestCase):
    def setUp(self) -> None:
        clean_campaign_file()

    def tearDown(self) -> None:
        clean_campaign_file()

    def testInitDefault(self) -> None:
        with CaptureOutput():
            campaign(FakeArgs(init=True))

        self.maxDiff = 1024
        with open(f"bombard/examples/{INIT_EXAMPLE}", encoding="utf8") as ex, open(
            f"{CAMPAIGN_FILE_NAME}", "r", encoding="utf8"
        ) as init:
            self.assertEqual(ex.read(), init.read())

    def testInitSimpleton(self) -> None:
        with CaptureOutput():
            campaign(FakeArgs(example="simpleton", init=True))

        self.maxDiff = 1024
        with open("bombard/examples/simpleton.yaml", encoding="utf8") as desc, open(
            f"{CAMPAIGN_FILE_NAME}", "r", encoding="utf8"
        ) as init:
            self.assertIn(desc.read(), init.read())
