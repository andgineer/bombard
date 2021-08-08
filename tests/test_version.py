import unittest

import bombard
from bombard.main import campaign
from tests.fake_args import FakeArgs
from tests.stdout_capture import CaptureOutput


class TestVersion(unittest.TestCase):
    def testVersion(self) -> None:
        with CaptureOutput() as captured:
            campaign(FakeArgs(version=True))

        with open("bombard/LICENSE.txt") as license:
            self.assertIn(license.readline(), captured.output)
        self.assertIn(bombard.version(), captured.output)
