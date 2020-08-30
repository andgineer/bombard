import unittest
from bombard.request_logging import setup_logging
import logging
from tests.stdout_capture import CaptureOutput
from tests.fake_args import FakeArgs
from bombard.main import start_campaign


EMPTY_BOOK = {}


class TestCampaignCheck(unittest.TestCase):
    def setUp(self):
        setup_logging(logging.DEBUG)

    def testSimplest(self):
        with CaptureOutput(capture=True) as captured:
            start_campaign(FakeArgs(example='simplest'), EMPTY_BOOK)
        self.assertIn(
            'You should have at least one of "prepare" and "ammo"',
            captured.output
        )

