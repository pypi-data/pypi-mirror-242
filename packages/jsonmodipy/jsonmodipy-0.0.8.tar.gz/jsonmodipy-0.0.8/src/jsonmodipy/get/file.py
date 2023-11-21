"""Handles the get commands for a Python file."""
from ast import FunctionDef
from typing import List

from typeguard import typechecked

from jsonmodipy.apply.function_helper import get_ast_functions_in_file
from jsonmodipy.file_parsing import get_file_content
from jsonmodipy.Mod_file import Mod_file


@typechecked
def get_class_names(
    *,
    some_file: Mod_file,
) -> List[str]:
    """Returns all the class names of a python file."""
    print("TODO: Return class names of Python file.")
    print(some_file)
    return ["TODO", "TODO"]


@typechecked
def get_function_names(
    *,
    some_file: Mod_file,
) -> List[str]:
    """Returns all the function names of a python file."""
    file_functions: List[FunctionDef] = get_ast_functions_in_file(
        src_code=get_file_content(filepath=some_file.abs_filepath)
    )
    file_func_names: List[str] = list(
        map(lambda function: function.name, file_functions)
    )
    for file_function in file_functions:
        print(file_function.name)
    return file_func_names


@typechecked
def get_file_docstring(
    *,
    some_file: Mod_file,
) -> str:
    """Returns the docstring of a python file without quotations.

    Return empty string if it does not exist.
    """
    print("TODO: Return docstring of Python file.")
    print(some_file)
    return "TODO"
