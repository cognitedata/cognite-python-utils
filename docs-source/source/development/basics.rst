Basics
======

To begin, let's get the code:

.. code:: bash

    $ git clone https://github.com/cognitedata/cognite-python-utils.git
    $ cd cognite-python-utils

Managing Dependencies
---------------------

The current project uses `poetry <https://python-poetry.org/docs/>`_ to manage
dependencies among different Python packages, which is essential to reproducibility.

First, ensure you are using the right version of Python (``^3.8``). We recommend you
use `pyenv <https://github.com/pyenv/pyenv>`_ to effectively manage multiple versions
of Python installation. You can then install ``poetry``:

.. code:: bash

    $ pip install poetry

Once you clone the project repo, go to its root and run:

.. code:: bash

    $ poetry install

to install correct dependencies for the project.

To activate the virtual environment, run:

.. code:: bash

    $ poetry shell

To add a new dependency, run:

.. code:: bash

    $ poetry add <new-package-name>

Finally, you can type:

.. code:: bash

    $ exit

to exit from the virtual environment.

Running Pre-Commit Hooks
------------------------

Consistent coding standards enable effective code review and maintenance. Hence, we strongly recommend
you use pre-commit hooks set for the project. You can install them by running:

.. code:: bash

    $ pre-commit install

Then, whenever you are about to make a new commit, run:

.. code:: bash

    $ pre-commit run --all-files

to automatically apply coding standards set for the project.

Updating Project Documentation
------------------------------

The current project's documentation is generated using `Sphinx <https://www.sphinx-doc.org/en/master/>`_
and hosted on `GitHub Pages <https://pages.github.com/>`_.
To update it, make changes in ``docs-source`` directory and run:

.. code:: bash

    $ cd docs-source
    $ make clean
    $ make html
    $ cp -r ./build/html/* ../docs

which will update build artifacts used by GitHub Pages.

.. warning::
    When adding demo ``Jupyter`` notebooks, please ensure that the outputs do not include
    any confidential information such as customer identity. To this aim, we recommend you use
    fictitious data for running your notebooks. If you have no choice but use customer data
    to run the notebooks, please ensure to redact/replace any confidential information from outputs.
