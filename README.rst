Bombard
=======

|build_status| |pypi_version| |pypi_license| |readthedocs|

Bombard is a tool for stress test and benchmarking your HTTP server.
Especially it's good to simulate a heavy load and initial burst of
simultaneous HTTP requests with complex logic.

It is designed to be extremely simple yet powerful tool to
load test functional behavior.

Thanks to optional Python inlines you can fast and easy describe
complex logic for the tests.

Test report shows you how many requests per second your server
is capable of serving and with what latency.

Installation
------------

.. code-block:: bash

    pip install bombard --upgrade

After that use ``bombard`` (``bombard.exe`` in Windows) executable:

.. code-block:: bash

    bombard --help

Requests description
--------------------

Requests can be just URL or contain JSON described like this

.. code-block:: yaml

    getToken:
        url: "{base}auth"  # use custom {base} variable to stay DRY
        method: POST
        body:  # below is JSON object for request body
            email: name@example.com
            password: admin
        extract:  # get token for next requests
            token:

In first request you can get security token as in example above.

And use it in next requests:

.. code-block:: yaml

     postsList:
        url: "{host}posts"
        headers:
            Authorization: "Bearer {token}"  # we get {token} in 1st request
        script: |
            for post in resp[:3]:  # for 1st three posts from response
                # schedule getPost request (from ammo section)
                # and provide it with id we got from the response
                reload(ammo.getPost, id=post['id'])

Included examples. To list examples

.. code-block:: bash

    bombard --examples

Command line
------------

From command line you can change number of threads, loop count,
supply vars, customize report and so on.

Also you can bootstrap your own ``bombard.yaml`` file from any example you
like::

    bombard --init --example simple

Report
------

Example of report for the command::

    bombard --example simple --repeat 2 --threshold 100

.. image:: docs/_static/simple_stdout.png

Documentation
-------------
`Bombard documentation <https://bombard.readthedocs.io/en/latest/>`_


.. |build_status| image:: https://travis-ci.org/masterandrey/bombard.png
    :target: https://travis-ci.org/masterandrey/bombard
    :alt: Latest release

.. |pypi_version| image:: https://img.shields.io/pypi/v/bombard.svg?style=flat-square
    :target: https://pypi.org/p/bombard
    :alt: Latest release

.. |pypi_license| image:: https://img.shields.io/pypi/l/bombard.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bombard
    :alt: MIT license

.. |readthedocs| image:: https://readthedocs.org/projects/bombard/badge/?version=latest
    :target: https://bombard.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

