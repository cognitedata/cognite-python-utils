Getting Started
===============

Installation
------------

To install this package, run:

.. code:: bash

    $ pip install cognite-utils

Or, if using `poetry <https://python-poetry.org/docs/>`_, run:

.. code:: bash

    $ poetry add cognite-utils

The following shows how you can load functionalities in the package:

.. code:: python

    >>> from cognite.utils.contextualization import EntityMatchCategorizer
    >>> from cognite.utils.infrastructure import ProjectArchiver
