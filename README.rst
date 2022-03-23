========
datatask
========

General-purpose data structure and representation format for tasks (stand-alone or part of a larger data workflow) that involve multiple data resources.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/datatask.svg
   :target: https://badge.fury.io/py/datatask
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/datatask/badge/?version=latest
   :target: https://datatask.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/nthparty/datatask/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/nthparty/datatask/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/nthparty/datatask/badge.svg?branch=main
   :target: https://coveralls.io/github/nthparty/datatask?branch=main
   :alt: Coveralls test coverage summary.

Purpose
-------
This library provides a data structure and format for representing individual tasks or steps (within a larger data workflow) that involve one or more resources containing tabular data. Data resource paths and URIs can be associated with more concise resource names (called *references*), and these references can then be used to specify task inputs and outputs (including their schemas). This library is *not* intended to act or to be used as a query language, though a collection of individual tasks may constitute (or may be included within) a larger query or data workflow graph.

Package Installation and Usage
------------------------------
The package is available on `PyPI <https://pypi.org/project/datatask/>`_::

    python -m pip install datatask

The library can be imported in the usual ways::

    import datatask
    from datatask import *

Examples
^^^^^^^^
This library makes it possible to define the input and output data resources involved in a data task::

    >>> from datatask import datatask
    >>> dt = datatask({"inputs": ["transactions.csv"], "outputs": ["report.csv"]})

The ``datatask`` class is derived from ``dict``, making conversion to JSON straightforward (using either the built-in `json <https://docs.python.org/3/library/json.html>`_ library or the wrapper methods presented below)::

    >>> dt.to_json()
    '{"inputs": ["transactions.csv"], "outputs": ["report.csv"]}'
    >>> datatask.from_json(
    ...     '{"inputs": ["transactions.csv"], "outputs": ["report.csv"]}'
    ... )
    {'inputs': ['transactions.csv'], 'outputs': ['report.csv']}

Typically, a data resource is a string consisting of a file path or a URI::

    >>> dt = datatask({
    ...    "inputs": [
    ...        "https://example.com/inventory.csv",
    ...        "https://example.com/transactions.csv"
    ...    ],
    ...    "outputs": [
    ...        "/home/user/report.csv"
    ...    ]
    ... })

It is also possible to specify concise names, or **references**, for data resources. These references can then be used to specify input and output data resources::

    >>> dt = datatask({
    ...    "resources": {
    ...        "inv": "https://example.com/inventory.csv",
    ...        "rep": "/home/user/report.csv"
    ...    },
    ...    "inputs": ["inv"],
    ...    "outputs": ["rep"]
    ... })

Each output data resource can be associated with its schema (which must be a list of dictionaries). In the example below, the task indicates that the output data resource's schema has two columns (the first and second columns found in the ``inv`` input data resource)::

    >>> dt = datatask({
    ...    "resources": {
    ...        "inv": "https://example.com/inventory.csv",
    ...        "rep": "/home/user/report.csv"
    ...    },
    ...    "inputs": ["inv"],
    ...    "outputs": {"rep": [{"inv": 0}, {"inv": 1}]}
    ... })

It is also possible to specify the schema (an ordered list of column names) of an input data resource, and then to reference individual columns in the input data resource using that schema::

    >>> dt = datatask({
    ...    "resources": {
    ...        "inv": "https://example.com/data.csv",
    ...        "rep": "/home/user/report.csv"
    ...    },
    ...    "inputs": {"inv": ["item", "quantity", "price"]},
    ...    "outputs": {"rep": [{"inv": "item"}, {"inv": "quantity"}]}
    ... })

Within both ``inputs`` and ``outputs`` entries, each reference can be associated with a **specification** rather than a schema. This specification can optionally contain the schema. The below instance is semantically equivalent to the example immediately above::

    >>> dt = datatask({
    ...    "inputs": {
    ...        "https://example.com/inventory.csv": {
    ...            "schema": ["item", "quantity", "price"]
    ...        }
    ...    },
    ...    "outputs": {
    ...        "/home/user/report.csv": {
    ...            "schema": [
    ...                {"https://example.com/inventory.csv": "item"},
    ...                {"https://example.com/inventory.csv": "quantity"}
    ...            ]
    ...        }
    ...    }
    ... })

A specification can also optionally contain a ``header`` attribute associated with a boolean value. This can be used to indicate whether a data resource has a header row. If a ``header`` attribute is not present, it is by default assumed that the data resource has no header row::

    >>> dt = datatask({
    ...    "inputs": {
    ...        "https://example.com/inventory.csv": {
    ...            "schema": ["item", "quantity", "price"],
    ...            "header": True
    ...        }
    ...    },
    ...    "outputs": {
    ...        "/home/user/report.csv": {
    ...            "schema": [
    ...                {"https://example.com/inventory.csv": "item"},
    ...                {"https://example.com/inventory.csv": "quantity"}
    ...            ],
    ...            "header": False
    ...        }
    ...    }
    ... })

Recommendations
^^^^^^^^^^^^^^^
This subsection presents recommended patterns for a few common task types. These recommendations are not enforced by the library.

Especially in larger instances or in instances that may be automatically processed (*e.g.*, to perform expansion of references into their corresponding data resource paths or URIs), it may be useful to explicitly distinguish reference strings using a special character::

    >>> dt = datatask({
    ...    "resources": {
    ...        "@inv": "https://example.com/inventory.csv",
    ...        "@rep": "/home/user/report.csv"
    ...    },
    ...    "inputs": {"@inv": ["item", "quantity", "price"]},
    ...    "outputs": {"@rep": [{"@inv": "item"}, {"@inv": "quantity"}]}
    ... })

To specify the column names within an output schema, nested dictionaries of the form ``{"column_name": ... }`` can be used::

    >>> dt = datatask({
    ...    "resources": {
    ...        "@inv": "https://example.com/data.csv",
    ...        "@rep": "/home/user/report.csv"
    ...    },
    ...    "inputs": {"@inv": ["item", "quantity", "price"]},
    ...    "outputs": {
    ...        "@rep": {
    ...            "schema": [
    ...                {"product": {"@inv": "item"}},
    ...                {"remaining": {"@inv": "quantity"}}
    ...            ],
    ...            "header": True
    ...        }
    ...    }
    ... })

To indicate that the values of a particular column in an output schema are computed by applying an operator to one or more column values from an input data resource, nested dictionaries of the form ``{"$operation_name": ... }`` can be used::

    >>> dt = datatask({
    ...    "resources": {
    ...        "@inv": "https://example.com/data.csv",
    ...        "@rep": "/home/user/report.csv"
    ...    },
    ...    "inputs": {"@inv": ["item", "quantity", "price"]},
    ...    "outputs": {
    ...        "@rep": {
    ...            "schema": [
    ...                {"item": {"@inv": "item"}},
    ...                {"cost": {"$mul": [{"@inv": "quantity"}, {"@inv": "price"}]}},
    ...            ],
    ...            "header": True
    ...        }
    ...    }
    ... })

Documentation
-------------
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org/>`_ (see ``setup.cfg`` for configuration details)::

    python -m pip install pytest pytest-cov
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python datatask/datatask.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    python -m pip install pylint
    python -m pylint datatask

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/nthparty/datatask>`_ for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.

Publishing
----------
This library can be published as a `package on PyPI <https://pypi.org/project/datatask/>`_ by a package maintainer. Install the `wheel <https://pypi.org/project/wheel/>`_ package, remove any old build/distribution files, and package the source into a distribution archive::

    python -m pip install wheel
    rm -rf dist *.egg-info
    python setup.py sdist bdist_wheel

Next, install the `twine <https://pypi.org/project/twine/>`_ package and upload the package distribution archive to PyPI::

    python -m pip install twine
    python -m twine upload dist/*
