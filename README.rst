========
datatask
========

General-purpose data structure and representation format for tasks (stand-alone or part of a larger data workflow) that involve multiple data resources.

|pypi| |readthedocs| |travis| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/datatask.svg
   :target: https://badge.fury.io/py/datatask
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/datatask/badge/?version=latest
   :target: https://datatask.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |travis| image:: https://app.travis-ci.com/nthparty/datatask.svg?branch=main
   :target: https://app.travis-ci.com/nthparty/datatask
   :alt: Travis CI build status.

.. |coveralls| image:: https://coveralls.io/repos/github/nthparty/datatask/badge.svg?branch=main
   :target: https://coveralls.io/github/nthparty/datatask?branch=main
   :alt: Coveralls test coverage summary.

Package Installation and Usage
------------------------------
The package is available on `PyPI <https://pypi.org/project/datatask/>`_::

    python -m pip install datatask

The library can be imported in the usual ways::

    import datatask
    from datatask import *

Documentation
-------------
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configuration details)::

    python -m pip install nose coverage
    nosetests --cover-erase

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

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
