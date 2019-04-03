"""
Colourizes text in terminal output
"""

COLOURS = {
    'green': '\033[1;32;40m',
    'red': '\033[1;31;40m',
    'dark_red': '\033[0;31;40m',
    'gray': '\033[1;30;40m',
    'brown': '\033[0;33;40m',
    'yellow': '\033[1;33;40m',
}

OFF = '\033[0;37;40m'

def colour_it(msg: str, colour: str) -> str:
    return f'{COLOURS[colour]}{msg}{OFF}'

def green(s: str) -> str:
    return colour_it(s, 'green')


def red(s: str) -> str:
    return colour_it(s, 'red')


def dark_red(s: str) -> str:
    return colour_it(s, 'dark_red')


def gray(s: str) -> str:
    return colour_it(s, 'gray')


def brown(s: str) -> str:
    return colour_it(s, 'brown')


def yellow(s: str) -> str:
    return colour_it(s, 'yellow')

