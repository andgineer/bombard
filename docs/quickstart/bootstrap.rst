Bootstrapping
-------------

To create your own ``bomard.yaml`` use command ``--init``.
By default it copy example ``easy.yaml``

.. code-block:: bash

    bombard --init

So now command ``bombard`` will use this local ``bomard.yaml``.
Edit it to adapt to your server.

If you want to use another example as base just add ``--example <name>``
with the example name you want:

.. code-block:: bash

    bombard --init --example simple

To list all available examples use ``--examples`` like that:

.. code-block:: bash

    bombard --examples
