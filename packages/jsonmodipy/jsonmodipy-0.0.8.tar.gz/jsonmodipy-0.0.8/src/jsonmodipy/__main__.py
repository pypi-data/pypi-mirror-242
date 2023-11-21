"""Entry point for the project."""


from typing import Dict

from jsonmodipy.arg_parser.process_args_engine import (
    Llm_and_coms,
    process_api_args_engine,
)
from jsonmodipy.arg_parser.process_args_set import process_api_args_set
from jsonmodipy.Mod_file import Mod_file

from .arg_parser.arg_values_checks import args_values_check
from .arg_parser.parse_args import parse_api_args
from .arg_parser.process_args_apply import process_api_args_apply
from .arg_parser.process_args_ask import process_api_args_ask
from .arg_parser.process_args_get import process_api_args_get
from .file_parsing import split_filepath

api_args = parse_api_args()
args_values_check(args=api_args)
# Get filepath and file name.

if api_args.filepath is not None:
    some_file: Mod_file = split_filepath(filepath=api_args.filepath)

    process_api_args_get(args=api_args, some_file=some_file)
    process_api_args_apply(args=api_args, some_file=some_file)
    config: Dict[str, Dict[str, str]]
    coms: Llm_and_coms
    coms, config = process_api_args_engine(args=api_args)
    process_api_args_ask(
        args=api_args, coms=coms, config=config, some_file=some_file
    )

process_api_args_set(args=api_args)
