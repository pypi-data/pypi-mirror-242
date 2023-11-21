"""Helps applying improvements to functions."""

import ast
import os
from ast import FunctionDef
from typing import List

from typeguard import typechecked

from jsonmodipy.chatgpt35.conversations.Conversation import Gpt_conversation
from jsonmodipy.file_parsing import load_conversation_from_json
from jsonmodipy.get.helper_function import FatDocstring
from jsonmodipy.gpt_output.gpt_output_paths import Gpt_output_paths
from jsonmodipy.gpt_output.verify_func_docstr import get_gpt_docstr_elems
from jsonmodipy.Mod_file import Mod_file


@typechecked
def get_ast_functions_in_file(*, src_code: str) -> List[FunctionDef]:
    """Get the functions in a file."""
    # Parse the source code into an AST
    tree = ast.parse(src_code)
    # tree = libcst.parse_module(src_code)
    functions: List[FunctionDef] = []

    # Traverse the AST to find functions and their indentation levels
    for node in ast.walk(tree):
        if isinstance(node, FunctionDef):
            functions.append(node)

    return functions


@typechecked
def get_fat_docstr_from_gpt_convo_file(
    *,
    func_location: str,
    iteration: int,
    some_file: Mod_file,
) -> FatDocstring:
    """Returns the docstring core of a function in a python file content with
    the chatgpt generated docstring core.

    a docstring core is the part of the docstring that does not have the
    arguments.
    """

    output_paths: Gpt_output_paths = Gpt_output_paths()

    llm_output_dir: str = output_paths.get_llm_output_dir(
        original_py=some_file,
        code_type="docstring",
        code_type_name=func_location,
    )

    gpt_output_filepath: str = f"{llm_output_dir}{iteration}.json"
    if not os.path.isfile(gpt_output_filepath):
        raise ValueError(
            f"Error, the file {llm_output_dir}/{iteration}.json does not "
            + "exist."
        )

    gpt_conversation: Gpt_conversation = load_conversation_from_json(
        json_path=gpt_output_filepath
    )

    # Load the gpt docstring core from file.
    funcDocstr: FatDocstring = get_gpt_docstr_elems(
        msg=gpt_conversation.messages[-1].message_str
    )
    return funcDocstr
