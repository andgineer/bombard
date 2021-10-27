"""
Capture stdout and stderr.

Since Python 3.4 we have redirect_std* in contextlib.
But I still prefer my context manager as simpler to use.

Usage:
>>> with CaptureOutput() as captured:
...     print('3', end='')
>>> captured.output
'3'

>>> with CaptureOutput(capture=False) as captured:
...     captured.output is None
True
"""
import sys
from io import StringIO
from typing import Optional


class CaptureOutput:
    def __init__(self, capture=True) -> None:
        """ To see output you can set capture to False"""
        self.capture = capture

    def __enter__(self) -> "CaptureOutput":
        self.old_out, self.old_err = sys.stdout, sys.stderr
        if self.capture:
            sys.stdout = self.out = StringIO()
            sys.stderr = self.err = StringIO()
        return self

    @property
    def stdout(self) -> Optional[str]:
        if self.capture and self.out.getvalue():
            return self.out.getvalue()
        return None

    @property
    def stderr(self) -> Optional[str]:
        if self.capture and self.err.getvalue():
            return self.err.getvalue()
        return None

    @property
    def output(self) -> Optional[str]:
        """ stdout and strerr separated by new line """
        if self.stdout is not None:
            if self.stderr is not None:
                return "\n".join([self.stdout, self.stderr])
            return self.stdout
        return self.stderr

    def __exit__(self, *args) -> None:
        if self.capture:
            sys.stdout, sys.stderr = self.old_out, self.old_err


if __name__ == "__main__":
    import doctest

    doctest.testmod()
