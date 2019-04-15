"""
If you use include files for scripts add into them

    from bombard.mock_globals import *; mock(<your yaml>)

That defines globals so you have valid code and code autocomplete in your IDE editor.
All strings with `bombard.examples.mock_globals` will be automatically removed before running bombard scripts.
"""
from bombard.campaign_yaml import yaml
from bombard.expand_file_name import expand_relative_file_name
import os.path  # we use it to simplify import lines in examples


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


def master(yaml_file_name: str):
    """
    Add names from the yaml file to the unit globals.
    That makes code autocomplete work in bombard script.
    """
    try:
        campaign_book = yaml.load(open(expand_relative_file_name(yaml_file_name), 'r'))
        for name in campaign_book['ammo']:
            setattr(ammo, name, None)
        for name in campaign_book['supply']:
            setattr(supply, name, None)
    except Exception:
        pass  # ignore if the file is not completed at the moment
    args.file_name = None
    args.repeat = None
    args.verbose = None
    args.log = None
    args.ms = None
    args.threshold = None
