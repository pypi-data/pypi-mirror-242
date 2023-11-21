"""Handles the generate commands for a Python file."""
# pylint: disable=R0801
from typeguard import typechecked

from jsonmodipy.Mod_file import Mod_file


@typechecked
def apply_file_docstring_json_to_py(
    *,
    some_file: Mod_file,
    iteration: int,
) -> None:
    """
    0. Verifies the <filedir>/<filename>.py file has a valid Python syntax.
    1. Makes a .json backup of the file of the file
    <filedir>/<filename>.py
    named:
    <filedir>/<filename>_func_<file>_backup_docstring_<iteration>.json.
    2. Verifies the docstring contains the triple quotation mark start and end.
    3. Applies the docstring of the
    <filedir>/<filename>_func_<file>_gpt_<iteration>.json
    to the <filedir>/<filename>.py file
    4. Verifies the <filedir>/<filename>.py file still has a valid Python
    syntax.
    5. Applies black formatting.
    """
    # pylint: disable=R0801
    print("TODO: Apply docstring in file in Python file based on Json.")
    print(some_file)
    print(iteration)


@typechecked
def apply_file_json_to_py(
    *,
    some_file: Mod_file,
    iteration: int,
) -> None:
    """
    0. Verifies the <filedir>/<filename>.py file has a valid Python syntax.
    1. Makes a .json backup of the file of the file
    <filedir>/<filename>.py
    named:
    <filedir>/<filename>_func_<file>_backup_file_<iteration>.json.
    2. Verify all file args are typed.
    3. Verify the return type of the file is specified.
    4. Verifies the docstring contains the argument parameters.
    5. Verifies the docstring contains the argument parameter descriptions.
    6. Verifies the docstring contains the return description.
    7. Optional: Verify the file signature remains unchanged.
    8. Optional: Verify the file AST remains unchanged.
    9. Optional: Verify the decorators remain unchanged.
    10. Optional: Verify the ignore (lint) comments remain unchanged.
    11. Applies the file of the
    <filedir>/<filename>_func_<file>gpt_<iteration>.json
    file, to the <filedir>/<filename>.py file
    12. Verifies the <filedir>/<filename>.py file still has a valid Python
    syntax.
    13. Applies black formatting.

    """
    # pylint: disable=R0801
    print("TODO: Apply file from json to file in Python file.")
    print(some_file)
    print(iteration)


@typechecked
def apply_test_code_json_for_file_to_py(
    *,
    some_file: Mod_file,
    iteration: int,
    test_dir: int,
) -> None:
    """
    0. If the <test_dir>/unit_test/<filename>/test_<file>.py exists,
        0.a Verifies the <test_dir>/unit_test/<filename>/test_<file>.py
          file has a valid Python syntax.
        0.b Makes a .json backup of the test file:
        <test_dir>/unit_test/<filename>/test_<file>.py
        named:
        <test_dir>/unit_test/<filename>/test_<file>_backup_<iteration>.json
    2. Verify all file args are typed.
    3. Verify the return type of the file is specified.
    4. Verifies the docstring contains the argument parameters.
    5. Verifies the docstring contains the argument parameter descriptions.
    6. Verifies the docstring contains the return description.
    7. Optional: Verify the file signature remains unchanged.
    8. Optional: Verify the file AST remains unchanged.
    9. Optional: Verify the decorators remain unchanged.
    10. Optional: Verify the ignore (lint) comments remain unchanged.
    11. Applies the file of the
    <filedir>/<filename>_func_<file>gpt_<iteration>.json
    file, to the <filedir>/<filename>.py file
    12. Verifies the <filedir>/<filename>.py file still has a valid Python
    syntax.
    13. Applies black formatting.
    """
    print(
        "TODO: Apply test_code in Python file for file in python"
        + " file based on Json."
    )
    # pylint: disable=R0801
    print(some_file)
    print(iteration)
    print(test_dir)
