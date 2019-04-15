from tests.stdout_capture import CaptureOutput
import unittest
from bombard.main import campaign
from tests.fake_args import FakeArgs
from bombard.args import INIT_EXAMPLE, DIR_DESC_FILE_NAME, CAMPAIGN_FILE_NAME
import os.path
from bombard.show_descr import markdown_for_terminal


def clean_campaign_file():
    """ Removes default campaign from folder root """
    if os.path.isfile(CAMPAIGN_FILE_NAME):
        os.remove(CAMPAIGN_FILE_NAME)


class TestShowFolder(unittest.TestCase):
    def setUp(self):
        clean_campaign_file()

    def tearDown(self):
        clean_campaign_file()

    def testShowFolder(self):
        with CaptureOutput() as captured:
            campaign(FakeArgs(examples=True))

        self.maxDiff = 1024
        with open(f'bombard/examples/{DIR_DESC_FILE_NAME}') as desc:
            self.assertIn(  # do not check 1st line of output with the folder name
                markdown_for_terminal(desc.read()),
                captured.output + '\n'
                )
