"""Verifies whether the ChatGPT output contains the required elements. First,
it determines which elements are expected in the function docstring response,
then it parses the function docstring response, and verifies the required
elements are included in the answer.

The function docstring could contain:
A string of text.
Function arguments with:
 - name
 - description
"""

import re
from typing import Dict, List, Tuple, Union

from libcst import FunctionDef, parse_module
from typeguard import typechecked

from jsonmodipy.file_parsing import load_file_content
from jsonmodipy.get.argument_getting import get_func_args
from jsonmodipy.get.function import get_function_docstring
from jsonmodipy.get.function_location import get_function_from_location
from jsonmodipy.get.helper_function import FatDocstring
from jsonmodipy.Mod_file import Mod_file
from jsonmodipy.PythonStructures import ArgStorage, TypeStorage


@typechecked
def get_expected_docstr_elems(
    *,
    func_location: str,
    some_file: Mod_file,
) -> FatDocstring:
    """some."""
    file_code: str = str(load_file_content(filepath=some_file.filepath))
    optional_func_node: Union[None, FunctionDef] = get_function_from_location(
        remaining_func_location=func_location,
        module=parse_module(file_code),
    )
    if optional_func_node is None:
        raise ValueError(f"Function {func_location} not found in file.")
    py_func_node: FunctionDef = optional_func_node

    actual_func_docstr: str = get_function_docstring(
        some_file=some_file,
        func_location=func_location,
    )

    func_args: List[ArgStorage] = get_func_args(py_func_node=py_func_node)

    # for func_arg in func_args:
    #     print(func_arg.to_python_string())
    return FatDocstring(docstring=actual_func_docstr, args=func_args)


@typechecked
def get_gpt_docstr_elems(*, msg: str) -> FatDocstring:
    """Converts the gpt output of a function or class docstring into a
    FatDocstring object."""
    arguments: List[ArgStorage] = get_gpt_func_args(msg=msg)
    return FatDocstring(docstring=get_gpt_docstr_core(msg=msg), args=arguments)


@typechecked
def get_gpt_docstr_core(*, msg: str) -> str:
    """Retrieves the primary docstring text (docstring core) of a function or
    class from a gpt output string."""
    start_line_nr: int
    end_line_nr: int
    # Replace the <p> and </p> tags with newlines
    msg = msg.replace("<p>", "\n").replace("</p>", "\n")
    # Split the response text into lines and process each line
    lines = msg.strip().split("\n")
    for i, line in enumerate(lines):
        if "|Docstring-core|" in line:
            start_line_nr = i + 1
            break
    for i in range(start_line_nr, len(lines)):
        if (
            "|End-docstring-core|" in lines[i]
            or "|End-Docstring-core|" in lines[i]
        ):
            end_line_nr = i
            break
        if is_arg_attribute_header(line=lines[i]):
            end_line_nr = i
            break

        if "|Return-" in lines[i][:7]:
            end_line_nr = i

        if "|End-response|" in lines[i]:
            end_line_nr = i
            break
    return str("\n".join(lines[start_line_nr:end_line_nr]))


@typechecked
def is_arg_attribute_header(*, line: str) -> bool:
    """Returns true if the line is a header for an argument attribute. Returns
    false otherwise.

    Argument attributes are: name, type, description.
    """
    if "|Arg" == line[:4]:
        for arg_attribute in ["-name", "-type", "-description"]:
            if is_match_with_nr_inbetween(
                before="Arg", after=arg_attribute, some_line=line
            ):
                return True
    return False


@typechecked
def get_gpt_func_args(*, msg: str) -> List[ArgStorage]:
    """some."""

    # Initialize variables to store argument information
    arguments: List[ArgStorage] = []
    current_arg: Dict[str, str] = {}

    # Replace the <p> and </p> tags with newlines
    msg = msg.replace("<p>", "\n").replace("</p>", "\n")
    # Split the response text into lines and process each line
    lines = msg.strip().split("\n")
    for i, line in enumerate(lines):
        # Check if an argument exists.
        if is_match_with_nr_inbetween(
            before="Arg", after="-name", some_line=line
        ):
            # An argument exists, get its name.
            current_arg["name"] = lines[i + 1]
            arg_nr: int = get_number_in_between(
                before="Arg", after="-name", some_line=line
            )

            # Check if the arg type is included, and if yes, store it.
            list_contains, line_nr = list_contains_substring(
                lines=lines, substring=f"Arg{arg_nr}-type"
            )
            if list_contains:
                # This is a placeholder to simplify type checking on the dict.
                current_arg["arg_type"] = "placeholder"
                typeStorage: TypeStorage = TypeStorage(
                    the_type=str(lines[line_nr + 1])
                )

            # Check if the arg description is included, and if yes, store it.
            list_contains, line_nr = list_contains_substring(
                lines=lines, substring=f"Arg{arg_nr}-description"
            )
            if list_contains:
                # current_arg["description"] = lines[i + 3]
                current_arg["description"] = lines[line_nr + 1]

            # Merge the args into a single object and add it to the list.
            arguments.append(
                ArgStorage(
                    str(current_arg["name"]),
                    typeStorage
                    # pylint:disable=C0201
                    if "arg_type" in current_arg.keys() else None,
                    str(current_arg["description"])
                    # pylint:disable=C0201
                    if "description" in current_arg.keys() else None,
                )
            )
            current_arg = {}
    return arguments


def list_contains_substring(
    *, lines: List[str], substring: str
) -> Tuple[bool, int]:
    """Check if any element in a list contains a specified substring and return
    the index of the first matching element.

    Args:
        lines (List[str]): The list of strings to search within.
        substring (str): The substring to search for.

    Returns:
        Tuple[bool, int]: A tuple containing a boolean indicating if any
        element in the list contains the substring, and the index of the first
        matching element. If no match is found, the index is -1.

    Example:
        >>> list_contains_substring(["apple", "banana", "cherry"], "an")
        (True, 0)  # "apple" contains "an" and is the first matching element
        at index 0.
        >>> list_contains_substring(["apple", "banana", "cherry"], "kiwi")
        (False, -1)  # No element contains "kiwi," so the result is
        (False, -1).
    """
    for line_nr, element in enumerate(lines):
        if substring in element:
            return True, line_nr
    return False, -1


@typechecked
def is_match_with_nr_inbetween(
    *, before: str, after: str, some_line: str
) -> bool:
    """Returns True if the some_line string matches pattern:
    <before><any_number><after>
     Returns False otherwise."""
    # Create a regular expression pattern to match the desired format
    pattern = re.compile(re.escape(before) + r"\d+" + re.escape(after))

    # Use the search method to find a match in the some_line string
    match = pattern.search(some_line)

    # If a match is found, return True; otherwise, return False
    return bool(match)


def get_number_in_between(*, before: str, after: str, some_line: str) -> int:
    """Extracts a number from a string located between two specified
    substrings.

    Args:
        before (str): The substring that comes before the desired number.
        after (str): The substring that comes after the desired number.
        some_line (str): The input string to search within.

    Returns:
        int: The extracted number as an integer.

    Raises:
        ValueError: If the number is not found or cannot be converted to an
        integer.

    Example:
        >>> get_number_in_between("Arg", "-name", "Arg42-name")
        42
        >>> get_number_in_between("Start", "End", "Start123End")
        123
        >>> get_number_in_between("Prefix", "Suffix", "PrefixSuffix")
        Traceback (most recent call last):
            ...
        ValueError: Number not found or cannot be converted to an integer.
    """
    start_index = some_line.find(before)
    if start_index == -1:
        raise ValueError("Number not found.")

    start_index += len(before)
    end_index = some_line.find(after, start_index)
    if end_index == -1:
        raise ValueError("Number not found.")

    number_str = some_line[start_index:end_index]
    return int(number_str)
