"""
Yaml loader extended with loading external files `!include file.ext`
"""
import os.path
import yaml


class Loader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


Loader.add_constructor('!include', Loader.include)


def load(file_name: str) -> dict:
    if not os.path.isfile(file_name):
            print(f'(!) Cannot find file "{file_name}."')
            exit(1)
    return yaml.load(open(file_name, 'r'), Loader)
