"""Handles the generate commands for a class in a file."""

from typeguard import typechecked

from jsonmodipy.Mod_file import Mod_file


@typechecked
def apply_class_docstring_json_to_py(
    *,
    class_name: str,
    some_file: Mod_file,
    iteration: int,
) -> None:
    """
    0. Verifies the <filedir>/<filename>.py file has a valid Python syntax.
    1. Makes a .json backup of the class of the file
    <filedir>/<filename>.py
    named:
    <filedir>/<filename>_class_<class>_backup_docstring_<iteration>.json.
    2. Verifies the docstring contains the argument parameters.
    3. Verifies the docstring contains the argument parameter descriptions.
    4. Verifies the docstring contains the return description.
    5. Applies the docstring of the
    <filedir>/<filename>_class_<class>gpt_<iteration>.json
    to the <filedir>/<filename>.py file
    6. Verifies the <filedir>/<filename>.py file still has a valid Python
    syntax.
    7. Applies black formatting.

    """
    print("TODO: Apply docstring in class in Python file based on Json.")
    print(class_name)
    print(some_file)

    print(iteration)


@typechecked
def apply_class_json_to_py(
    *,
    class_name: str,
    some_file: Mod_file,
    iteration: int,
) -> None:
    r"""
    0. Verifies the <filedir>/<filename>.py file has a valid Python syntax.
    1. Makes a .json backup of the class of the file
    <filedir>/<filename>.py
    named:
    <filedir>/<filename>_class\_<class>_backup_class_<iteration>.json.
    2. Verify all class args are typed.
    3. Verify the return type of the class is specified.
    4. Verifies the docstring contains the argument parameters.
    5. Verifies the docstring contains the argument parameter descriptions.
    6. Verifies the docstring contains the return description.
    7. Optional: Verify the class signature remains unchanged.
    8. Optional: Verify the class AST remains unchanged.
    9. Optional: Verify the decorators remain unchanged.
    10. Optional: Verify the ignore (lint) comments remain unchanged.
    11. Applies the class of the
    <filedir>/<filename>_class_<class>gpt_<iteration>.json
    file, to the <filedir>/<filename>.py file
    12. Verifies the <filedir>/<filename>.py file still has a valid Python
    syntax.
    13. Applies black formatting.
    """
    print("TODO: Apply class from json to class in Python file.")
    print(class_name)
    print(some_file)

    print(iteration)


@typechecked
def apply_test_code_json_for_class_to_py(
    *,
    class_name: str,
    some_file: Mod_file,
    iteration: int,
    test_dir: int,
) -> None:
    """
    0. If the <test_dir>/unit_test/<filename>/test_<class>.py exists,
        0.a Verifies the <test_dir>/unit_test/<filename>/test_<class>.py
          file has a valid Python syntax.
        0.b Makes a .json backup of the test file:
        <test_dir>/unit_test/<filename>/test_<class>.py
        named:
        <test_dir>/unit_test/<filename>/test_<class>_backup_<iteration>.json
    2. Verify all class args are typed.
    3. Verify the return type of the class is specified.
    4. Verifies the docstring contains the argument parameters.
    5. Verifies the docstring contains the argument parameter descriptions.
    6. Verifies the docstring contains the return description.
    7. Optional: Verify the class signature remains unchanged.
    8. Optional: Verify the class AST remains unchanged.
    9. Optional: Verify the decorators remain unchanged.
    10. Optional: Verify the ignore (lint) comments remain unchanged.
    11. Applies the class of the
    <filedir>/<filename>_class_<class>gpt_<iteration>.json
    file, to the <filedir>/<filename>.py file
    12. Verifies the <filedir>/<filename>.py file still has a valid Python
    syntax.
    13. Applies black formatting.
    """
    print(
        "TODO: Apply test_code in Python file for class in python"
        + " file based on Json."
    )
    print(class_name)
    print(some_file)

    print(iteration)
    print(test_dir)
