"""Parses CLI arguments for the API interactions."""
import argparse

from typeguard import typechecked


@typechecked
def parse_api_args() -> argparse.Namespace:
    """Reads command line arguments and converts them into Python arguments."""
    parser = argparse.ArgumentParser(
        description="CLI for handling JSON, Python code, and docstrings."
    )

    # Group for asking ChatGPT a question.
    engine_group = parser.add_argument_group(
        "Specify which LLM engine you want to use."
    )
    engine_group.add_argument(
        "--engine",
        required=True,
        choices=[
            "chatgpt4",
            "chatgpt3.5",
        ],
        help="Chose which LLM engine you would like to use.",
    )
    engine_group.add_argument(
        "--channel",
        required=True,
        choices=[
            "official",
            "browser",
        ],
        help="Chose which communication channel to use to talk to your LLM.",
    )

    # Group for asking ChatGPT a question.
    get_group = parser.add_argument_group("Ask question to ChatGPT")
    get_group.add_argument(
        "--ask",
        choices=[
            "test-generation",
            "comments",
            "docstring",
        ],
        help="Ask question to ChatGpt.",
    )

    # Group for getting information
    get_group = parser.add_argument_group(
        "Get Information from target repository"
    )
    get_group.add_argument(
        "--get",
        choices=[
            "class_names",
            "docstring",
            "func_names",
            "src_code",
            "test_code",
            "testnames",
        ],
        help="Get information from the target repository.",
    )

    # Group for getting information
    set_group = parser.add_argument_group(
        "Set the json file with the structure of the target repository."
    )
    set_group.add_argument(
        "--set",
        type=str,
        help="Set the json file with the structure of the target repository."
        + "Give a list of ; separated filepaths for which the functions, "
        "classes and tests are to be generated.",
    )
    set_group.add_argument(
        "--structure-json-filepath",
        type=str,
        help=("Absolute path towards the target repository."),
    )

    # Group for genting information
    gen_group = parser.add_argument_group("Apply Json to Python")
    gen_group.add_argument(
        "--apply",
        choices=["docstring", "src_code", "test_code"],
        help=(
            "Apply Json files from ChatGPT into the target repository "
            + "Python code."
        ),
    )

    # Group for getting information
    get_group = parser.add_argument_group("ChatGPT iteration number")
    get_group.add_argument(
        "--iteration",
        type=int,
        help="Perform actions on some edit iteration.",
    )

    # Common arguments
    parser.add_argument(
        "--filepath",
        help="Path to the file with function, a docstring, or classes.",
        type=str,
    )
    parser.add_argument(
        "--filepaths",
        help="List of filepaths to consider.",
        type=str,
    )

    parser.add_argument(
        "--apply-to-filepath",
        help="Filepath to the file that should be changed. (Used for temp"
        + " delta diff files).",
        type=str,
    )

    # Common arguments
    parser.add_argument(
        "--question-filepath",
        required=False,
        help="Path to the file with the question to ask ChatGPT.",
        type=str,
    )

    parser.add_argument(
        "--test-dir",
        help="Path to the unit test dir.",
        type=str,
    )

    parser.add_argument(
        "--func-location",
        help=(
            "Function path that you want to consider like: "
            + ".class.MyClass.function.some_function."
        ),
    )

    parser.add_argument(
        "--clss",
        help=(
            "List of classes that you want to consider"
            ". E.g. --classes Plant Sky"
        ),
    )

    parser.add_argument(
        "--compilability",
        type=int,
        help=(
            "The nr of times that the LLMs are asked to improve their answer"
            + "if it yielded an answer that prevents the code from compiling."
        ),
    )

    parser.add_argument(
        "--runnability",
        type=int,
        help=(
            "The nr of times that the LLMs are asked to improve their answer"
            + "if it yielded an answer that prevents the code from running on."
            + " a set of pre-determined commands."
        ),
    )
    parser.add_argument(
        "--precommit-passes",
        type=int,
        help=(
            "The nr of times that the LLMs are asked to improve their answer"
            + "if it yielded an answer that makes the code fail pre-commit "
            + "checks."
        ),
    )
    parser.add_argument(
        "--tests-pass",
        type=int,
        help=(
            "The nr of times that the LLMs are asked to improve their answer"
            + "if it yielded an answer that makes the code fail tests."
        ),
    )

    args = parser.parse_args()

    return args
