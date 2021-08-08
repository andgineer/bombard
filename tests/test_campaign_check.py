import logging
import unittest

from bombard.main import start_campaign
from bombard.request_logging import setup_logging
from tests.fake_args import FakeArgs
from tests.stdout_capture import CaptureOutput

EMPTY_BOOK = {}


class TestCampaignCheck(unittest.TestCase):
    def setUp(self) -> None:
        setup_logging(logging.DEBUG)

    def testSimplest(self) -> None:
        with CaptureOutput(capture=True) as captured:
            start_campaign(FakeArgs(example="simplest"), EMPTY_BOOK)
        self.assertIn('You should have at least one of "prepare" and "ammo"', captured.output)
