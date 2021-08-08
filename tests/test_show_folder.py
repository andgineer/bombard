import unittest

from bombard.args import DIR_DESC_FILE_NAME
from bombard.main import campaign
from bombard.show_descr import markdown_for_terminal
from tests.fake_args import FakeArgs
from tests.stdout_capture import CaptureOutput


class TestShowFolder(unittest.TestCase):
    def testShowFolder(self) -> None:
        with CaptureOutput() as captured:
            campaign(FakeArgs(examples=True))

        self.maxDiff = 1024
        with open(f"bombard/examples/{DIR_DESC_FILE_NAME}") as desc:
            self.assertIn(  # do not check 1st line of output with the folder name
                markdown_for_terminal(desc.read()), captured.output
            )
