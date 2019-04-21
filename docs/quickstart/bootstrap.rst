Bootstrapping
-------------

To create template yaml file you place your requests in use command ``--init``.
By default it copy example ``easy.yaml`` into the current folder, with the name
``bomard.yaml``.

.. code-block:: bash

    bombard --init

So now command ``bombard`` will use this file. And you can edit it so it will
bombard your API.

If you want to use another example as base just add ``--example <name>`` with the
example name you want.

.. code-block:: bash

    bombard --init --example simple

To list all available examples you can use ``--examples`` like that

.. code-block:: bash

    bombard --examples