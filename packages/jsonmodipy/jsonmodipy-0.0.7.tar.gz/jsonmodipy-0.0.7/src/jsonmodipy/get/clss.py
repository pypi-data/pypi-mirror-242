"""Handles the get commands for a class in a file."""
from typeguard import typechecked

from jsonmodipy.Mod_file import Mod_file


@typechecked
def get_class_docstring(
    *,
    class_name: str,
    some_file: Mod_file,
) -> str:
    """Returns the docstring of a Python class in a python file."""
    print("TODO: Return class docstring.")
    print(class_name)
    print(some_file)
    return "TODO"


@typechecked
def get_class_code(
    *,
    class_name: str,
    some_file: Mod_file,
) -> str:
    """Returns the code of a Python class in a python file."""
    print("TODO: Return Python code of the class in the file.")
    print(class_name)
    print(some_file)
    return "TODO"


@typechecked
def get_class_test_file_code(
    *,
    class_name: str,
    some_file: Mod_file,
) -> str:
    """Returns the code of a test file that tests a Python class of a python
    file."""
    print("TODO: Return python test file code of the class in the file.")
    print(class_name)
    print(some_file)
    return "TODO"


@typechecked
def get_class_test_names(
    *,
    class_name: str,
    some_file: Mod_file,
) -> str:
    """Returns the names of the test class of the test file that tests a Python
    class of a python file."""
    print("TODO: Return python test names of the class in the file.")
    print(class_name)
    print(some_file)
    return "TODO"
