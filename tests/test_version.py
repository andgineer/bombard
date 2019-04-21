from tests.stdout_capture import CaptureOutput
import unittest
from bombard.main import campaign
from tests.fake_args import FakeArgs
import bombard


class TestVersion(unittest.TestCase):
    def testVersion(self):
        with CaptureOutput() as captured:
            campaign(FakeArgs(version=True))

        with open(f'bombard/LICENSE.txt') as license:
            self.assertIn(
                license.readline(),
                captured.output
                )
        self.assertIn(
            bombard.version(),
            captured.output
            )
