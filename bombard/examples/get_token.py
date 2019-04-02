"""
Executed after getToken Bombard request (see bombard.yaml).
Get auth token and after that schedule requests.
"""
from bombard.mock_globals import *; master('bombard.yaml')
# to have code autocomplete to work. lines with `bombard.examples.mock_globals` (including this one) will be removed before execution


supply(token=resp['token'])
for _ in range(args.repeat):
    reload(ammo.projectsList)
    reload(ammo.usersList)
