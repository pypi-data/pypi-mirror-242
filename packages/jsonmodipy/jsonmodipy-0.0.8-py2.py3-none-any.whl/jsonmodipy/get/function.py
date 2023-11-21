"""Handles the get commands for a function in a file."""

from typing import Union

from libcst import FunctionDef, parse_module
from typeguard import typechecked

from jsonmodipy.get.function_location import get_function_from_location
from jsonmodipy.Mod_file import Mod_file

from ..file_parsing import load_file_content
from ..get.helper import get_code_for_node
from .helper_function import get_docstring_from_function_node


@typechecked
def get_function_docstring(
    *,
    some_file: Mod_file,
    func_location: str,
) -> str:
    """Returns the docstring of a Python function in a python file."""
    file_code: str = str(load_file_content(filepath=some_file.filepath))
    optional_func_node: Union[None, FunctionDef] = get_function_from_location(
        remaining_func_location=func_location,
        module=parse_module(file_code),
    )
    if optional_func_node is None:
        raise ValueError(f"Function {func_location} not found in file.")
    py_func_node: FunctionDef = optional_func_node

    func_docstring: str = get_docstring_from_function_node(
        py_func_node=py_func_node
    )
    return func_docstring


@typechecked
def get_function_src_code(
    *,
    some_file: Mod_file,
    func_location: str,
) -> str:
    """Returns the code of a Python function in a python file."""
    file_code: str = str(load_file_content(filepath=some_file.filepath))

    optional_func_node: Union[None, FunctionDef] = get_function_from_location(
        remaining_func_location=func_location,
        module=parse_module(file_code),
    )
    if optional_func_node is None:
        raise ValueError(f"Function {func_location} not found in file.")
    py_func_node: FunctionDef = optional_func_node

    py_func_str: str = get_code_for_node(some_node=py_func_node)
    return py_func_str


@typechecked
def get_function_test_file_code(
    *,
    some_file: Mod_file,
    func_name: str,
) -> str:
    """Returns the code of a test file that tests a Python function of a python
    file."""
    print("TODO: Return python test file code of the function in the file.")

    print(some_file)
    print(func_name)
    return "TODO"


@typechecked
def get_function_test_names(
    *,
    some_file: Mod_file,
    func_name: str,
) -> str:
    """Returns the names of the test functions of the test file that tests a
    Python function of a python file."""
    print("TODO: Return python test names of the function in the file.")
    print(some_file)
    print(func_name)
    return "TODO"
