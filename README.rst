========
datatask
========

General-purpose data structure and representation format for tasks (stand-alone or part of a larger data workflow) that involve multiple data resources.

|pypi|

.. |pypi| image:: https://badge.fury.io/py/datatask.svg
   :target: https://badge.fury.io/py/datatask
   :alt: PyPI version and link.

Package Installation and Usage
------------------------------
The package is available on `PyPI <https://pypi.org/project/datatask/>`_::

    python -m pip install datatask

The library can be imported in the usual ways::

    import datatask
    from datatask import *

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configuration details)::

    python -m pip install nose coverage
    nosetests --cover-erase

Some unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python datatask/datatask.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    python -m pip install pylint
    pylint datatask

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/nthparty/datatask>`_ for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
