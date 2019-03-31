resp = {}; reload = lambda *x, **y: x; supply = args = ammo = object()  # just to have valid code. this line will be removed before exec
"""
Executed after getToken Bombard request (see bombard.yaml).
Get auth token and after that schedule requests.
"""
supply.add(token=resp['token'])
for _ in range(args.repeat):
    reload(ammo['projectsList'])
    reload(ammo['usersList'])
