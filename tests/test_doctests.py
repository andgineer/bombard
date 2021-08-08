"""
doctests from all modules of packages listed in PACKAGES
will be added to unit tests suite.

So you will have one nice test report and one test result/exit code in CI.

You should import below all your packages with doctests and list them in PACKAGES.
"""
import doctest
from glob import glob
from importlib import import_module
from os.path import basename, dirname, isfile

import bombard
import tests

PACKAGES = [bombard, tests]

PY_EXT = ".py"


def load_tests(loader, tests, ignore) -> None:
    """
    Unittest hook to add tests to auto-discovered ones
    https://docs.python.org/3/library/unittest.html#load-tests-protocol
    """
    for package in PACKAGES:
        for module_file in glob(dirname(package.__file__) + f"/*{PY_EXT}"):
            if isfile(module_file) and not module_file.endswith("__init__.py"):
                tests.addTest(
                    doctest.DocTestSuite(
                        import_module(f"{package.__name__}.{basename(module_file)[:-len(PY_EXT)]}")
                    )
                )
    return tests
