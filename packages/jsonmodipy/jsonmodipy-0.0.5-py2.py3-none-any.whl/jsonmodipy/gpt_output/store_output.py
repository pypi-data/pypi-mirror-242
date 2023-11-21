"""Stores the unparsed output of ChatGPT.

The gpt_output storage format is given in the code of Gpt_output_paths.
"""
# pylint: disable=R0801
import os

from typeguard import typechecked

from jsonmodipy.chatgpt35.conversations.Conversation import Gpt_conversation
from jsonmodipy.file_parsing import create_relative_path, write_dict_to_json
from jsonmodipy.gpt_output.gpt_output_paths import Gpt_output_paths
from jsonmodipy.Mod_file import Mod_file


@typechecked
def store_function_docstring(
    *, some_file: Mod_file, func_location: str, conversation: Gpt_conversation
) -> None:
    """Stores the function docstring output of ChatGPT to a file.

    First finds the original file, then checks if there already exist
    function_docstring gpt output files, then it gets the current index
    of the function docstring output, and stores the new
    function_docstring file.
    """
    extension_with_dot: str = ".json"
    # Verify the original Python file exists.
    if not os.path.isfile(some_file.filepath):
        raise FileNotFoundError(f"File '{some_file.filepath}' does not exist.")
    output_paths: Gpt_output_paths = Gpt_output_paths()
    # Get the file path of the function docstring output.
    # TODO: refactor to remove file_segment, and use the function/class
    # location instead.
    llm_output_dir: str = output_paths.get_llm_output_dir(
        code_type="docstring",
        code_type_name=func_location,
        original_py=some_file,
    )
    gpt_output_nr: int = output_paths.get_new_gpt_output_index(
        extension_with_dot=extension_with_dot,
        code_type="docstring",
        code_type_name=func_location,
        original_py=some_file,
    )
    create_relative_path(relative_path=llm_output_dir)
    # Store the function docstring output.
    write_dict_to_json(
        filepath=f"{llm_output_dir}{gpt_output_nr}.json",
        data=conversation.to_json(),
    )

    # Assert file exists.
    if not os.path.isfile(
        f"{llm_output_dir}{gpt_output_nr}{extension_with_dot}"
    ):
        raise FileNotFoundError(
            f"File '{llm_output_dir}/{gpt_output_nr}{extension_with_dot}'"
            + " does not exist."
        )
