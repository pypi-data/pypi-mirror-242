"""Handles the get commands for a function in a file."""

from typing import List, Optional, Tuple

from libcst import (
    Expr,
    FunctionDef,
    IndentedBlock,
    SimpleStatementLine,
    SimpleString,
)
from typeguard import typechecked

from jsonmodipy.PythonStructures import ArgStorage


# pylint: disable=R0903
class FatDocstring:
    """Stores the docstring of a Python file."""

    @typechecked
    def __init__(self, docstring: str, args: List[ArgStorage]):
        self.docstring: str = docstring
        self.args: List[ArgStorage] = args

    @typechecked
    def is_equal(
        self, other: "FatDocstring", verbose: Optional[bool] = False
    ) -> bool:
        """Check if two FatDocstring instances are equal."""
        if self.docstring != other.docstring:
            return False
        return self.has_equal_args(other_args=other.args, verbose=verbose)

    @typechecked
    def has_equal_args(
        self, other_args: List[ArgStorage], verbose: Optional[bool] = False
    ) -> bool:
        """Check if two FatDocstring instances are equal."""
        if len(self.args) != len(other_args):
            if verbose:
                print("len")
            return False
        for i, arg in enumerate(self.args):
            if arg.to_json_dict() != other_args[i].to_json_dict():
                if verbose:
                    print(f"arg={arg.to_json_dict()}")
                    print(f"other_args[i]={other_args[i].to_json_dict()}")
                return False
        return True

    @typechecked
    def to_unindented_string(
        self,
    ) -> str:
        """Converts the FatDocstring to a string."""
        args: str = ""
        for arg in self.args:
            args += f"{arg.to_python_docstring()}\n"
        return f"{self.docstring}\n{args}"


@typechecked
def get_docstring_from_function_node(*, py_func_node: FunctionDef) -> str:
    """Get the docstring node from the function node."""
    # We start by checking if the body of the function node is well structured.
    if isinstance(py_func_node.body, IndentedBlock):
        func_body: IndentedBlock = py_func_node.body

        # Within the function's body, we want to look at the lines of code.
        if isinstance(func_body.body, tuple):
            func_code_lines: Tuple = func_body.body  # type: ignore[type-arg]

            # We focus on the first line of code in the function
            if isinstance(func_code_lines[0], SimpleStatementLine):
                first_func_code_line = func_code_lines[0]

                # On this line, we are interested in the first element.
                if isinstance(first_func_code_line.body[0], Expr):
                    expr_node = first_func_code_line.body[0]

                    # Within this expression, we're checking if there's a
                    # string value.
                    if isinstance(expr_node.value, SimpleString):
                        # If we find a string, it means we've likely found the
                        #  docstring and we return its value.
                        return str(expr_node.value.value)

    # If no docstring is found through these checks, we return an empty string
    return ""
