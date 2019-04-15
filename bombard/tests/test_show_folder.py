from tests.stdout_contextmanager import CaptureOutput
import unittest
from bombard.main import campaign
from tests.fake_args import FakeArgs
from bombard.args import INIT_EXAMPLE, DIR_DESC_FILE_NAME, CAMPAIGN_FILE_NAME
import os.path


class TestShowFolder(unittest.TestCase):
    def setUp(self):
        if os.path.isfile(CAMPAIGN_FILE_NAME):
            os.remove(CAMPAIGN_FILE_NAME)

    def testShowFolder(self):
        with CaptureOutput() as captured:
            campaign(FakeArgs(init=True))
            with open(f'bombard/examples/{DIR_DESC_FILE_NAME}') as desc:
                expected = desc.read()
            self.maxDiff = 1024
            self.assertEqual(
                captured.out.getvalue().strip(),
                expected
            )

