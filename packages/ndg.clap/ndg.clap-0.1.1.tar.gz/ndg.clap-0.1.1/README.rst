CLAP
====

.. contents:: Table of Contents

Introduction
------------

|PyPI Version|

**CLAP** is the command-line argument parser that builds itself.

It is designed to be easy to use, by building itself based on function
signatures and documentation!

Getting Started
---------------

Requires Python 3.10+ and uses
`NumPy-style docstrings <https://github.com/numpy/numpydoc>`_.

* Available on PyPI as ``ndg.clap``. Install it with PIP.

.. code:: bash

    python -m pip install -U ndg.clap

* All of clap's functionality is available through the ``clap`` module.

.. code:: python

    import clap

Here is a quick example of how to construct a basic parser.

.. code:: python

    class MyCommands(clap.Parser):
        """Represents a collection of commands that the user can execute."""

        def __init__(self) -> None:
            super().__init__(
                help="An example CLI tool created using CLAP.",
                epilog="Thank you for using CLAP!",
            )

        @clap.command()
        def greet(self, name: str, /, nervous: bool = False) -> None:
            """Print a greeting to the specified name.

            Parameters
            ----------
            name : str
                The name of the person to greet.
            nervous : bool, default=False
                Whether to greet the person nervously.
            """
            if nervous is True:
                print(f"Um... hello, {name}...")
            else:
                print(f"Hello, {name}!")


    if __name__ == "__main__":
        parser = MyCommands()
        parser.parse()

.. code:: console

    $ python example.py greet --help
    Prints a greeting to the specified name.
    
    USAGE: greet [OPTIONS] <NAME>
    
    OPTIONS:
      -h, --help   Display this help message and exit. [default: False]
      --nervous  Whether to greet the person nervously. [default: False]
    
    ARGUMENTS:
      name  The name of the person to greet. (required)

    $ python examples/basic.py greet "Gojo Satoru"
    Hello, Gojo Satoru!
    
    $ python examples/basic.py greet --nervous "Gojo Satoru"
    Um... hello, Gojo Satoru...

Additional examples can be found in the ``examples`` directory.

Version Naming
--------------

This library uses semantic versioning::

    MAJOR.MINOR.PATCH

Where an increment in:

* ``MAJOR`` = Incompatible changes (i.e., code may need to be updated).
* ``MINOR`` = Backwards compatible feature changes.
* ``PATCH`` = Backwards compatible bug fixes.

Bug / Feature Request
---------------------

If you find a bug (program failed to run and/or gave undesired results) or you
just want to request a new feature, kindly open a new issue
`here <https://github.com/nicdgonzalez/clap/issues>`_

Contributing
------------

Want to contribute? Great!

Contributions should follow the |Python Style Guide|_.

To fix a bug or enhance an existing module, follow these steps:

* |Fork|_ the repository and create a new branch.

.. code:: console

  $ git clone "git@github.com:{username}/{respository}.git"
  $ cd respository
  $ git checkout -b improve-feature

* Make the appropriate changes and stage the modified files.

.. code:: console

  $ git add <FILES...>

* Commit the changes.

.. code:: console

  $ git commit -m "Improve feature."

* Push to the new branch.

.. code:: console

  $ git push origin improve-feature

* Create a new |Pull Request|_.


.. |PyPI Version| image:: https://badgen.net/pypi/v/ndg.clap
  :target: https://pypi.org/project/ndg.clap

.. |Python Style Guide| replace:: PEP-8 Style Guide for Python Code
.. _Python Style Guide: https://peps.python.org/pep-0008/

.. |Fork| replace:: Fork
.. _Fork: https://github.com/nicdgonzalez/clap/fork

.. |Pull Request| replace:: Pull Request
.. _Pull Request: https://github.com/nicdgonzalez/clap/pulls
