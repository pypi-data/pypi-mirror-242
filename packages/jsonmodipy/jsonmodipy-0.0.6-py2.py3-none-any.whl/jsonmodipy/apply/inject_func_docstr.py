"""This is an MWE that replaces the documentation string of a function using
libcst."""
import ast
from typing import List

import libcst as cst
from libcst import (
    Expr,
    FunctionDef,
    MaybeSentinel,
    Newline,
    SimpleStatementLine,
    SimpleString,
    SimpleWhitespace,
    TrailingWhitespace,
)
from typeguard import typechecked


# pylint: disable=R0903
class ImportFixer(cst.CSTTransformer):  # type:ignore[misc]
    """This is an object that is used to replace the docstring of a
    function."""

    @typechecked
    def __init__(
        self,
        func_name: str,
        new_indented_docstring: str,
        indentation: int,
    ):
        self.func_name = func_name
        self.new_indented_docstring = new_indented_docstring
        self.indentation = indentation

    def leave_FunctionDef(
        self, original_node: FunctionDef, updated_node: FunctionDef
    ) -> FunctionDef:
        """Replace the docstring of the specified function with a new
        docstring."""

        if original_node.name.value == self.func_name:
            # Create a new expression node with the new docstring
            body_of_simplestring = [
                Expr(
                    value=SimpleString(
                        # value=self.new_indented_docstring,
                        value=self.new_indented_docstring,
                        lpar=[],
                        rpar=[],
                    ),
                    semicolon=MaybeSentinel.DEFAULT,
                ),
            ]

            if original_node.get_docstring() is None:
                # Prepend docstring instead of replacing it.
                new_docstr: SimpleStatementLine = SimpleStatementLine(
                    body=body_of_simplestring,
                    leading_lines=[],
                    trailing_whitespace=TrailingWhitespace(
                        whitespace=SimpleWhitespace(
                            value="",
                        ),
                        comment=None,
                        newline=Newline(
                            value=None,
                        ),
                    ),
                )
                remainder = original_node.body.body
                updated_body = original_node.body.with_changes(
                    body=(new_docstr,) + remainder
                )
            else:
                simplestatementline: SimpleStatementLine = (
                    original_node.body.body[0]
                )
                remainder = original_node.body.body[1:]

                updated_expr_node = simplestatementline.with_changes(
                    body=body_of_simplestring
                )

                # Update the body with the updated expression node and the
                # remainder.
                updated_body = original_node.body.with_changes(
                    body=[updated_expr_node] + list(remainder)
                )

            # Update the original_node with the updated body
            updated_node = updated_node.with_changes(body=updated_body)

        return updated_node


@typechecked
def add_indentation_to_docstring(*, docstring: str, indentation: int) -> str:
    """Add indentation to each line in a docstring.

    Args:
        docstring (str): The input docstring to which indentation will be
        added.
        indentation (int): The number of spaces to add as indentation.

    Returns:
        str: The updated docstring with indentation added.
    """
    lines = docstring.split("\n")
    indented_lines: List[str] = [lines[0]]
    for line in lines[1:]:
        if line != "":
            indented_lines.append(" " * indentation + line)
        else:
            indented_lines.append("")
    return "\n".join(indented_lines)


@typechecked
def get_indent(*, src_code: str, node: ast.FunctionDef) -> int:
    """Returns the indentation of a node in a Python AST."""
    lineno, _ = node.lineno, node.col_offset
    lines = src_code.split("\n")
    return len(lines[lineno - 1]) - len(lines[lineno - 1].lstrip())


@typechecked
def get_function_indentation(*, src_code: str, func_name: str) -> int:
    """Get the indentation levels of functions in a Python source code string.

    Args:
        src_code (str): Python source code as a string.

    Returns:
        List[tuple]: A list of tuples containing function names and their
        indentation levels.
    """
    # Parse the source code into an AST
    tree = ast.parse(src_code)

    # Traverse the AST to find functions and their indentation levels
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name == func_name:
                return get_indent(src_code=src_code, node=node)
    raise ValueError(f"Error, did not find function:{func_name}.")


@typechecked
def inject_docstr_into_func(
    *,
    original_src: str,
    func_location: str,
    unindented_new_docstr: str,
    indentation_level: int,
) -> str:
    """Inject a new docstring into a function in a Python source code
    string."""
    # TODO: Assert function occurs only once in source code.

    source_tree = cst.parse_module(original_src)
    func_indentation: int = get_function_indentation(
        src_code=original_src, func_name=func_location.split(".")[-1]
    )
    print(f"func_indentation={func_indentation}.")
    new_indented_docstring: str = add_indentation_to_docstring(
        docstring=unindented_new_docstr,
        indentation=func_indentation + indentation_level,
    )
    print(f"new_indented_docstring={new_indented_docstring}.")
    # TODO: change this to make the import fixer change functions at location
    # instead of at name.
    transformer = ImportFixer(
        func_name=func_location.split(".")[-1],
        new_indented_docstring=new_indented_docstring,
        indentation=func_indentation,
    )

    modified_tree = source_tree.visit(transformer)
    return str(modified_tree.code)
