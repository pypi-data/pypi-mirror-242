"""There are different types of function arguments.

This function retrieves them all from a piece of parsed python code that
is turned into libcst, using the libcst API.
"""

from typing import List, Union

from libcst import FunctionDef, Module, Param
from typeguard import typechecked

from jsonmodipy.PythonStructures import ArgStorage, TypeStorage


@typechecked
def get_func_args(*, py_func_node: FunctionDef) -> List[ArgStorage]:
    """Returns a list of argument names and their types (as tuple of two
    strings), from the incoming function."""

    args_list: List[ArgStorage] = []
    possible_arg_params: List[Param] = list(
        py_func_node.params.params
        + py_func_node.params.kwonly_params
        + py_func_node.params.posonly_params
    )
    for param in possible_arg_params:
        if isinstance(param, Param):
            arg_name = param.name.value
            arg_type: Union[None, str] = get_type_from_param(param=param)
            if arg_type is not None:
                new_arg: ArgStorage = ArgStorage(
                    name=arg_name,
                    arg_type=TypeStorage(the_type=arg_type),
                )
            else:
                new_arg = ArgStorage(name=arg_name)
        else:
            raise TypeError(f"Error, unexpected argument type:{type(param)}")
        args_list.append(new_arg)
    return args_list


def get_type_from_param(*, param: Param) -> Union[None, str]:
    """Returns the type from a libcst Param if it has one."""
    if param_has_type(param=param):
        # annotation = param.annotation
        return extract_type_from_annotation(param=param)
    return None


@typechecked
def param_has_type(*, param: Param) -> bool:
    """Returns True if the incoming param has a type annotation, False."""
    if isinstance(param, Param):
        if param.annotation is not None:
            return True
        return False
    raise TypeError(f"Error, unexpected argument type:{type(param)}")


@typechecked
def extract_type_from_annotation(
    *,
    param: Param,
) -> str:
    """Extract the type information from an annotation.

    Args:
        param Param: The parameter to extract the type from.

    Returns:
        str: The extracted type information.
    """
    parameter_text: str = Module([]).code_for_node(
        node=param,
    )

    # Remove any trailing spaces.
    parameter_text = parameter_text.strip()

    # Remove trailing commas if there are any.
    if parameter_text.endswith(","):
        parameter_text = parameter_text[:-1]

    # Split argument name and text into a list and get the type.
    the_type: str = parameter_text.split(":")[1].strip()

    return the_type
