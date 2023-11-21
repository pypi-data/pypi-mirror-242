"""Generates a JSON representation of the structure of a Python file.

# Example usage:
if __name__ == "__main__":
    source_code = some_file_src = \"\"\"
class MyClass:
    def __init__(self):
        pass

    def my_method(self):
        pass

def my_function():
    pass
\"\"\"

    structure = parse_python_file(source_code)
    print(structure.to_json())
"""
from typing import Any, Dict, List, Optional

import libcst as cst
from typeguard import typechecked


# pylint: disable=R0903
class Classdef:
    """Represents a class definition within a Python file.

    Attributes:
        classes (List[Classdef]): A list of nested Classdef objects
        representing classes within this class.
        functions (List[Functiondef]): A list of Functiondef objects
        representing functions within this class.
    """

    @typechecked
    def __init__(self, name: str) -> None:
        """Initializes a Classdef instance with empty lists for nested classes
        and functions."""
        self.name: str = name
        self.classes: List["Classdef"] = []
        self.functions: List["Functiondef"] = []


# pylint: disable=R0903
# pylint: disable=R0903
class Functiondef:
    """Represents a function definition within a Python file.

    Attributes:
        classes (List[Classdef]): A list of nested Classdef objects
        representing classes within this function.
        functions (List[Functiondef]): A list of nested Functiondef objects
        representing functions within this function.
    """

    def __init__(self, name: str):
        """Initializes a Functiondef instance with empty lists for nested
        classes and functions."""
        self.name: str = name
        self.classes: List[Classdef] = []
        self.functions: List["Functiondef"] = []


# pylint: disable=R0903
class PythonFileStructure:
    """Represents the structure of a parsed Python file, including classes and
    functions.

    Attributes:
        classes (List[Classdef]): A list of Classdef objects representing the
        classes in the Python file.
        functions (List[Functiondef]): A list of Functiondef objects
        representing the functions in the Python file.

    Methods:
        to_json() -> Dict: Converts the PythonFileStructure to a dictionary
        representation.
        _class_to_dict(class_obj) -> Dict: Converts a Classdef object to a
        dictionary.
        _function_to_dict(function_obj) -> Dict: Converts a Functiondef object
          to a dictionary.
    """

    @typechecked
    def __init__(self) -> None:
        """Initializes a PythonFileStructure instance with empty lists for
        classes and functions."""
        self.classes: List[Classdef] = []
        self.functions: List[Functiondef] = []

    @typechecked
    def to_json(self) -> Dict:  # type: ignore[type-arg]
        """Converts the PythonFileStructure to a dictionary representation.

        Returns:
            Dict: A dictionary representing the PythonFileStructure.
                It contains keys 'classes' and 'functions', each mapping to a
                list of dictionaries.
        """
        return {
            "classes": [self._class_to_dict(c) for c in self.classes],
            "functions": [self._function_to_dict(f) for f in self.functions],
        }

    @typechecked
    def _class_to_dict(
        self, class_obj: "Classdef"
    ) -> Dict:  # type: ignore[type-arg]
        """Converts a Classdef object to a dictionary.

        Parameters:
            class_obj: The Classdef object to convert.

        Returns:
            Dict: A dictionary representing the Classdef object.
        """
        return {
            "name": class_obj.name,
            "classes": [self._class_to_dict(c) for c in class_obj.classes],
            "functions": [
                self._function_to_dict(f) for f in class_obj.functions
            ],
        }

    @typechecked
    def _function_to_dict(self, function_obj: "Functiondef") -> Dict[str, Any]:
        """Converts a Functiondef object to a dictionary.

        Parameters:
            function_obj: The Functiondef object to convert.

        Returns:
            Dict: A dictionary representing the Functiondef object.
        """
        return {
            "name": function_obj.name,
            "classes": [self._class_to_dict(c) for c in function_obj.classes],
            "functions": [
                self._function_to_dict(f) for f in function_obj.functions
            ],
        }


@typechecked
def parse_python_file(source_code: str) -> PythonFileStructure:
    """Parses a Python source code and constructs a PythonFileStructure to
    represent its class and function definitions.

    Parameters:
        source_code (str): The Python source code to parse.

    Returns:
        PythonFileStructure: A structured representation of the parsed
        Python source code.
    """

    # Parse the source code using libcst
    module = cst.parse_module(source_code)

    # Create a PythonFileStructure instance to store the parsed structure
    file_structure: PythonFileStructure = PythonFileStructure()

    # Helper function to traverse the CST and extract class and function
    # definitions.
    @typechecked
    def traverse(  # type: ignore[no-untyped-def]
        *,
        node: Any,
        parent_class: Optional[Any] = None,
    ):
        if isinstance(node, cst.ClassDef):
            class_obj = Classdef(name=node.name.value)
            if parent_class:
                parent_class.classes.append(class_obj)
            else:
                file_structure.classes.append(class_obj)
            if isinstance(node.body, cst.IndentedBlock):
                for item in node.body.body:
                    traverse(node=item, parent_class=class_obj)
            else:
                traverse(node=node.body, parent_class=class_obj)
        elif isinstance(node, cst.FunctionDef):
            function_obj = Functiondef(name=node.name.value)
            if parent_class:
                parent_class.functions.append(function_obj)
            else:
                file_structure.functions.append(function_obj)
            if isinstance(node.body, cst.IndentedBlock):
                for item in node.body.body:
                    traverse(node=item, parent_class=function_obj)
            else:
                traverse(node=node.body, parent_class=parent_class)

    # Start traversing the CST
    for item in module.body:
        traverse(node=item)
    return file_structure
