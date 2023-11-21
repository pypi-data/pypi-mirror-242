"""Loads Python file content into string, and performs checks on Python
files."""
import configparser
import json
import os
import subprocess  # nosec
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Union

from typeguard import typechecked

from jsonmodipy.chatgpt35.conversations.Conversation import Gpt_conversation
from jsonmodipy.chatgpt35.conversations.Gpt_message import Gpt_message
from jsonmodipy.Mod_file import Mod_file

from .PythonStructures import JsonContentType

if TYPE_CHECKING:
    from jsonmodipy.arg_parser.process_args_engine import Llm_and_coms


def split_filepath(*, filepath: str) -> Mod_file:
    """Split a file path into directory path, filename, and extension.

    Args:
        filepath (str): The input file path.

    Returns:
        Tuple[str, str, str]: A tuple containing directory path, filename, and
        extension.
    """
    path_obj: Path = Path(filepath)
    directory_path: str = str(path_obj.parent)
    if directory_path[-1] != "/":
        directory_path += "/"
    filename = os.path.splitext(path_obj.name)[0]
    extension = path_obj.suffix

    the_file: Mod_file = Mod_file(
        filedir=directory_path, filename=filename, extension=extension
    )

    return the_file


@typechecked
def get_py_filenames(
    extension: str, folder_path: str, exclude_start: str
) -> List[str]:
    """Get a list of files with the specified extension in a folder, excluding
    those starting with the specified prefix.

    Args:
        extension (str): The desired file extension (e.g., '.py').
        folder_path (str): The path to the folder containing the files.
        exclude_start (str): The prefix to exclude from file names.

    Returns:
        list: A list of files with the specified extension in the folder that
          do not start with the specified prefix.
    """
    files = []
    for file in os.listdir(folder_path):
        if file.endswith(extension) and not file.startswith(exclude_start):
            filename_without_extension = os.path.splitext(file)[0]
            files.append(filename_without_extension)
    return files


@typechecked
def load_file_content(
    filepath: str,
) -> Union[str, Dict]:  # type: ignore[type-arg]
    """Load the content of a file into a single string.

    Args:
        filepath (str): The path to the file to be loaded.

    Returns:
        str: The content of the file as a single string.

    Raises:
        FileNotFoundError: If the specified filepath does not exist.
        IOError: If there's an error reading the file.
    """
    with open(filepath, encoding="utf-8") as file:
        content = file.read()
    return content


@typechecked
def write_dict_to_json(
    *, data: Dict, filepath: str  # type: ignore[type-arg]
) -> None:
    """Write a dictionary to a JSON file.

    Args:
        data (Dict[str, Any]): The dictionary to be written.
        filename (str): The name of the JSON file to create or overwrite.
    """
    with open(filepath, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)


@typechecked
def load_dict_from_json(
    filename: str,
) -> JsonContentType:
    """Load a dictionary from a JSON file.

    Args:
        filename (str): The name of the JSON file to read from.

    Returns:
        Dict[str, Any]: The dictionary loaded from the JSON file.
    """
    with open(filename, encoding="utf-8") as json_file:
        data: JsonContentType = json.load(json_file)
    return data


@typechecked
def format_python_file(filepath: str) -> None:
    """Format a Python file using the Black code formatter.

    Args:
        filepath (str): Path to the Python file.
    """
    # TODO: verify black formatting was successful.
    subprocess.run(
        ["black", filepath],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )  # nosec


@typechecked
def get_file_content(filepath: str) -> str:
    """Get the content of the specified file.

    Args:
        filepath (str): Path to the Python file.

    Returns:
        str: Content of the file if found. Raises error otherwise.
    """
    if os.path.exists(filepath):
        with open(filepath, encoding="utf-8") as file:
            content = file.read()
        return content
    raise FileNotFoundError(f"File '{filepath}' not found.")


@typechecked
def set_file_content(filepath: str, content: str) -> None:
    """Set the content of the specified file.

    Args:
        filepath (str): Path to the Python file.
        content (str): Content to write into the file.
    """
    some_file: Mod_file = split_filepath(filepath=filepath)

    if os.path.exists(filepath):
        raise FileExistsError(f"File '{filepath}' already exists.")
    create_relative_path(relative_path=some_file.filedir)

    with open(filepath, "w", encoding="utf-8") as file:
        # file.write(content)
        file.write(content)


def create_relative_path(*, relative_path: str) -> None:
    """Creates a relative path if it does not yet exist.

    Args:
        relative_path (str): Relative path to create.

    Returns:
        None
    """
    if not os.path.exists(relative_path):
        os.makedirs(relative_path)
    if not os.path.exists(relative_path):
        raise NotADirectoryError(f"Error, did not find:{relative_path}")


@typechecked
def delete_file_if_exists(filepath: str) -> None:
    """Delete a file if it exists.

    :param filepath: The path to the file to be deleted.
    :type filepath: str
    """
    if os.path.exists(filepath):
        os.remove(filepath)


@typechecked
def load_config(
    config_filepath: str, coms: "Llm_and_coms"
) -> Dict[str, Dict[str, str]]:
    """Loads configuration file with ChatGPT/engine login from file."""
    if not os.path.exists(config_filepath):
        raise FileExistsError(f"File '{config_filepath}' does not exist.")

    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(config_filepath)

    # Convert the configuration to a dictionary
    config_dict: Dict[str, Dict[str, str]] = {}
    for section in config.sections():
        if section == coms.engine:
            config_dict[str(section)] = {}
            for key, value in config.items(section):
                config_dict[section][str(key)] = str(value)

    return config_dict


@typechecked
def load_conversation_from_json(*, json_path: str) -> Gpt_conversation:
    """Loads a conversation from a json file.

    Args:
        json_path (str): The path to the json file containing the
        conversation.

    Returns:
        Gpt_conversation: The loaded conversation object.
    """

    conversation: Dict = load_json_file(  # type: ignore[type-arg]
        filepath=json_path
    )
    if not isinstance(conversation, str):
        messages: List[Gpt_message] = []
        for message in conversation["messages"]:
            messages.append(Gpt_message(**message))
        return Gpt_conversation(
            chat_uuid=conversation["chat_uuid"], messages=messages
        )
    raise TypeError(
        "Conversation is not a JSON file.:"
        f"{type(conversation)}, {conversation}"
    )


@typechecked
def load_json_file(*, filepath: str) -> Dict:  # type: ignore[type-arg]
    """Load a JSON file and return its contents as a dictionary.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        Dict: A dictionary containing the JSON data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.

    Example:
        >>> data = load_json_file("data.json")
    """
    print(f"loading:{filepath}")
    with open(filepath, encoding="utf-8") as json_file:
        data: Dict = json.load(json_file)  # type: ignore[type-arg]
        return data


@typechecked
def split_filepaths_into_files(
    *,
    some_filepaths: str,
) -> List[Mod_file]:
    """Splits a semicolon-separated string of file paths into individual
    Mod_file objects.

    Parameters:
        some_filepaths (str): A semicolon-separated string of file paths to
        be split.

    Returns:
        List[Mod_file]: A list of Mod_file objects, each corresponding to a
        file path from the input string.
    """
    file_objects: List[Mod_file] = []
    for some_filepath in some_filepaths.split(";"):
        file_objects.append(split_filepath(filepath=some_filepath))
    return file_objects
