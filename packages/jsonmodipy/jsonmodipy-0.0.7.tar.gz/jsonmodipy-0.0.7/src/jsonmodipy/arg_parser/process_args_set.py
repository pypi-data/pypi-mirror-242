"""Processes API arguments and performs the requested actions."""
import os
from argparse import Namespace
from typing import Dict, List

from typeguard import typechecked

from jsonmodipy.file_parsing import (
    create_relative_path,
    load_file_content,
    split_filepath,
    split_filepaths_into_files,
    write_dict_to_json,
)
from jsonmodipy.Mod_file import Mod_file, has_duplicates
from jsonmodipy.set.create_jsonstructure import (
    PythonFileStructure,
    parse_python_file,
)


@typechecked
def process_api_args_set(*, args: Namespace) -> None:
    """Processes the get arguments and performs the requested actions."""
    if args.set is not None:
        if args.filepaths is None:
            raise ValueError(
                "Error, include filepaths if you desire to get the json "
                + "structure of the target repository."
            )

        if args.structure_json_filepath is not None:
            json_structure_file: Mod_file = split_filepath(
                filepath=args.structure_json_filepath
            )

            json_structure: Dict[str, Dict] = {}  # type: ignore[type-arg]

            # Process the files that are passed into this arg.
            filepaths: List[Mod_file] = split_filepaths_into_files(
                some_filepaths=args.filepaths
            )

            # Verify there are no duplicate filepaths in the list.
            if has_duplicates(filepaths=filepaths):
                raise ValueError(
                    "Error, duplicate filepaths not permitted in json "
                    + "structure."
                )

            for some_file in filepaths:
                source_code: str = str(
                    load_file_content(filepath=some_file.abs_filepath)
                )
                pythonFileStructure: PythonFileStructure = parse_python_file(
                    source_code=source_code
                )
                json_structure[
                    some_file.abs_filepath
                ] = pythonFileStructure.to_json()
            create_relative_path(relative_path=json_structure_file.filedir)
            write_dict_to_json(
                data={"filepaths": json_structure},
                filepath=args.structure_json_filepath,
            )
            if not os.path.exists(args.structure_json_filepath):
                raise FileNotFoundError(
                    "Error, the json structure file was not created."
                )

        else:
            raise ValueError(
                "Error, if you want the json of with the structure of the "
                + "target repository, you must provide the path to the json "
                + "file."
            )
