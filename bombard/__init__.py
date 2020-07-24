import bombard.version


__version__ = bombard.version.VERSION


def version():
    """ 'major.minor' without build number """
    return '.'.join(__version__.split('.')[:2])


if __name__ == '__main__':
    print(version())
