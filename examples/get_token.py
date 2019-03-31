resp = ammo = {}; reload = lambda *x, **y: x; supply = args = object()  # just to have valid code. this line will be removed before exec
"""
Executed after getToken Bombard request (see bombard.yaml).
Adds to requests list all requests from templates list.
"""
supply.add(token=resp['token'])
for _ in range(args.repeat):
    reload(ammo['projectsList'])
    reload(ammo['usersList'])
