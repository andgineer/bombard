from tests.stdout_capture import CaptureOutput
import unittest
from bombard.main import campaign
from tests.fake_args import FakeArgs
from bombard.args import INIT_EXAMPLE, DIR_DESC_FILE_NAME, CAMPAIGN_FILE_NAME
import os.path
from bombard.show_descr import markdown_for_terminal


class TestShowFolder(unittest.TestCase):
    def testShowFolder(self):
        with CaptureOutput() as captured:
            campaign(FakeArgs(examples=True))

        self.maxDiff = 1024
        with open(f'bombard/examples/{DIR_DESC_FILE_NAME}') as desc:
            self.assertIn(  # do not check 1st line of output with the folder name
                markdown_for_terminal(desc.read()),
                captured.output
                )
