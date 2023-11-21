"""Converts the output of gpt to a function docstring."""
from typing import List

from typeguard import typechecked

from jsonmodipy.gpt_output.verify_func_docstr import get_gpt_func_args
from jsonmodipy.PythonStructures import ArgStorage


@typechecked
def convert_gpt_output_to_function_docstring(
    *,
    gpt_output: str,
) -> str:
    """Converts the output of gpt to a function docstring."""
    gpt_docstr_args: List[ArgStorage] = get_gpt_func_args(msg=gpt_output)
    print(f"gpt_docstr_args={gpt_docstr_args}")
    return "TODO: return something."
