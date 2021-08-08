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

from colorama.ansi import AnsiFore, AnsiStyle, code_to_chars

GREEN = code_to_chars(f"{AnsiStyle.BRIGHT};{AnsiFore.GREEN}")
RED = code_to_chars(f"{AnsiStyle.BRIGHT};{AnsiFore.RED}")
DARK_RED = code_to_chars(f"{AnsiStyle.DIM};{AnsiFore.RED}")
GRAY = code_to_chars(f"{AnsiStyle.BRIGHT};{AnsiFore.BLACK}")
BROWN = code_to_chars(f"{AnsiStyle.DIM};{AnsiFore.YELLOW}")
YELLOW = code_to_chars(f"{AnsiStyle.BRIGHT};{AnsiFore.YELLOW}")

OFF = code_to_chars(AnsiStyle.RESET_ALL)


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
