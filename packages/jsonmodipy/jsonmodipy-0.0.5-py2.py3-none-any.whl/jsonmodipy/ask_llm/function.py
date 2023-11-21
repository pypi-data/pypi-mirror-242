"""Handles the get commands for a function in a file."""
from argparse import Namespace
from typing import Dict, List, Optional

from typeguard import typechecked

from jsonmodipy.arg_parser.process_args_engine import Llm_and_coms
from jsonmodipy.ask_llm.ask_gpt import ask_question
from jsonmodipy.chatgpt35.conversations.Conversation import Gpt_conversation
from jsonmodipy.get.helper_function import FatDocstring
from jsonmodipy.gpt_output.verify_func_docstr import get_expected_docstr_elems
from jsonmodipy.Mod_file import Mod_file
from jsonmodipy.PythonStructures import ArgStorage


@typechecked
def ask_function_test_generation(
    *,
    some_file: Mod_file,
    func_location: str,
    question: str,
) -> None:
    """Asks ChatGPT/some engine to generate unit tests for a function."""

    print(some_file)
    print(f"func_location={func_location}")
    print(f"question={question}")
    print("TODO: Ask ChatGPT to generate unit tests for function.")
    print("TODO: Verify ChatGPT unit tests pass.")


@typechecked
def ask_function_comments(
    *,
    some_file: Mod_file,
    func_location: str,
    question: str,
) -> None:
    """Asks ChatGPT/some engine to generate code comments for a function."""
    print(some_file)
    print(f"func_location={func_location}")
    print(f"question={question}")
    print("TODO: Ask ChatGPT to generate function code comments.")
    print("TODO: Verify ChatGPT function code comments preserved code/syntax.")


@typechecked
def ask_function_docstring(
    *,
    args: Namespace,
    coms: Llm_and_coms,
    question: str,
    some_file: Mod_file,
    config: Optional[Dict[str, Dict[str, str]]] = None,
    incoming_conversation: Optional[Gpt_conversation] = None,
) -> Gpt_conversation:
    """Asks ChatGPT/some engine to generate the docstring for a function."""
    conversation: Gpt_conversation = ask_question(
        question=question,
        coms=coms,
        config=config,
        conversation=incoming_conversation,
    )

    # TODO: check if args are missing, and ask for them if so.

    fat_docstr: FatDocstring = get_expected_docstr_elems(
        func_location=args.func_location,
        some_file=some_file,
    )
    expected_args: List[ArgStorage] = fat_docstr.args

    conversation.messages[-1].set_expected_args(expected_args=expected_args)

    return conversation
