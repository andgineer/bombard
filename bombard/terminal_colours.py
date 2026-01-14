"""
Colourize text in terminal
source https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

You can use it function style
>>> green('Hello!')
'\\x1b[1;32mHello!\\x1b[0m'

Or include style
>>> f'{YELLOW}Hello{OFF}, {RED}world{OFF}!'
'\\x1b[1;33mHello\\x1b[0m, \\x1b[1;31mworld\\x1b[0m!'

Under the hood this is colorama.
But I keep my wrapper in this module as legacy.
"""

from colorama.ansi import CSI, AnsiFore, AnsiStyle

GREEN = f"{CSI}{AnsiStyle.BRIGHT};{AnsiFore.GREEN}m"
RED = f"{CSI}{AnsiStyle.BRIGHT};{AnsiFore.RED}m"
DARK_RED = f"{CSI}{AnsiStyle.DIM};{AnsiFore.RED}m"
GRAY = f"{CSI}{AnsiStyle.BRIGHT};{AnsiFore.BLACK}m"
BROWN = f"{CSI}{AnsiStyle.DIM};{AnsiFore.YELLOW}m"
YELLOW = f"{CSI}{AnsiStyle.BRIGHT};{AnsiFore.YELLOW}m"

OFF = f"{CSI}{AnsiStyle.RESET_ALL}m"


def paint_it(msg: str, colour: str) -> str:
    return f"{colour}{msg}{OFF}"


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

    fail, total = doctest.testmod(report=True)
    if not fail:
        print(f"... {total} test(s) passed")
