"""
Capture stdout and stderr.

Since Python 3.4 they have (redirect_stdout, redirect_stderr) in contextlib
but my context manager is simpler to use.

Usage:
>>> with CaptureOutput() as captured:
...     print('3', end='')
>>> captured.output
'3'
"""
import sys
from io import StringIO


class CaptureOutput:
    def __init__(self, capture=True):
        """ To see output you can set capture to False"""
        self.capture = capture

    def __enter__(self):
        self.old_out, self.old_err = sys.stdout, sys.stderr
        if self.capture:
            sys.stdout = self.out = StringIO()
            sys.stderr = self.err = StringIO()
        return self

    @property
    def stdout(self):
        if self.capture:
            return self.out.getvalue()
        else:
            return ''

    @property
    def stderr(self):
        if self.capture:
            return self.err.getvalue()
        else:
            return ''

    @property
    def output(self):
        if self.stderr:
            return '\n'.join([self.stdout, self.stderr])
        else:
            return self.stdout

    def __exit__(self, *args):
        if self.capture:
            sys.stdout, sys.stderr = self.old_out, self.old_err
