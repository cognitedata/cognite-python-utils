Basics
======

Setup
-----

To begin, let's get the code:

.. code:: bash

    $ git clone https://github.com/cognitedata/cognite-python-utils.git
    $ cd cognite-python-utils

The current project uses `poetry <https://python-poetry.org/docs/>`_ to manage
dependencies among different Python packages, which is essential to reproducibility.

First, ensure you are using the right version of Python (``^3.8``). We recommend you
use `pyenv <https://github.com/pyenv/pyenv>`_ to effectively manage multiple versions
of Python installation. You can then install ``poetry``:

.. code:: bash

    $ pip install poetry

Once you clone the current repo into your local machine, you can go inside the repo and run:

.. code:: bash

    $ poetry install

to install the right versions of packages for running scripts in the project repo.

To use the new Python configuration that has been installed, you need to run:

.. code:: bash

    $ poetry shell

which will activate the virtual environment for the project repo.

You can simply type:

.. code:: bash

    $ exit

to exit from the virtual environment and return to the global (or system) Python installation.

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
