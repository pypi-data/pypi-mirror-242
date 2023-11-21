"""Processes API arguments and performs the requested actions."""
from argparse import Namespace
from typing import Union

from typeguard import typechecked

from jsonmodipy.file_parsing import split_filepath
from jsonmodipy.Mod_file import Mod_file

from ..apply.clss import (
    apply_class_docstring_json_to_py,
    apply_class_json_to_py,
    apply_test_code_json_for_class_to_py,
)
from ..apply.file import (
    apply_file_docstring_json_to_py,
    apply_file_json_to_py,
    apply_test_code_json_for_file_to_py,
)
from ..apply.function import (
    apply_function_docstring_json_to_py,
    apply_function_json_to_py,
    apply_test_code_json_for_function_to_py,
)


@typechecked
def process_api_args_apply(*, args: Namespace, some_file: Mod_file) -> None:
    """Processes the gen arguments and performs the requested actions."""
    output_file: Union[None, Mod_file]
    if args.apply_to_filepath:
        output_file = split_filepath(filepath=args.apply_to_filepath)
    else:
        output_file = None

    process_api_args_apply_file(
        args=args,
        some_file=some_file,
    )
    process_api_args_apply_function(
        args=args,
        some_file=some_file,
        output_file=output_file,
    )
    process_api_args_apply_class(
        args=args,
        some_file=some_file,
        class_name=args.clss,
    )


def process_api_args_apply_file(
    *, args: Namespace, some_file: Mod_file
) -> None:
    """Apply file related generation actions.

    If no function are specified, refer to file.
    """
    if args.apply == "class_names" and not (args.func_location or args.clss):
        raise NotImplementedError("Error, will not apply class_names")
    if args.apply == "docstring" and not (args.func_location or args.clss):
        apply_file_docstring_json_to_py(
            some_file=some_file,
            iteration=args.iteration,
        )
    elif args.apply == "func_names" and not (args.func_location or args.clss):
        raise NotImplementedError("Error, will not apply func_names")
    if args.apply == "json" and not (args.func_location or args.clss):
        raise NotImplementedError(
            "Error, the thing that is applied, is a json, so will not apply a "
            + "json to a json."
        )
    if args.apply == "src_code" and not (args.func_location or args.clss):
        apply_file_json_to_py(
            some_file=some_file,
            iteration=args.iteration,
        )
    elif args.apply == "test_code" and not (args.func_location or args.clss):
        apply_test_code_json_for_file_to_py(
            some_file=some_file,
            iteration=args.iteration,
            test_dir=args.test_dir,
        )
    elif args.apply == "test_names" and not (args.func_location or args.clss):
        raise NotImplementedError("Error, will not apply test_names")


def process_api_args_apply_function(
    *, args: Namespace, some_file: Mod_file, output_file: Union[None, Mod_file]
) -> None:
    """Apply function name related generation actions."""

    if args.apply == "class_names" and args.func_location is not None:
        raise NotImplementedError(
            "Error, will not apply class_names for function."
        )
    if args.apply == "docstring" and args.func_location is not None:
        apply_function_docstring_json_to_py(
            some_file=some_file,
            func_location=args.func_location,
            iteration=int(args.iteration),
            output_file=output_file,
        )
    elif args.apply == "func_names" and args.func_location is not None:
        raise NotImplementedError(
            "Error, will not apply func_names for function"
        )
    if args.apply == "json" and args.func_location is not None:
        raise NotImplementedError(
            "Error, the thing that is applied, is a json, so will not apply a "
            + "json to a json."
        )
    if args.apply == "src_code" and args.func_location is not None:
        apply_function_json_to_py(
            some_file=some_file,
            func_location=args.func_location,
            iteration=args.iteration,
        )
    elif args.apply == "test_code" and args.func_location is not None:
        apply_test_code_json_for_function_to_py(
            some_file=some_file,
            func_location=args.func_location,
            iteration=args.iteration,
            test_dir=args.test_dir,
        )
    elif args.apply == "test_names" and args.func_location is not None:
        raise NotImplementedError(
            "Error, will not apply test_names for function."
        )


def process_api_args_apply_class(
    *,
    args: Namespace,
    some_file: Mod_file,
    class_name: str,
) -> None:
    """Apply class name related generation actions."""
    if args.apply == "class_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, will not apply class_names for class."
        )
    if args.apply == "docstring" and args.clss is not None:
        print("TODO: Apply docstring in class in Python file based on Json.")
        apply_class_docstring_json_to_py(
            class_name=class_name,
            some_file=some_file,
            iteration=args.iteration,
        )
    elif args.apply == "func_names" and args.clss is not None:
        raise NotImplementedError("Error, will not apply func_names for class")
    if args.apply == "json" and args.clss is not None:
        raise NotImplementedError(
            "Error, the thing that is applied, is a json, so will not apply a "
            + "json to a json."
        )
    if args.apply == "src_code" and args.clss is not None:
        apply_class_json_to_py(
            class_name=class_name,
            some_file=some_file,
            iteration=args.iteration,
        )
    elif args.apply == "test_code" and args.clss is not None:
        apply_test_code_json_for_class_to_py(
            class_name=class_name,
            some_file=some_file,
            iteration=args.iteration,
            test_dir=args.test_dir,
        )
    elif args.apply == "test_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, will not apply test_names for class."
        )
