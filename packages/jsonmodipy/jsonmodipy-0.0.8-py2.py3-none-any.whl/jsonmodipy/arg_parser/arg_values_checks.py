"""Processes API arguments and performs the requested actions."""
from argparse import Namespace

from typeguard import typechecked


@typechecked
def args_values_check(*, args: Namespace) -> None:
    """Processes the arguments and performs the requested actions."""
    if args.func_location is not None:
        function_start: str = ".function."
        class_start: str = ".class."
        if args.func_location[: len(function_start)] != function_start and (
            args.func_location[: len(class_start)] != class_start
        ):
            raise NotImplementedError(
                f"Raw function name provided:{args.func_location}."
            )

    if args.get or args.apply:
        if not args.filepath and not args.filepaths:
            raise ValueError(
                "--filepath or filepaths is required when any action is "
                + "specified."
            )

        # pylint: disable=R0801
        if args.get is not None and args.get not in [
            "class_names",
            "docstring",
            "func_names",
            "json",
            "src_code",
            "test_code",
            "testnames",
        ]:
            raise ValueError(f"Invalid choice for --get action:{args.get}.")

        if args.apply is not None and args.apply not in [
            "docstring",
            "src_code",
            "test_code",
        ]:
            raise ValueError(
                "--function or --classes must be provided with --gen action."
            )
    else:
        if not args.filepath and not args.filepaths:
            raise ValueError("--filepath or --filepaths is required.")
