Development
===========

All development is currently done against Python 3.5 (the latest available in
Ubuntu 16.04), and all CI tests are ran against version 2.7, 3.5, and 3.6.

Bootstrapping
------------
Bootstrapping your development environment is easy! Once you set up whatever
virtualenv or container or VM that you want to do development in, there's one
command to run:

::

    make develop


This will install all of the pip requirements in ``requirements.dev.txt`` and
install Posty into your environment in 'editable mode'. Editable mode means
that Posty will be installed into your env as if it were any other package, but
any changes you make to the source code will be instantly reflected in the CLI
binary.


Testing
-------
To run the test suite, simply run ``make test``. This will run:

#. ``pycodestyle`` (formerly ``pep8``)
#. ``flake8``
#. ``pytest``
