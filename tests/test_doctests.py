"""
Add doctests to unittests suite, so you have one nice reports and one test result (exit code).

To add doctests you should import all packages with doctests and list them in doctest_packages
"""
import doctest
from os.path import dirname, basename, isfile
from glob import glob
from importlib import import_module
import tests
import bombard

doctests_packages = [bombard, tests]

PY_EXT = '.py'


def load_tests(loader, tests, ignore):
    """
    Unittest hook to add tests to auto-discovered ones
    https://docs.python.org/3/library/unittest.html#load-tests-protocol
    """
    for package in doctests_packages:
        for module_file in glob(dirname(package.__file__) + f'/*{PY_EXT}'):
            if isfile(module_file) and not module_file.endswith('__init__.py'):
                tests.addTest(doctest.DocTestSuite(
                    import_module(f'{package.__name__}.{basename(module_file)[:-len(PY_EXT)]}')
                ))
    return tests
