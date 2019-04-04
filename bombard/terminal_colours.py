"""
Colourize text in terminal
source https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

You can use it function style
green('Hello!')

Or include style
f'{YELLOW}Hello{OFF}, {RED}world{OFF}!'
"""

GREEN = '\033[1;32;40m'
RED = '\033[1;31;40m'
DARK_RED = '\033[0;31;40m'
GRAY = '\033[1;30;40m'
BROWN = '\033[0;33;40m'
YELLOW = '\033[1;33;40m'

OFF = '\033[0m'


def paint_it(msg: str, colour: str) -> str:
    return f'{colour}{msg}{OFF}'


def green(s: str) -> str:
    return paint_it(s, GREEN)


def red(s: str) -> str:
    return paint_it(s, RED)


def dark_red(s: str) -> str:
    return paint_it(s, DARK_RED)


def gray(s: str) -> str:
    return paint_it(s, GRAY)


def brown(s: str) -> str:
    return paint_it(s, BROWN)


def yellow(s: str) -> str:
    return paint_it(s, YELLOW)


if __name__ == "__main__":
    import doctest
    doctest.testmod()