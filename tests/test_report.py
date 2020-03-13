from tests.stdout_capture import CaptureOutput
import unittest
from bombard.report import Reporter


class TestInit(unittest.TestCase):
    def setUp(self):
        self.reporter = Reporter(
            )

    def testZeroTime(self):
        """
        zero time => infinity numbers
        """
        report = self.reporter.report()
        self.assertIn(  
                '\u221E',  # utf8 infinity char ∞
                report
                )
