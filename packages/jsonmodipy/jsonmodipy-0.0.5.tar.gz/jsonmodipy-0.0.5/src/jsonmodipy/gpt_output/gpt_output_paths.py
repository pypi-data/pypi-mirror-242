"""This file implements the way the output of the LLMs is stored, and how the
backups of the target code files are made.

See docs/source/intro/datastructures.md for the datastructure of the gpt
output.
"""

import os
from typing import List, Optional

from typeguard import typechecked

from jsonmodipy.file_parsing import delete_file_if_exists
from jsonmodipy.Hardcoded import Hardcoded
from jsonmodipy.Mod_file import Mod_file


class Gpt_output_paths:
    """Stores the hardcoded paths for the GPT output files."""

    @typechecked
    def __init__(self) -> None:
        """Initialise the hardcoded data."""
        self.code_types: List[str] = ["docstring", "comments", "tests"]
        self.llm_storage_dirname: str = Hardcoded().llm_storage_dirname

    @typechecked
    def assert_code_type_is_valid(self, code_type: str) -> None:
        """Asserts the code type is valid."""
        if code_type not in self.code_types:
            if code_type == "comment":
                print("Did you mean 'comments'?")
            if code_type == "test":
                print("Did you mean 'tests'?")
            raise ValueError(
                f"Error, code_type={code_type} is not a valid code type."
            )

    @typechecked
    def get_backup_dir(
        self,
        original_py: Mod_file,
    ) -> str:
        """Returns the backup dir for a default code file."""
        return (
            f"{original_py.filedir}{self.llm_storage_dirname}/"
            + f"{original_py.filename}/backup/"
        )

    @typechecked
    def get_llm_output_dir(
        self,
        original_py: Mod_file,
        code_type: str,
        code_type_name: Optional[str] = None,
    ) -> str:
        """Returns directory to which the LLM output is stored as .txt file."""

        self.assert_code_type_is_valid(code_type=code_type)

        if code_type in ["docstring", "comments"]:
            return self.get_docstr_or_comment_dir(
                original_py=original_py,
                code_type=code_type,
                code_type_name=code_type_name,
            )
        if code_type in ["tests"]:
            return self.get_relative_test_dir(
                original_py=original_py,
                code_type_name=code_type_name,
            )
        raise ValueError("Superfluous error message, code_type is not valid.")

    @typechecked
    def get_docstr_or_comment_dir(
        self,
        original_py: Mod_file,
        code_type: str,
        code_type_name: Optional[str] = None,
    ) -> str:
        """Returns the file_dir in which the LLM output will be stored for the
        given target file improvement request.

        A similar but different path is used to create the backup of a
        file. This is done in function get_backup_path().
        """
        path_to_llm_filedir: str
        cmd_related_path: str
        # This function should not be called for tests.
        if code_type == "tests":
            raise ValueError(
                "Error, can not give a directory for improvement suggestions"
                "on tests in this function. Look at get_relative_test_dir()."
            )
        if code_type == "comments" and code_type_name is None:
            raise ValueError(
                "Error, cannot give directory for improvement suggestions for "
                + "all the comments in a file."
            )

        # Construct the base path for the LLM output related to the original_py
        # file.
        path_to_llm_filedir = (
            original_py.filedir
            + self.llm_storage_dirname
            + "/"
            + original_py.filename
            + "/"
        )
        if code_type_name is None:
            cmd_related_path = code_type + "/"
        else:
            cmd_related_path = code_type_name + "/" + code_type + "/"
        return f"{path_to_llm_filedir}{cmd_related_path}"

    @typechecked
    def get_relative_test_dir(
        self,
        original_py: Mod_file,
        code_type_name: Optional[str] = None,
    ) -> str:
        """Returns the file_dir in which the LLM output will be stored that
        specifies the test files that test the given target file and
        function/class."""
        path_to_llm_filedir: str
        cmd_related_path: str
        path_to_llm_filedir = (
            "tests/unit/"
            + original_py.filedir
            + "/"
            + original_py.filename
            + "/"
        )
        if code_type_name is None:
            raise ValueError("Error, code_type_name is None.")
        cmd_related_path = code_type_name + "/"
        return f"{path_to_llm_filedir}{cmd_related_path}"

    # pylint: disable=R0913
    @typechecked
    def get_new_gpt_output_index(
        self,
        extension_with_dot: str,
        code_type: str,
        code_type_name: str,
        original_py: Mod_file,
    ) -> int:
        """Returns the index of the gpt_output file."""
        # Find what the greatest index of the file is.
        index: int = 0

        llm_output_dir: str = self.get_llm_output_dir(
            code_type=code_type,
            code_type_name=code_type_name,
            original_py=original_py,
        )

        if not os.path.isdir(llm_output_dir):
            print(f"not isdir: {llm_output_dir}")
            return 0

        # Get the index of the gpt_output file.
        for file in os.listdir(llm_output_dir):
            if file.endswith(extension_with_dot):
                index += 1
        return index

    # pylint: disable=R0913
    @typechecked
    def delete_all_suggestions(
        self,
        extension_with_dot: str,
        code_type: str,
        code_type_name: str,
        original_py: Mod_file,
    ) -> None:
        """Deletes all versions 0 to x of LLM output for a specific code type
        of a specific code_type_name of a specific file.

        (E.g. the documentation of the add_two functions of the adder.py
        file.)
        """
        counter: int = 0
        while (
            self.get_new_gpt_output_index(
                extension_with_dot=extension_with_dot,
                code_type=code_type,
                code_type_name=code_type_name,
                original_py=original_py,
            )
            != 0
        ):
            counter += 1
            llm_output_dir: str = self.get_llm_output_dir(
                code_type=code_type,
                code_type_name=code_type_name,
                original_py=original_py,
            )
            latest_new_index: int = self.get_new_gpt_output_index(
                extension_with_dot=extension_with_dot,
                code_type=code_type,
                code_type_name=code_type_name,
                original_py=original_py,
            )

            # Delete the latest existing file (=latest_new_index -1)
            latest_filepath: str = (
                f"{llm_output_dir}{latest_new_index - 1}{extension_with_dot}"
            )
            delete_file_if_exists(filepath=latest_filepath)
