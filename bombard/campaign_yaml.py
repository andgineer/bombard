"""
Bombard campaign loader.

Extends yaml loader with loading external files `!include file.ext`.
Excludes lines that import mock_globals.
"""
import os.path
import yaml as original_yaml
import io


SIGNATURE = 'bombard.mock_globals'


class Yaml:
    @staticmethod
    def load(*args, **kwargs):
        """
        Mimics yaml interface for seamless injection
        """
        return original_yaml.load(*args, **kwargs, Loader=IncludesLoader)

    @staticmethod
    def full_load(*args, **kwargs):
        """
        Mimics yaml interface for seamless injection
        """
        return original_yaml.load(*args, **kwargs, Loader=IncludesLoader)


yaml = Yaml()


class IncludesLoader(original_yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(IncludesLoader, self).__init__(stream)

    @staticmethod
    def wrap_in_yaml_document(msg: str) ->str:
        """
        Converts multi-line msg to yaml document that we can insert into yaml
        """
        result = []
        for line in msg.split('\n'):
            if SIGNATURE not in line:  # skip line that mocks globals
                result.append(' '*4 + line)
        return '|\n' + '\n'.join(result)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            wrapped = io.StringIO(self.wrap_in_yaml_document(f.read()))
            wrapped.name = f.name  # to please owe own __init__
            return original_yaml.load(wrapped, IncludesLoader)


IncludesLoader.add_constructor('!include', IncludesLoader.include)

