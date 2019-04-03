import unittest
from unittest.mock import MagicMock
from bombard import bombardier


TEST_REQUEST = {
    'url': 'https://localhost/users',
    'method': 'GET',
    'headers': {'x-x': 'json'}
}


class FakeArgs:
    threads = 1
    timeout = 3


class TestHttpRequests(unittest.TestCase):
    def setUp(self):
        bombardier.http.client.HTTPSConnection.request = MagicMock()
        bombardier.http.client.HTTPSConnection.getresponse = MagicMock()

    def testRequest(self):
        bombardier.Bombardier(args=FakeArgs()).make_request(**TEST_REQUEST)
        bombardier.http.client.HTTPSConnection.request.assert_called_once_with(
            'GET', '/users', body=None, headers={'x-x': 'json'}
        )
        bombardier.http.client.HTTPSConnection.getresponse.assert_called_once()


if __name__ == '__main__':
    unittest.main()
