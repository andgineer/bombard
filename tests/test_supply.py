import unittest
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


class TestHttpRequests(unittest.TestCase):
    def testApplySupply(self):
        self.assertEqual(bombardier.apply_supply_dict(TEST_REQUEST_TEMPLATE, TEST_SUPPLY)['1']['2'], '4')


if __name__ == '__main__':
    unittest.main()