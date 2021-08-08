import unittest

from bombard.report import Reporter


class TestInit(unittest.TestCase):
    def setUp(self) -> None:
        self.reporter = Reporter()

    def testZeroTime(self) -> None:
        """
        zero time => infinity numbers
        """
        report = self.reporter.report()
        self.assertIn("\u221E", report)  # utf8 infinity char ∞
