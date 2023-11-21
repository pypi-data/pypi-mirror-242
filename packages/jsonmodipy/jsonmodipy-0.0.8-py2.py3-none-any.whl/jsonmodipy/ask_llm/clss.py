"""Handles the get commands for a class in a file."""
from typeguard import typechecked

from jsonmodipy.Mod_file import Mod_file


@typechecked
def ask_class_test_generation(
    *,
    some_file: Mod_file,
    class_name: str,
    question: str,
) -> None:
    """Asks ChatGPT/some engine to generate unit tests for a class."""
    print(some_file)
    print(f"class_name={class_name}")
    print(f"question={question}")
    print("TODO: Ask ChatGPT to generate unit tests for class.")
    print("TODO: Verify ChatGPT unit tests pass.")


@typechecked
def ask_class_comments(
    *,
    some_file: Mod_file,
    class_name: str,
    question: str,
) -> None:
    """Asks ChatGPT/some engine to generate code comments for a class."""
    print(some_file)
    print(f"class_name={class_name}")
    print(f"question={question}")
    print("TODO: Ask ChatGPT to generate class code comments.")
    print("TODO: Verify ChatGPT class code comments preserved code/syntax.")


@typechecked
def ask_class_docstring(
    *,
    some_file: Mod_file,
    class_name: str,
    question: str,
) -> None:
    """Asks ChatGPT/some engine to generate the docstring for a class."""
    print(some_file)
    print(f"class_name={class_name}")
    print(f"question={question}")
    print("TODO: Ask ChatGPT to generate docstring of class.")
