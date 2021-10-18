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
        """
        return self.get("resources", {})

    def inputs(self):
        """
        Return dictionary of inputs for this instance.
        """
        return self.get("inputs", {})

    def outputs(self):
        """
        Return dictionary of outputs for this instance.
        """
        return self.get("outputs", {})

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
