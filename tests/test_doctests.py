import doctest
from bombard import attr_dict, pretty_ns
from tests import stdout_capture, fake_args


def load_tests(loader, tests, ignore):
    tests.addTest(doctest.DocTestSuite(attr_dict))
    tests.addTest(doctest.DocTestSuite(stdout_capture))
    tests.addTest(doctest.DocTestSuite(fake_args))
    tests.addTest(doctest.DocTestSuite(pretty_ns))
    return tests
