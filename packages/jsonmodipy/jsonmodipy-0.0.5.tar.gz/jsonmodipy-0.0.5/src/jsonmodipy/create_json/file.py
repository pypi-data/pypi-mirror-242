"""Creates a .json backup of a .py file if it exists and is not yet backed
up."""
from typeguard import typechecked


@typechecked
def create_file_backup_json(filepath: str) -> None:
    """
    0. Verifies the target file exists.
    1. Verifies the target code is of valid Python syntax.
    2. Gets the latests backup number for that segment.
    3. Then it checks whether the backup for that segment would be a unique
    json. If it is unique:
        3.a it creates a new backup for that segment (with an updated backup
        nr.).
    """
    print(filepath)


@typechecked
def generate_json_from_py_file(
    *,
    filedir: str,
    filename: str,
    func_name: str,
    iteration: int,
) -> str:
    """
    0. Verifies the <filedir>/<filename>.py file has a valid Python syntax.
    1. Makes the a json of the file named:
    <filedir>/<filename>_<iteration>.json
    2. Applies black formatting to the Json.
    3. Verifies the <filedir>/<filename>_func_<file>_<iteration>.json can
     be applied to/injected in a json of the <filedir>/<filename>.py.
    4. Verifies the restored .py file from the modified json of the
    <filedir>/<filename>.py file has identical content to the original .py
    file.
    """
    print("TODO: Generate Json code from file in code of Python file.")
    # pylint: disable=R0801
    print(filedir)
    print(filename)
    print(func_name)
    print(iteration)
    return "TODO"
