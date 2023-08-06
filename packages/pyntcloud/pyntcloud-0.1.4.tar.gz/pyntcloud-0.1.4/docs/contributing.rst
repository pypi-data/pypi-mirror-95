.. _contributing:

============
Contributing
============

At the very least, you need a Python(>3.5) installation (an isolated environment, i.e conda, is recommended) and the following requirements:

- numpy
- numba
- scipy
- pandas
- flake8
- pytest

Then you can clone the repo and install it in editable mode:

.. code-block:: bash

    git clone https://github.com/daavoo/pyntcloud.git
    pip install -e pyntcloud

From the root of the repo, you can run:

.. code-block:: bash

    # for getting warnings about syntax and other kinds of errors
    flake8

    # for running all the tests
    pytest -v
