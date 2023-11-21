"""Processes API arguments and performs the requested actions."""
from argparse import Namespace

from typeguard import typechecked

from jsonmodipy.Mod_file import Mod_file

from ..file_parsing import get_file_content
from ..get.clss import (
    get_class_code,
    get_class_docstring,
    get_class_test_file_code,
    get_class_test_names,
)
from ..get.file import get_class_names, get_file_docstring, get_function_names
from ..get.function import (
    get_function_docstring,
    get_function_src_code,
    get_function_test_file_code,
    get_function_test_names,
)


@typechecked
def process_api_args_get(*, args: Namespace, some_file: Mod_file) -> None:
    """Processes the get arguments and performs the requested actions."""
    process_api_args_get_file(args=args, some_file=some_file)
    process_api_args_get_function(args=args, some_file=some_file)
    process_api_args_get_class(args=args, some_file=some_file)


def process_api_args_get_file(*, args: Namespace, some_file: Mod_file) -> None:
    """Get file related information.

    If no function are specified, refer to file.
    """
    if args.get == "class_names" and not (args.func_location or args.clss):
        get_class_names(
            some_file=some_file,
        )
    elif args.get == "docstring" and not (args.func_location or args.clss):
        # Return empty string if docstring does not exist.
        get_file_docstring(
            some_file=some_file,
        )
    elif args.get == "func_names" and not (args.func_location or args.clss):
        get_function_names(
            some_file=some_file,
        )
    elif args.get == "json" and not (args.func_location or args.clss):
        raise NotImplementedError("Error, returning JSON not supported.")
    if args.get == "src_code" and not (args.func_location or args.clss):
        get_file_content(
            filepath=f"{some_file.filedir}{some_file.filename}.py"
        )
    elif args.get == "test_code" and not (args.func_location or args.clss):
        raise NotImplementedError(
            "Error, returning test files of all functions in a file is not"
            + " supported."
        )
    if args.get == "test_names" and args.func_location is None:
        raise NotImplementedError(
            "Error, returning test names of all test names of all function in"
            + " a file is not supported."
        )


def process_api_args_get_function(
    *, args: Namespace, some_file: Mod_file
) -> None:
    """Get function name related information."""
    if args.get == "class_names" and args.func_location is not None:
        raise NotImplementedError(
            "Error, you gave a function name and asked for class name."
        )
    if args.get == "docstring" and args.func_location is not None:
        # Return empty string if docstring does not exist.
        func_docstring: str = get_function_docstring(
            some_file=some_file,
            func_location=args.func_location,
        )
        print(func_docstring)
    elif args.get == "func_names" and args.func_location is not None:
        raise NotImplementedError(
            "Error, you gave a function name and asked for it."
        )
    elif args.get == "json" and args.func_location is not None:
        raise NotImplementedError("Error, cannot give json for a function.")
    elif args.get == "src_code" and args.func_location is not None:
        func_src_code: str = get_function_src_code(
            some_file=some_file,
            func_location=args.func_location,
        )
        print(func_src_code)
    elif args.get == "test_code" and args.func_location is not None:
        get_function_test_file_code(
            some_file=some_file,
            func_name=args.func_location,
        )
    elif args.get == "test_names" and args.func_location is not None:
        get_function_test_names(
            some_file=some_file,
            func_name=args.func_location,
        )


def process_api_args_get_class(
    *, args: Namespace, some_file: Mod_file
) -> None:
    """Get class name related information."""
    if args.get == "class_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, you gave a class name and asked for class name."
        )
    if args.get == "docstring" and args.clss is not None:
        # Return empty string if docstring does not exist.
        print("TODO: Return docstring of the class in the file.")
        get_class_docstring(
            class_name=args.clss,
            some_file=some_file,
        )
    elif args.get == "func_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, you gave a class name and asked for it."
        )
    if args.get == "json" and args.clss is not None:
        raise NotImplementedError("Error, returning JSON not supported.")
    if args.get == "src_code" and args.clss is not None:
        print("TODO: Return Python code of the class in the file.")
        get_class_code(
            class_name=args.clss,
            some_file=some_file,
        )
    elif args.get == "test_code" and args.clss is not None:
        print("TODO: Return python test file of the class in the file.")
        get_class_test_file_code(
            class_name=args.clss,
            some_file=some_file,
        )
    elif args.get == "test_names" and args.clss is not None:
        print("TODO: Return python test names of the class in the file.")
        get_class_test_names(
            class_name=args.clss,
            some_file=some_file,
        )
