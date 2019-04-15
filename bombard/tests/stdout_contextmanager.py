import sys
from contextlib import contextmanager
from io import StringIO


class CaptureOutput:
    def __enter__(self):
        self.out, self.err = StringIO(), StringIO()
        self.old_out, self.old_err = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self.out, self.err
        return self

    def __exit__(self, *args):
        sys.stdout, sys.stderr = self.old_out, self.old_err
