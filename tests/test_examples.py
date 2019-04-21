import unittest
from bombard import http_request
from bombard.request_logging import setup_logging
import logging
from tests.stdout_capture import CaptureOutput
from tests.fake_args import FakeArgs
from bombard.main import campaign
from tests.fake_jsonplaceholder import FakeJSONPlaceholder


class TestExamples(unittest.TestCase):
    def setUp(self):
        self.fake_server = FakeJSONPlaceholder()
        http_request.http.client.HTTPSConnection.request = self.fake_server.request
        http_request.http.client.HTTPSConnection.getresponse = self.fake_server.response
        setup_logging(logging.DEBUG)

    def testSimplest(self):
        with CaptureOutput(capture=True) as captured:
            campaign(FakeArgs(example='simplest'))
        self.assertIn(
            'GET jsonplaceholder.typicode.com/posts',
            captured.output
        )
        self.assertIn(
            'GET jsonplaceholder.typicode.com/posts/1',
            captured.output
        )
