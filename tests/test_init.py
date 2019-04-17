from tests.stdout_capture import CaptureOutput
import unittest
from bombard.main import campaign
from tests.fake_args import FakeArgs
from bombard.args import INIT_EXAMPLE, CAMPAIGN_FILE_NAME
import os.path


def clean_campaign_file():
    """ Removes default campaign from folder root """
    if os.path.isfile(CAMPAIGN_FILE_NAME):
        os.remove(CAMPAIGN_FILE_NAME)


class TestInit(unittest.TestCase):
    def setUp(self):
        clean_campaign_file()

    def tearDown(self):
        clean_campaign_file()

    def testInitDefault(self):
        with CaptureOutput() as captured:
            campaign(FakeArgs(init=True))

        self.maxDiff = 1024
        with open(f'bombard/examples/{INIT_EXAMPLE}') as ex, open(f'{CAMPAIGN_FILE_NAME}', 'r') as init:
            self.assertEqual(
                ex.read(),
                init.read()
                )

    def testInitSimpleton(self):
        with CaptureOutput() as captured:
            campaign(FakeArgs(example='simpleton', init=True))

        self.maxDiff = 1024
        with open(f'bombard/examples/simpleton.yaml') as desc, open(f'{CAMPAIGN_FILE_NAME}', 'r') as init:
            self.assertIn(
                desc.read(),
                init.read()
                )