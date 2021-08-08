import logging
import unittest
from unittest.mock import MagicMock

from bombard import bombardier, http_request
from bombard.main import setup_logging
from tests.fake_args import FakeArgs

TEST_AMMO = {
    "request": {"url": "https://localhost/users", "method": "GET", "headers": {"x-x": "json"}},
    "id": 1,
    "name": "request",
    "supply": {},
}


class TestHttpRequests(unittest.TestCase):
    def setUp(self) -> None:
        http_request.http.client.HTTPSConnection.request = MagicMock()
        http_request.http.client.HTTPSConnection.getresponse = MagicMock()
        setup_logging(logging.DEBUG)

    def testRequest(self) -> None:
        bombardier.Bombardier(args=FakeArgs()).worker(1, TEST_AMMO)
        http_request.http.client.HTTPSConnection.request.assert_called_once_with(
            "GET", "/users", body=None, headers={"x-x": "json"}
        )
        http_request.http.client.HTTPSConnection.getresponse.assert_called_once()


if __name__ == "__main__":
    unittest.main()
