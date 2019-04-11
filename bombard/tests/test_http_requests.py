import unittest
from unittest.mock import MagicMock
from bombard import bombardier
from bombard import http_request
from bombard.main import setup_logging
import logging


TEST_AMMO = {
    'request': {
        'url': 'https://localhost/users',
        'method': 'GET',
        'headers': {'x-x': 'json'}
    },
    'id': 1,
    'name': 'request',
    'supply': {},
}


class FakeArgs:
    threads = 1
    timeout = 3
    ms = False
    threshold = 1000
    quiet = False
    dry = False


class TestHttpRequests(unittest.TestCase):
    def setUp(self):
        http_request.http.client.HTTPSConnection.request = MagicMock()
        http_request.http.client.HTTPSConnection.getresponse = MagicMock()
        setup_logging(logging.DEBUG)

    def testRequest(self):
        bombardier.Bombardier(args=FakeArgs()).worker(1, TEST_AMMO)
        http_request.http.client.HTTPSConnection.request.assert_called_once_with(
            'GET', '/users', body=None, headers={'x-x': 'json'}
        )
        http_request.http.client.HTTPSConnection.getresponse.assert_called_once()


if __name__ == '__main__':
    unittest.main()
