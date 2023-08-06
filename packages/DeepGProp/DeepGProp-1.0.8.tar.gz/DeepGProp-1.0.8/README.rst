

*DeepGProp*
=================================

   Neural Networks optimization with Genetic Algorithms

Based on the BSc thesis by

-  **Author: Luis Liñán Villafranca**
-  **Mentor: Juan Julián Merelo Guervós**

----

.. contents:: **Table of contents**
   :depth: 2

----

Installation
------------

The first prerequisite is to have `Python 3.6, 3.7 or 3.8
<https://www.python.org/downloads/>`_ and pip_ installed on the system. It is
recommended to create a virtual environment to isolate the used package
versions. For more information about pip_ and venv_ check the `official tutorial
<https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`_.

If you are using `pyenv`, remember to compile your version with the
`--enable-shared` configuration option:

First, you need to install a version of python that’s been compiled with
``-fPIC``. ``pyenv`` versions by default are not, so you will need to
issue something like this:

.. code:: shell

   env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.6



Virtual environment creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can use a core module to create the virtual environment, it’s
been working since version 3.3

.. code:: shell

   python -m venv .venv

..

Please make sure when you do this that all ``__pycache__``
directories have been deleted; otherwise, it might fail in some
unexpected place.

This will create a virtual environment in the ``.venv`` directory. Once
that’s been done, we need to activate it; use one of the following
commands (depending on the interpreter) (obtained from the official
venv_ documentation):

+--------+---------------+---------------------------------------+
|Platform|Shell          |Command to activate virtual environment|
+========+===============+=======================================+
|POSIX   |bash/zsh       |``$ source <venv>/bin/activate``       |
|        +---------------+---------------------------------------+
|        |fish           |``$ . <venv>/bin/activate.fish``       |
|        +---------------+---------------------------------------+
|        |csh/tcsh       |``$ source <venv>/bin/activate.csh``   |
|        +---------------+---------------------------------------+
|        |PowerShell Core|``$ <venv>/bin/Activate.ps1``          |
+--------+---------------+---------------------------------------+
|Windows |cmd.exe        |``C:\> <venv>\Scripts\activate.bat``   |
|        +---------------+---------------------------------------+
|        |PowerShell     |``PS C:\> <venv>\Scripts\Activate.ps1``|
+--------+---------------+---------------------------------------+

Table 1.1: *Activating the virtual environment.*

You won’t need to create the virtual environment in the case you’re
using global installation of modules via version managers such as
``pyenv``.

Installing the DeepGProp CLI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run DeepGProp first we need to install its cli. You can install it
with ``pip``:

.. code:: shell

   pip install -U DeepGProp

Or downloading the repository with:

.. code:: shell

   pip install .

On the other hand, if we want the code to be updated as we change it, we
will need to install DeepGProp in editable mode. To do this, we need to
add the option ``-e/--editable`` to the installation command:

.. code:: shell

   pip install -e .

All the available options can be listed using:

.. code:: shell

   dgp --help

Extra modules
~~~~~~~~~~~~~

I’ve divided all the used packages in different groups to avoid
installing undesirable ones for specific use of the repository:

+---------+-------------------------+--------------------------------------------------------------------------------------------------+
| Purpose | File path               | Description                                                                                      |
+=========+=========================+==================================================================================================+
| Test    | requirements/tests.txt  | Necessary packages for tests. Nox_ installs them automaticly when running the tests.             |
+---------+-------------------------+--------------------------------------------------------------------------------------------------+
| Lint    | requirements/lint.txt   | Necessary packages for linting. Nox_ installs them automaticly when linting the code.            |
+---------+-------------------------+--------------------------------------------------------------------------------------------------+
| Format  | requirements/format.txt | Necessary packages for formatting. Nox_ installs them automaticly when running format command.   |
+---------+-------------------------+--------------------------------------------------------------------------------------------------+
| Dev     | requirements/dev.txt    | All above packages.                                                                              |
+---------+-------------------------+--------------------------------------------------------------------------------------------------+


To install any of these packages you can run:

.. code:: shell

   pip install -r <file path>

If you are not using any virtual environment, make sure you install
these packages so that they are available in the required Python
version.

Tutorials
---------

* `Runing DGP on the MNIST dataset <docs/using_mnist_dataset.rst>`_

Tests and formatting
--------------------

.. note:: To be able to run the DeepGProp tests, you will need to
   install it in editable mode. checkout in `Installing the DeepGProp
   CLI <#installing-the-deepgprop-cli>`_ section how to do it.

First, we need to install the Nox_ tool:

.. code:: shell

   pip install -U nox

To run all the tests:

.. code:: shell

   nox -k test

To run the linters:

.. code:: shell

   nox -k lint

You can check all the possible sessions with the following command:

.. code:: shell

   nox -l

Frameworks
----------

-  `Keras <https://keras.io/>`_ - base library to create and run the
   neural networks.

-  `DEAP <https://deap.readthedocs.io/en/master/>`_ - genetic
   algorithms library used to optimize the models hyper parametters.

Utilities
---------

-  Automation:

   -  Nox_ - automation tool to
      run different tasks as the tests or the code formatting check.

-  Tests:

   -  `pytest <https://docs.pytest.org/en/latest/>`_ - Python test
      framework to run the tests.

Datasets
--------

All datasets need to have a first row with the column names, and one of the
columns needs to be named `class`. For the time being, it's prepared to run only
classification problems.

Licence
-------

The original code can be found in the `DeepGProp
<https://github.com/lulivi/dgp-lib>`_ repo under GPLv3 License.

.. _pip: https://pypi.org/project/pip/
.. _Nox: https://nox.thea.codes/en/stable
.. _venv: https://docs.python.org/3/library/venv.html