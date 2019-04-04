Bombard
=======

|build_status| |pypi_version| |pypi_license|

Bombards target server with simultaneous requests 
to reveal any problems under the stress.

Requests can contain JSON described in yaml file.

You can get security token before bombarding and use the token in requests.

Please see ``examples/`` it's pretty straightforward and is commented.

You can change number of threads, requests file name and vars from command
line (see ``--help``).


.. |build_status| image:: https://travis-ci.org/masterandrey/bombard.png
    :target: https://travis-ci.org/masterandrey/bombard
    :alt: Latest release

.. |pypi_version| image:: https://img.shields.io/pypi/v/bombard.svg?style=flat-square
    :target: https://pypi.org/p/bombard
    :alt: Latest release

.. |pypi_license| image:: https://img.shields.io/pypi/l/bombard.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bombard
    :alt: MIT license

