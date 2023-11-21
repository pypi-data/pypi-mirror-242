"""Stores hardcoded project data."""

import os
from typing import List

from typeguard import typechecked


# pylint: disable=R0903
class Mod_file:
    """Stores modular file."""

    @typechecked
    def __init__(
        self,
        filedir: str,
        filename: str,
        extension: str,
    ) -> None:
        """Store a modular file in format: <filedir><filename><extension> for
        /some_path/other_dir/some_filename.txt with:
        <filedir>=/some_path/other_dir/
        <filename>=some_filename
        <extension>=.txt

        TODO: assert directory, and file exist.
        ."""
        self.filedir: str = filedir
        self.filename: str = filename
        self.extension: str = extension
        if f"{filedir}"[-1] != "/":
            raise ValueError(
                "Error, filedir and filename must end with a '/'. Got: "
                + f"{filedir}{filename}."
            )
        self.filepath: str = f"{filedir}{filename}{extension}"
        self.abs_filepath: str = os.path.abspath(self.filepath)


@typechecked
def has_duplicates(*, filepaths: List[Mod_file]) -> bool:
    """Returns True if there are duplicates filepaths in the list, False
    otherwise.

    Args:
        filepaths (List[Mod_file]): A list of Mod_file objects with
        'abs_filepath' attribute.

    Returns:
        bool: Returns True if there are duplicates filepaths in the list, False
         otherwise.
    """
    filepath_set = set()
    for file in filepaths:
        if file.abs_filepath in filepath_set:
            return True  # Duplicate found
        filepath_set.add(file.abs_filepath)
    return False  # No duplicates found
