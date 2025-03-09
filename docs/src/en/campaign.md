# Campaign file

All sections are optional.

But you need section `prepare` or `ammo` so Bombard will fire some requests.

Anywhere you can use Python expressions `{}` like

```python
repeat: "{args.repeat * 2}"
```

Command line arguments are available as `args` in these expressions.
All supply variables are available as globals.

## HTTP parameters

All HTTP parameters but URL are optional.

```yaml
url: "{host}auth"  # fully specified URL
method: POST  # by default GET
body:  # below is JSON object for request body
    email: name@example.com
    password: admin
headers:
  json:  # the same as Content-Type: "application/json"
  Authorization: "Bearer {token}"
```

## supply

Variables you use like `{name}` in your requests.
Also you can (re)define this variable using `--supply` like:

```
bombard -s name=value,name2=value2
```

Also you can (re)define it from requests.

If you have `extract` section in a request description, it will
(re)define `supply` variable with the name from this section.

And `script` section in request also can (re)define variables.

## Request description

You use these descriptions in sections `prepare` and `ammo`
described below.

Each request should have `URL` and basically that's it.
If you need to, you can add other elements like that:

```yaml
getToken:  # Name of request by your choice
  repeat: "{args.repeat * 2}"  # default - option --repeat
  url: "{host}auth"  # we use supply.base var
  method: POST  # by default GET
  headers: json  # shortcut for Content-Type: application/json
  body:  # JSON object for the request body
    email: admin@example.com
    password: admin
  extract:  # extract from request result and add to supply
    token:
```

Bombard automatically adds `application/json` to headers if in
the request some JSON body is specified.
If you need another `Content-Type` specification just add it to
`headers` section and it will redefine that default.

### repeat

Override `--repeat` command line option. Number of repetitions
for the request.

### script

In request you can add section `script` with Python3 code.
It runs after request.

It can use `supply` object and fire requests with `reload` function.
Requests definitions from `ammo` section available as `ammo.request_name`.

Response to the request is available in `resp` object.

In example below we fire requests `getPost` from `ammo` section for
1st three posts we get in the response:

```python
for post in resp[:3]:
  reload(ammo.getPost, id=post['id'])
```

Also you can place Python code to separate file and use it like this:

```yaml
script: !include get_token.py
```

If you add this line it mocks all necessary objects and
you can use code autocomplete in your IDE:

```python
from bombard.mock_globals import *; master('path/to/you/yaml')
```

### extract

Instead of script you can use section `extract` in request.
It can contain map of `name: extract` pairs. For each pair
Bombard will (re)define `supply` var with name `name` with
value extracted from the request response as `['extract']`.

```yaml
extract:
    name: extract
    name2: extract2
```

If `extract` is empty Bombard will use the `name`, so
`name:` is the same as `name: name`.

Also you can use any custom indices you want like that

```yaml
extract:
    token: "['data']['JWT']"  # place resp['data']['JWT'] to supply.token
```

so `name: ['name']` is the same as `name:`.

### dry

If you run Bombard with `--dry` it do not make actual HTTP requests.
And if you have `dry` section in request Bombard will use it as
result of this `dry` request.

## prepare

If campaign file has this section, Bombard will start fire with requests
from this section.

Requests in this section can fire requests from `ammo` section, like this:

```yaml
prepare:
  postsList:  # Get ids from posts
    url: "{host}posts"
    script: |
      for post in resp[:3]:  # fire ammo.getPost for 1st three posts in the list
        reload(ammo.getPost, id=post['id'])
```

As you see above you can send some variable not only to global `supply`
but just to the request you fire.

If `prepare` section did not fire any `ammo` requests, Bombard after
`prepare` will fire all requests from `ammo` section.

So, if you have only `extract` sections in `prepare` requests.
Or if `scripts` in `prepare` requests do not call `reload` to fire
requests from `ammo`. Then Bombard will fire all `ammo` requests
after `prepare` requests.

## ammo

If campaign file do not have `prepare` section, Bombard will just fire all
requests from this section.

Each request will be repeated `--repeat` times as defined in command line
(or by default value for this option).

Otherwise bombard will fire `prepare` section and after that if `prepare`
requests did not fire any requests from `ammo`, bombard will fire all
requests from `ammo`.

Example of `ammo` request for the request that you see in `prepare`
section:

```yaml
ammo:
  getPost:
    url: "{host}posts/{id}"  # use {host} from global supply and {id} in local supply just for this request - see script above
```
