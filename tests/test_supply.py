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

TEST_REQUEST_TEMPLATE = {
    '1': {
        '2': '{a}'
    }
}
TEST_SUPPLY = {'a': '4'}


def test_apply_supply():
    assert main.apply_supply(TEST_REQUEST_TEMPLATE, TEST_SUPPLY)['1']['2'] == '4'
