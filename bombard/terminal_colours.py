"""
Colourizes text in terminal output
"""


def green(s: str) -> str:
    return f'\033[1;32;40m{s}\033[0;37;40m'


def red(s: str) -> str:
    return f'\033[1;31;40m{s}\033[0;37;40m'


def dark_red(s: str) -> str:
    return f'\033[0;31;40m{s}\033[0;37;40m'
