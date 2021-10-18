"""
General-purpose data structure and representation format for tasks
(stand-alone or part of a larger data workflow) that involve multiple
data resources.
"""
from __future__ import annotations
from typing import Union
import doctest
import json

class datatask(dict):
    """
    Data structure that represents a data task. A data task consists of:

    * an optional collection of data resource name definitions (to allow
      for use of concise references within the input and output entries),
    * an optional list of input data resources (with optional schemas), and
    * a required list of output data resources (with a schema required
      for each output).

    The resource definitions attribute should be a map of names to
    individual file paths or URIs.

    >>> dt = datatask({
    ...     "resources": {
    ...         "abc": "https://examples.org/abc.txt",
    ...         "xyz": "xyz.txt"
    ...     },
    ...     "inputs": {"abc": ["column"]},
    ...     "outputs": {"xyz": [{"abc": "column"}]}
    ... })

    Any attempt to construct an instance with an invalid collection of
    resource definitions raises an exception.

    >>> dt = {"resources": [], "outputs": {"xyz.txt": []}}
    >>> datatask(dt) # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    TypeError: resources attribute value must be a dictionary that maps \
resource name strings to file path or URI strings
    >>> datatask({"resources": {"abc": 123}, "outputs": {"xyz.txt": []}})
    Traceback (most recent call last):
      ...
    TypeError: each resource entry value must be a path or URI string

    Input entries are specified using a dictionary that maps each input
    either to ``None`` or to its schema (consisting of a list of column names).

    >>> dt = datatask({
    ...     "inputs": {"abc.txt": ["a", "b", "c"], "def.csv": None},
    ...     "outputs": {"xyz.txt": []}
    ... })

    Any attempt to construct an instance with an invalid collection of
    input entries raises an exception.

    >>> dt = {"inputs": [], "outputs": {"xyz.txt": []}}
    >>> datatask(dt) # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    TypeError: inputs attribute must be a dictionary mapping resource names, \
paths, and/or URIs to schemas
    >>> dt = {"inputs": {123: []}, "outputs": {"xyz.txt": []}}
    >>> datatask(dt) # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    TypeError: each specified input must be a string corresponding to a defined \
resource name, a valid path, or a valid URI
    >>> datatask({"inputs": {"abc.txt": 123}, "outputs": {"xyz.txt": []}})
    Traceback (most recent call last):
      ...
    TypeError: input schema must be None or a list of strings

    A valid instance must have at least one output entry. Each output entry
    maps an output resource name, path, or URI to the schema for that output
    entry. The schema must be a list of dictionaries; no other constraints
    are enforced on the structure of a schema. A recommended approach is to
    use a dictionary such as ``{"abc.csv": "b"}`` to reference a named column
    ``"b"`` found in an input resource ``"abc.csv"``.

    >>> dt = datatask({
    ...     "resources": {
    ...         "xyz": "xyz.csv"
    ...     },
    ...     "inputs": {"abc.csv": ["a", "b", "c"]},
    ...     "outputs": {"xyz": [{"abc.csv": "c"}, {"abc.csv": "b"}]}
    ... })

    Any attempt to construct an instance without any output entries or an
    invalid collection of output entries raises an exception.

    >>> datatask.from_json({})
    Traceback (most recent call last):
      ...
    ValueError: at least one output must be specified
    >>> datatask.from_json({"outputs": {}})
    Traceback (most recent call last):
      ...
    ValueError: at least one output must be specified
    >>> datatask.from_json({"outputs": []}) # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    TypeError: outputs attribute must be a dictionary mapping resource names, \
paths, and/or URIs to schemas
    >>> datatask.from_json({"outputs": None}) # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    TypeError: outputs attribute must be a dictionary mapping resource \
names, paths, and/or URIs to schemas
    >>> datatask.from_json({"outputs": {123: []}}) # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    ValueError: each specified output must be a string corresponding to a \
defined resource name, a valid path, or a valid URI
    >>> datatask.from_json({"outputs": {"xyz.txt": 123}})
    Traceback (most recent call last):
      ...
    TypeError: output schema must be a list of dictionaries
    """
    def __new__(cls, argument: dict) -> datatask: # pylint: disable=R0912
        """
        Create class instance from a dictionary with a compatible structure.

        >>> datatask({"inputs": {}, "outputs": {"xyz.txt":[]}})
        {'inputs': {}, 'outputs': {'xyz.txt': []}}
        """
        # Check that the resources attribute has a valid structure.
        resources = {}
        if "resources" in argument:
            if not isinstance(argument["resources"], dict):
                raise TypeError(
                    'resources attribute value must be a dictionary ' + \
                    'that maps resource name strings to file path or ' + \
                    'URI strings'
                )

            resources = argument["resources"]
            if not all(isinstance(uri, str) for uri in resources.values()):
                raise TypeError(
                    'each resource entry value must be a path or URI string'
                )

        # Check that the inputs attribute has a valid structure.
        if "inputs" in argument:
            if not isinstance(argument["inputs"], dict):
                raise TypeError(
                    'inputs attribute must be a dictionary mapping ' + \
                    'resource names, paths, and/or URIs to schemas'
                )

            for (name_or_uri, schema) in argument["inputs"].items():
                if not isinstance(name_or_uri, str):
                    raise TypeError(
                        'each specified input must be a string corresponding to ' + \
                        'a defined resource name, a valid path, or a valid URI'
                    )
                if not (
                    schema is None or\
                    (
                        isinstance(schema, list) and\
                        all(isinstance(column, str) for column in schema)
                    )
                ):
                    raise TypeError(
                        'input schema must be None or a list of strings'
                    )

        # Check that the outputs attribute is present and has a valid structure.
        if "outputs" not in argument:
            raise ValueError('at least one output must be specified')

        if not isinstance(argument["outputs"], dict):
            raise TypeError(
                'outputs attribute must be a dictionary mapping ' + \
                'resource names, paths, and/or URIs to schemas'
            )

        if len(argument["outputs"]) == 0:
            raise ValueError('at least one output must be specified')

        for (name_or_uri, schema) in argument["outputs"].items():
            if not isinstance(name_or_uri, str):
                raise ValueError(
                    'each specified output must be a string corresponding to ' + \
                    'a defined resource name, a valid path, or a valid URI'
                )
            if not (
                isinstance(schema, list) and\
                all(isinstance(column, dict) for column in schema)
            ):
                raise TypeError(
                    'output schema must be a list of dictionaries'
                )

        return dict.__new__(cls, argument)

    @staticmethod
    def from_json(argument: Union[str, dict]) -> datatask:
        """
        Parse a dictionary or JSON string into an instance of this class.

        >>> datatask.from_json('{"outputs": {"xyz.txt":[]}}')
        {'outputs': {'xyz.txt': []}}
        >>> datatask.from_json({"inputs": {}, "outputs": {"xyz.txt":[]}})
        {'inputs': {}, 'outputs': {'xyz.txt': []}}
        """
        if isinstance(argument, str):
            argument = json.loads(argument)

        return datatask(argument)

    def to_json(self, *args, **kwargs) -> str:
        """
        Convert an instance of this class into a JSON string.

        >>> dt = datatask({"outputs": {"abc.text": []}})
        >>> dt.to_json()
        '{"outputs": {"abc.text": []}}'
        """
        return json.dumps(self, *args, **kwargs)

    def resources(self):
        """
        Return dictionary mapping resource name to resource URIs for this instance.

        >>> dt = datatask.from_json({
        ...     "inputs": {"abc.txt": None},
        ...     "outputs": {"xyz.text": [{"abc.txt": 0}]}
        ... })
        >>> dt.resources()
        {}
        """
        return self.get("resources", {})

    def inputs(self):
        """
        Return dictionary of inputs for this instance.

        >>> dt = datatask.from_json({
        ...     "inputs": {"abc.txt": None},
        ...     "outputs": {"xyz.text": [{"abc.txt": 0}]}
        ... })
        >>> dt.inputs()
        {'abc.txt': None}
        """
        return self.get("inputs", {})

    def outputs(self):
        """
        Return dictionary of outputs for this instance.

        >>> dt = datatask.from_json({
        ...     "inputs": {"abc.txt": None},
        ...     "outputs": {"xyz.text": [{"abc.txt": 0}]}
        ... })
        >>> dt.outputs()
        {'xyz.text': [{'abc.txt': 0}]}
        """
        return self.get("outputs", {})

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
