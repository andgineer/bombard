from unittest.mock import MagicMock
from importlib.machinery import SourceFileLoader


bombard = SourceFileLoader('bombard', 'bombard').load_module()


TEST_REQUEST = {
    'url': 'https://localhost/users',
    'method': 'GET',
    'headers': {'x-x': 'json'}
}

TEST_REQUEST_TEMPLATE = {
    '1': {
        '2': '{a}'
    }
}
TEST_CONTEXT = {'a': '4'}


def test_make_request():
    bombard.http.client.HTTPSConnection.request = MagicMock()
    bombard.http.client.HTTPSConnection.getresponse = MagicMock()
    bombard.make_request(TEST_REQUEST)
    bombard.http.client.HTTPSConnection.request.assert_called_once_with('GET', '/users', body=None, headers={'x-x': 'json'})
    bombard.http.client.HTTPSConnection.getresponse.assert_called_once()


def test_apply_context():
    assert bombard.apply_context(TEST_REQUEST_TEMPLATE, TEST_CONTEXT)['1']['2'] == '4'
