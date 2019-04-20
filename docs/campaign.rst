Campaign file
=============
All sections are optional.

But you need section ``prepare`` or ``ammo`` so Bombard will
fire some requests.

supply
------

Variables you use like ``{name}`` in your requests.
Also you can (re)define this variable using ``--supply`` like::

    bombard -s name=value,name2=value2

Also you can (re)define it from requests.

If you have ``extract`` section in a request description, it will
(re)define ``supply`` variable with the name from this section.

And ``script`` section in request also can (re)define variables.

Request description
-------------------

You use this descriptions in sections ``prepare`` and ``ammo``
described below.

Each request should have ``URL`` and basically that's it.
If you need to, you can add other elements like that:

.. code-block:: yaml

  getToken:  # Name of request by your choice
    url: "{base}auth"  # we use supply.base var
    method: POST  # by default GET
    body:  # JSON object for the request body
      email: admin@example.com
      password: admin
    extract:  # extract from request result and add to supply
      token:

script
______

In request you can add section ``script`` with Python3 code.
It runs after request.

It can use ``supply`` object and fire requests with ``reload`` function.
Requests definitions from ``ammo`` section available as ``ammo.request_name``.

Response to the request is available in ``resp`` object.

In example below we fire requests ``getPost`` from ``ammo`` section for
1st three posts we get in the response:

.. code-block:: python

      for post in resp[:3]:
        reload(ammo.getPost, id=post['id'])

Also you can place Python code to separate file and use it like this:

.. code-block:: yaml

    script: !include get_token.py

If you add this line it mocks all necessary objects and
you can use code autocomplete in your IDE:

.. code-block:: python

    from bombard.mock_globals import *; master('path/to/you/yaml')



extract
_______

Instead of script you can use section ``extract`` in request.
It can contain map of ``name: extract`` pairs. For each pair
Bombard will (re)define ``supply`` var with name ``name`` with
value extracted from the request response as ``['extract']``.

.. code-block:: yaml

    extract:
        name: extract
        name2: extract2

If ``extract`` is empty Bombard will use the ``name``, so
``name:`` is the same as ``name: name``.

Also you can use any custom indices you want like that

.. code-block:: yaml

    extract:
        token: "['data']['JWT']"  # place resp['data']['JWT'] to supply.token

so ``name: ['name']`` is the same as ``name:``.

prepare
-------

If campaign file has this section, Bombard will fire only requests from
this section.

Each request will be repeated ``--repeat`` times as defined in command line
(or by default value for this option).

And scripts in this section are responsible to fire scripts from ``ammo``
section, like this

.. code-block:: yaml

    prepare:
      postsList:  # Get ids from posts
        url: "{host}posts"
        script: |
          for post in resp[:3]:  # fire ammo.getPost for 1st three posts in the list
            reload(ammo.getPost, id=post['id'])

As you see above you can send some variable not only to global ``supply``
but just to the request you fire.

ammo
----

If campaign file do not have ``prepare`` section, Bombard will fire all requests
from this section.

Each request will be repeated ``--repeat`` times as defined in command line
(or by default value for this option).

Otherwise this requests should be fired from requests from ``prepare`` section
as described above.

Example of ``ammo`` request for the request that you see in ``prepare``
section:

.. code-block:: yaml

    ammo:
      getPost:
        url: "{host}posts/{id}"  # use {host} from global supply and {id} in local supply just for this request - see script above
