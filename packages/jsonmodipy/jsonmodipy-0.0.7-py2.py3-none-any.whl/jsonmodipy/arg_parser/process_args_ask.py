"""Processes API arguments and performs the requested actions."""
from argparse import Namespace
from typing import Dict

from typeguard import typechecked

from jsonmodipy.arg_parser.process_args_engine import Llm_and_coms
from jsonmodipy.ask_llm.clss import (
    ask_class_comments,
    ask_class_docstring,
    ask_class_test_generation,
)
from jsonmodipy.ask_llm.file import ask_file_docstring
from jsonmodipy.ask_llm.function import (
    ask_function_comments,
    ask_function_docstring,
    ask_function_test_generation,
)
from jsonmodipy.chatgpt35.conversations.Conversation import Gpt_conversation
from jsonmodipy.file_parsing import load_file_content
from jsonmodipy.gpt_output.store_output import store_function_docstring
from jsonmodipy.Mod_file import Mod_file


@typechecked
def process_api_args_ask(
    *,
    args: Namespace,
    coms: Llm_and_coms,
    config: Dict[str, Dict[str, str]],
    some_file: Mod_file,
) -> None:
    """Processes the get arguments and performs the requested actions."""
    if args.ask in ["test-generation", "comments", "docstring"]:
        if args.question_filepath is None:
            raise ValueError(
                "Error, must specify question filepath if asking ChatGPT."
            )
        question: str = str(load_file_content(filepath=args.question_filepath))
        if question == "":
            raise ValueError("Error, question content was empty.")

        process_api_args_ask_file(
            args=args,
            some_file=some_file,
            question=question,
        )
        process_api_args_ask_function(
            args=args,
            coms=coms,
            config=config,
            some_file=some_file,
            question=question,
        )
        process_api_args_ask_class(
            args=args,
            some_file=some_file,
            question=question,
        )


def process_api_args_ask_file(
    *,
    args: Namespace,
    some_file: Mod_file,
    question: str,
) -> None:
    """Get file related information.

    If no function are specified, refer to file.
    """
    if args.ask == "test-generation" and not (args.func_location or args.clss):
        raise NotImplementedError(
            "Error, can not yet auto generate all tests for all functions and "
            "classes in a file, because those templates are not yet available"
            " within this repository."
        )
    if args.ask == "comments" and not (args.func_location or args.clss):
        # Return empty string if docstring does not exist.
        raise NotImplementedError(
            "Error, can not yet auto generate all tests for all functions and "
            "classes in a file, because those templates are not yet available"
            " within this repository."
        )
    if (
        args.ask == "docstring"
        and not (args.func_location or args.clss)
        and (args.question_filepath)
    ):
        ask_file_docstring(
            some_file=some_file,
            question=question,
        )


def process_api_args_ask_function(
    *,
    args: Namespace,
    coms: Llm_and_coms,
    config: Dict[str, Dict[str, str]],
    some_file: Mod_file,
    question: str,
) -> None:
    """Get function name related information."""

    if args.ask == "test-generation" and args.func_location is not None:
        ask_function_test_generation(
            some_file=some_file,
            func_location=args.func_location,
            question=question,
        )
    elif args.ask == "comments" and args.func_location is not None:
        ask_function_comments(
            some_file=some_file,
            func_location=args.func_location,
            question=question,
        )
    elif args.ask == "docstring" and args.func_location is not None:
        conversation: Gpt_conversation = ask_function_docstring(
            args=args,
            coms=coms,
            question=question,
            config=config,
            some_file=some_file,
        )
        store_function_docstring(
            some_file=some_file,
            func_location=args.func_location,
            conversation=conversation,
        )


def process_api_args_ask_class(
    *,
    args: Namespace,
    some_file: Mod_file,
    question: str,
) -> None:
    """Get class name related information."""
    if args.ask == "test-generation" and args.clss is not None:
        ask_class_test_generation(
            some_file=some_file,
            class_name=args.clss,
            question=question,
        )
    elif args.ask == "comments" and args.clss is not None:
        ask_class_comments(
            some_file=some_file,
            class_name=args.clss,
            question=question,
        )
    elif args.ask == "docstring" and args.clss is not None:
        ask_class_docstring(
            some_file=some_file,
            class_name=args.clss,
            question=question,
        )
