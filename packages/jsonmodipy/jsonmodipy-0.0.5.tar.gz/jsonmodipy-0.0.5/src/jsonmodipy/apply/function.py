"""Handles the generate commands for a function in a file."""

import os
from typing import Union

from typeguard import typechecked

from jsonmodipy.apply.function_helper import get_fat_docstr_from_gpt_convo_file
from jsonmodipy.apply.inject_func_docstr import inject_docstr_into_func
from jsonmodipy.file_parsing import (
    delete_file_if_exists,
    get_file_content,
    set_file_content,
)
from jsonmodipy.get.helper_function import FatDocstring
from jsonmodipy.gpt_output.gpt_output_paths import Gpt_output_paths
from jsonmodipy.Mod_file import Mod_file


@typechecked
def apply_function_docstring_json_to_py(
    *,
    some_file: Mod_file,
    func_location: str,
    iteration: int,
    output_file: Union[None, Mod_file],
) -> None:
    """
    0. Verifies the <filedir>/<filename>.py file has a valid Python syntax.
    1. Makes a .json backup of the function of the file
    <filedir>/<filename>.py
    named:
    <filedir>/<filename>_func_<function>_backup_docstring_<iteration>.json.
    2. Verifies the docstring contains the argument parameters.
    3. Verifies the docstring contains the argument parameter descriptions.
    4. Verifies the docstring contains the return description.
    5. Applies the docstring of the
    <filedir>/<filename>_func_<function>_gpt_<iteration>.json
    to the <filedir>/<filename>.py file
    6. Verifies the <filedir>/<filename>.py file still has a valid Python
    syntax.
    7. Applies black formatting.
    """

    original_content: str = get_file_content(filepath=some_file.abs_filepath)
    output_paths: Gpt_output_paths = Gpt_output_paths()
    # Create backup file of the original code file.
    backup_filepath: str = (
        output_paths.get_backup_dir(
            original_py=some_file,
        )
        + f"{some_file.filename}.txt"
    )
    if not os.path.isfile(backup_filepath):
        set_file_content(filepath=backup_filepath, content=original_content)
    if not os.path.isfile(backup_filepath):
        raise FileNotFoundError(f"File '{backup_filepath}' does not exist.")

    fatDocstring: FatDocstring = get_fat_docstr_from_gpt_convo_file(
        func_location=func_location,
        iteration=iteration,
        some_file=some_file,
    )
    new_unindented_docstr = fatDocstring.to_unindented_string()
    # Get arguments from the message.

    if new_unindented_docstr[:3] != '"""':
        new_unindented_docstr = '"""' + new_unindented_docstr + '"""'

    improved_code: str = inject_docstr_into_func(
        original_src=original_content,
        func_location=func_location,
        unindented_new_docstr=new_unindented_docstr,
        indentation_level=4,
    )

    if output_file is None:
        actual_output_file: Mod_file = some_file
    else:
        actual_output_file = output_file

    delete_file_if_exists(filepath=actual_output_file.abs_filepath)
    set_file_content(
        filepath=actual_output_file.abs_filepath, content=improved_code
    )


@typechecked
def apply_function_json_to_py(
    *,
    some_file: Mod_file,
    func_location: str,
    iteration: int,
) -> None:
    """
    0. Verifies the <filedir>/<filename>.py file has a valid Python syntax.
    1. Makes a .json backup of the function of the file
    <filedir>/<filename>.py
    named:
    <filedir>/<filename>_func_<function>_backup_function_<iteration>.json.
    2. Verify all function args are typed.
    3. Verify the return type of the function is specified.
    4. Verifies the docstring contains the argument parameters.
    5. Verifies the docstring contains the argument parameter descriptions.
    6. Verifies the docstring contains the return description.
    7. Optional: Verify the function signature remains unchanged.
    8. Optional: Verify the function AST remains unchanged.
    9. Optional: Verify the decorators remain unchanged.
    10. Optional: Verify the ignore (lint) comments remain unchanged.
    11. Applies the function of the
    <filedir>/<filename>_func_<function>gpt_<iteration>.json
    file, to the <filedir>/<filename>.py file
    12. Verifies the <filedir>/<filename>.py file still has a valid Python
    syntax.
    13. Applies black formatting.

    """
    print("TODO: Apply function from json to function in Python file.")
    print(some_file)
    print(func_location)
    print(iteration)


@typechecked
def apply_test_code_json_for_function_to_py(
    *,
    some_file: Mod_file,
    func_location: str,
    iteration: int,
    test_dir: int,
) -> None:
    """
    0. If the <test_dir>/unit_test/<filename>/test_<function>.py exists,
        0.a Verifies the <test_dir>/unit_test/<filename>/test_<function>.py
          file has a valid Python syntax.
        0.b Makes a .json backup of the test file:
        <test_dir>/unit_test/<filename>/test_<function>.py
        named:
        <test_dir>/unit_test/<filename>/test_<function>_backup_<iteration>.json
    2. Verify all function args are typed.
    3. Verify the return type of the function is specified.
    4. Verifies the docstring contains the argument parameters.
    5. Verifies the docstring contains the argument parameter descriptions.
    6. Verifies the docstring contains the return description.
    7. Optional: Verify the function signature remains unchanged.
    8. Optional: Verify the function AST remains unchanged.
    9. Optional: Verify the decorators remain unchanged.
    10. Optional: Verify the ignore (lint) comments remain unchanged.
    11. Applies the function of the
    <filedir>/<filename>_func_<function>gpt_<iteration>.json
    file, to the <filedir>/<filename>.py file
    12. Verifies the <filedir>/<filename>.py file still has a valid Python
    syntax.
    13. Applies black formatting.
    """
    print(
        "TODO: Apply test_code in Python file for function in python"
        + " file based on Json."
    )
    print(some_file)
    print(func_location)
    print(iteration)
    print(test_dir)
