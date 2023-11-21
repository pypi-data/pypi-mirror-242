"""Handles the get commands for a Python file."""


from typeguard import typechecked

from jsonmodipy.Mod_file import Mod_file


@typechecked
def ask_file_docstring(
    *,
    some_file: Mod_file,
    question: str,
) -> None:
    """Returns all the class names of a python file."""
    print(some_file)
    print(question)
    print("TODO: Return class names of Python file.")
