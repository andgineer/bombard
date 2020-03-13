import colorama


colorama.init()  # On Windows will filter ANSI escape sequences out of any text sent to 
# stdout or stderr, and replace them with equivalent Win32 calls.

__version__ = '1.20.1'


def version():
    """ 'major.minor' without build number """
    return '.'.join(__version__.split('.')[:2])


if __name__ == '__main__':
    print(version())
