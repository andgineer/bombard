bombard your app
================
Bombard is a pure Python application to bombard with
hundreds of HTTP-requests.

This is tool for stress-testing with extremely simple
configuration.

You write requests in simple yaml-file (`bombard campaign book`).
And can include a couple of Python lines in it.

If you need more logic you can include external Python file and debug
it in your IDE.

The simplest (but not very useful) example

.. code-block:: yaml

   ammo:
      postsList:
         url: "https://jsonplaceholder.typicode.com/posts"

More complex example

.. code-block:: yaml

   supply:  # you can redefine it from command line (--supply)
     host: https://jsonplaceholder.typicode.com/
   prepare:
     postsList:
       url: "{host}posts"
       script: |
         for post in resp[:3]:  # add getPost requests for 1st ten posts in the list
           reload(ammo.getPost, id=post['id'])
   ammo:
     getPost:
       url: "{host}posts/{id}"
       headers: json

Example above is included into bombard internal examples that you can use with
option `--example` like that::

    bombard --example simple --repeat 2 --threshold 100

Above we also set repetition number to 2 and threshold to 100ms
so anything equal and above that will be in red.

You will get something like this:

.. image:: _static/simple_stdout.png

Source code: `GitHub <https://github.com/masterandrey/bombard/>`_.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
