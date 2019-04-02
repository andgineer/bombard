from bombard import bombardier


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
    assert bombardier.apply_supply(TEST_REQUEST_TEMPLATE, TEST_SUPPLY)['1']['2'] == '4'
