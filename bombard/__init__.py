__version__ = '1.8.1'


def version():
    return '.'.join(__version__.split('.')[:2])


if __name__ == '__main__':
    print(version())