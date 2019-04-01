"""
If you use include files for scripts add into them

    from bombard.examples.mock_globals import *; mock(<your yaml>)

That defines globals so you have valid code and code autocomplete in your IDE editor.
All strings with `bombard.examples.mock_globals` will be automatically removed before running bombard scripts.
"""
from src.yaml_includes import yaml
import os.path  # we use it to simplify import lines in examples


SIGNATURE = 'bombard.examples.mock_globals'

resp = {}

def reload(requests, repeat=None, **kwargs):
    pass


class _Supply(dict):
    pass


class _Args:
    pass


class _Ammo(dict):
    pass


ammo = _Ammo()
supply = _Supply()
args = _Args()


def mock(yaml_file_name: str):
    """
    Add names from the yaml file to the unit globals.
    To make code autocomplete to work in bombard script.
    """
    campaign_book = yaml.load(open(yaml_file_name, 'r'))
    for name in campaign_book['ammo']:
        setattr(ammo, name, None)
    for name in campaign_book['supply']:
        setattr(supply, name, None)
    args.file_name = None
    args.repeat = None
    args.verbose = None
    args.log = None
    args.ms = None
    args.threshold = None
