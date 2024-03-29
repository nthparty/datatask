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

Installation and Usage
----------------------
This library is available as a `package on PyPI <https://pypi.org/project/datatask>`__::

    python -m pip install datatask

The library can be imported in the usual ways::

    import datatask
    from datatask import *

Examples
^^^^^^^^
This library makes it possible to define the input and output data resources involved in a data task::

    >>> from datatask import datatask
    >>> dt = datatask({"inputs": ["transactions.csv"], "outputs": ["report.csv"]})

.. |datatask| replace:: ``datatask``
.. _datatask: https://datatask.readthedocs.io/en/0.3.0/_source/datatask.html#datatask.datatask.datatask

.. |dict| replace:: ``dict``
.. _dict: https://docs.python.org/3/library/stdtypes.html#dict

The |datatask|_ class is derived from |dict|_, making conversion to JSON straightforward (using either the built-in `json <https://docs.python.org/3/library/json.html>`__ library or the wrapper methods presented below)::

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

Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The ``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__::

    python -m pip install .[docs,lint]

Documentation
^^^^^^^^^^^^^
The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__::

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see the ``pyproject.toml`` file for configuration details)::

    python -m pip install .[test]
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__::

    python src/datatask/datatask.py -v

Style conventions are enforced using `Pylint <https://pylint.pycqa.org>`__::

    python -m pip install .[lint]
    python -m pylint src/datatask

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/nthparty/datatask>`__ for this library.

Versioning
^^^^^^^^^^
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/datatask>`__ by a package maintainer. First, install the dependencies required for packaging and publishing::

    python -m pip install .[publish]

Ensure that the correct version number appears in ``pyproject.toml``, and that any links in this README document to the Read the Docs documentation of this package (or its dependencies) have appropriate version numbers. Also ensure that the Read the Docs project for this library has an `automation rule <https://docs.readthedocs.io/en/stable/automation-rules.html>`__ that activates and sets as the default all tagged versions. Create and push a tag for this version (replacing ``?.?.?`` with the version number)::

    git tag ?.?.?
    git push origin ?.?.?

Remove any old build/distribution files. Then, package the source into a distribution archive::

    rm -rf build dist src/*.egg-info
    python -m build --sdist --wheel .

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__::

    python -m twine upload dist/*
