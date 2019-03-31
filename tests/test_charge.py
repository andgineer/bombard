from unittest.mock import MagicMock
from importlib.machinery import SourceFileLoader
from src import main
from src import bombardier
# bombard = SourceFileLoader('bombard', 'bombard').load_module()


TEST_REQUEST = {
    'url': 'https://localhost/users',
    'method': 'GET',
    'headers': {'x-x': 'json'}
}


def test_make_request():
    bombardier.http.client.HTTPSConnection.request = MagicMock()
    bombardier.http.client.HTTPSConnection.getresponse = MagicMock()
    bombardier.make_request(TEST_REQUEST)
    bombardier.http.client.HTTPSConnection.request.assert_called_once_with(
        'GET', '/users', body=None, headers={'x-x': 'json'}
    )
    bombardier.http.client.HTTPSConnection.getresponse.assert_called_once()

