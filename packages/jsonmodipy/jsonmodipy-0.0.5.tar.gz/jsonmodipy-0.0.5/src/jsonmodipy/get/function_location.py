"""Operations related to the location of a function within a file.

E.g. .class.MyClass.function.my_function
"""

from typing import Any, Type, Union

from libcst import ClassDef, FunctionDef
from typeguard import typechecked


@typechecked
def get_function_from_location(
    *, remaining_func_location: str, module: Any
) -> Union[None, FunctionDef]:
    """Returns a FunctionDef node from a Python file.

    Verifies it it exists in a particular nested location, e.g.
    .class.MyClass.function.my_function.
    """
    func_name: str = remaining_func_location.split(".")[-1]
    # Check the leading elements in the module whether they are the expected
    # function.
    if isinstance(module, tuple):
        for element in module:
            result = get_function_from_location(
                remaining_func_location=remaining_func_location,
                module=element,
            )
            if result:
                return result

    if hasattr(module, "body"):
        for assignment in module.body:
            if (
                isinstance(assignment, FunctionDef)
                and assignment.name.value == func_name
            ):
                # Assert the remaining path is directly towards the function.
                # If this is not the case, it is a duplicate function in a
                # different location.
                # TODO: write test for this case.
                if remaining_func_location != f".function.{func_name}":
                    raise ValueError(
                        f"Expected remaining_func_location to be .function"
                        f".{func_name}, got: {remaining_func_location}"
                    )
                return assignment

            next_expected_type: Union[
                Type[FunctionDef], Type[ClassDef]
            ] = get_next_expected_type(func_location=remaining_func_location)
            if isinstance(
                assignment,
                next_expected_type,
            ):
                expected_next_name: str = get_next_expected_name(
                    func_location=remaining_func_location,
                    next_expected_type=next_expected_type,
                )

                if expected_next_name == assignment.name.value:
                    remaining_func_location = eat_leading_location(
                        obj_type=next_expected_type,
                        obj_name=expected_next_name,
                        func_location=remaining_func_location,
                    )
                    result = get_function_from_location(
                        remaining_func_location=remaining_func_location,
                        module=assignment.body,
                    )
                    if result:
                        return result
    return None


@typechecked
def get_next_expected_type(
    *,
    func_location: str,
) -> Union[Type[FunctionDef], Type[ClassDef]]:
    """Returns the type that is expected next in the function location.

    E.g. for:
     .class.MyClass.function.my_function it returns ClassDef
    for:
    .function.my_function it returns FunctionDef
    """

    if func_location.split(".")[0] != "" or func_location[0] != ".":
        raise ValueError(
            "Error, expected the function location to start with a dot."
        )
    start_type = func_location.split(".")[1]
    if start_type == "class":
        return ClassDef  # type: ignore[no-any-return]
    if start_type == "function":
        return FunctionDef  # type: ignore[no-any-return]
    raise ValueError(
        f"Expected .function. or .class. at start, got {start_type} in:"
        + f" {func_location}"
    )


@typechecked
def get_next_expected_name(
    *,
    func_location: str,
    next_expected_type: Union[Type[FunctionDef], Type[ClassDef]],
) -> str:
    """Returns the name of the function or class that is expected next in the
    function location.

    E.g. for:
     .class.MyClass.function.my_function it returns MyClass
    for:
    .function.my_function it returns my_function
    """

    if func_location.split(".")[0] != "" or func_location[0] != ".":
        raise ValueError(
            "Error, expected the function location to start with a dot."
        )
    start_type = func_location.split(".")[1]
    if isinstance(next_expected_type, ClassDef) and start_type != "class":
        raise ValueError(
            f"Expected {next_expected_type} at start, got {start_type} in:"
            + f" {func_location}"
        )
    if (
        isinstance(next_expected_type, FunctionDef)
        and start_type != "function"
    ):
        raise ValueError(
            f"Expected {next_expected_type} at start, got {start_type} in:"
            + f" {func_location}"
        )
    return func_location.split(".")[2]


@typechecked
def eat_leading_location(
    *,
    obj_type: Union[Type[FunctionDef], Type[ClassDef]],
    obj_name: str,
    func_location: str,
) -> str:
    """Removes the leading .<obj_type>.<obj_name> from the function
    location."""
    obj_type_lead: str
    if obj_type == ClassDef:
        obj_type_lead = "class"
    elif obj_type == FunctionDef:
        obj_type_lead = "function"
    else:
        raise ValueError(
            f"Expected function or class, got:{obj_type} in:"
            + f" {func_location}"
        )

    expected_lead: str = f".{obj_type_lead}.{obj_name}"
    len_expected_lead = len(expected_lead)
    if func_location[:len_expected_lead] != expected_lead:
        raise ValueError(
            f"Expected {expected_lead} at start, got "
            f"{func_location[:len_expected_lead]} in:{func_location}"
        )
    return func_location[len_expected_lead:]
