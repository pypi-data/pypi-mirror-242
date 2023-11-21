"""Contains the supported Python objects that store the content of a Python
file in strings."""
import re
from typing import Dict, List, Optional, Union

from typeguard import typechecked

TypeStorageType = str


# pylint: disable=R0903
class TypeStorage:
    """Stores a Type."""

    @typechecked
    def __init__(
        self,
        the_type: Union[type, str],
    ):
        self.the_type: str
        if isinstance(the_type, str):
            self.the_type = the_type
        elif isinstance(the_type, type):
            self.the_type = type_to_string(the_type)
        else:
            raise TypeError(
                f"Error, expected type or string. Got:{type(the_type)}"
            )

    @typechecked
    def to_string(self) -> str:
        """Convert the TypeStorage object to a dictionary representation.

        :return: The dictionary representation of the ArgStorage object.
        :rtype: dict
        """
        return self.the_type


ArgStorageType = Dict[str, str]


# pylint: disable=R0903
class ArgStorage:
    """Stores a Python argument, containing the name of the argument, and its
    type."""

    @typechecked
    def __init__(
        self,
        name: str,
        arg_type: Optional[TypeStorage] = None,
        description: Optional[str] = None,
    ):
        self.name: str = name
        self.arg_type: Union[None, TypeStorage]
        if arg_type is None:
            self.arg_type = None
        elif isinstance(arg_type, TypeStorage):
            self.arg_type = arg_type
        else:
            raise TypeError("Error, expected a TypeStorage object, not str.")
        if description is not None:
            self.description: Union[None, str] = description
        else:
            self.description = None

    @typechecked
    def has_type(self) -> bool:
        """Returns True if the ArgStorage contains a type stored as TypeStorage
        in self.arg_type, returns False otherwise."""
        if self.arg_type is None:
            return False
        if isinstance(self.arg_type, TypeStorage):
            return True
        raise TypeError("Error, expected a TypeStorage object, not str.")

    @typechecked
    def has_description(self) -> bool:
        """Returns True if the ArgStorage contains a description stored as
        string in self.arg_description, returns False otherwise."""
        if self.description is None:
            return False
        if isinstance(self.description, str):
            return True
        raise TypeError("Error, expected a TypeStorage object, not str.")

    @typechecked
    def to_json_dict(self) -> ArgStorageType:
        """Convert the ArgStorage object to a dictionary representation.

        :return: The dictionary representation of the ArgStorage object.
        :rtype: dict
        """
        if self.arg_type is None:
            return {"name": self.name}
        return {"arg_type": self.arg_type.to_string(), "name": self.name}

    @typechecked
    def to_python_string(
        self,
    ) -> str:
        """Convert the argument object back into a string of Python code.

        :return: The code as a string of Python code.
        :rtype: str
        """
        if self.arg_type is None:
            return f"{self.name},"
        return f"{self.name}: {self.arg_type.the_type}, "

    @typechecked
    def to_python_docstring(
        self,
    ) -> str:
        """Convert the argument object back into a string of Python code.

        :return: The code as a string of Python code.
        :rtype: str
        """
        start: str
        if self.arg_type is None:
            start = f":{self.name}: "
        else:
            start = f":{self.name}: ({self.arg_type.the_type}), "
        if self.has_description():
            return f"{start} {self.description}"
        return f"{start}:"


DocstringType = Dict[str, str]


class Docstring:
    """Stores the docstring of a Python file."""

    @typechecked
    def __init__(
        self,
        docstring: str,
    ):
        self.docstring: str = docstring

    @typechecked
    def to_json_dict(self) -> DocstringType:
        """Convert the Docstring object to a dictionary representation.

        :return: The dictionary representation of the Docstring object.
        :rtype: dict
        """
        return {"docstring": self.docstring}

    @typechecked
    def to_python_string(self) -> str:
        """Convert the Docstring object back into a string of Python code.

        :return: The Docstring of a file as a string of Python code.
        :rtype: str
        """
        return self.docstring


CodeStorageType = Dict[str, Union[str, int]]


class CodeStorage:
    """Stores Python code as string."""

    @typechecked
    def __init__(
        self,
        code_content: str,
        indentation: int,
    ):
        self.code_content: str = code_content.lstrip("\n").rstrip("\n")
        self.indentation: int = indentation

    @typechecked
    def to_json_dict(self) -> CodeStorageType:
        """Convert the CodeStorage object to a dictionary representation.

        :return: The dictionary representation of the CodeStorage
            object.
        :rtype: dict
        """
        return {
            "code_content": self.code_content,
            "indentation": self.indentation,
        }

    # pylint: disable=W0613
    @typechecked
    def to_python_string(self, ind_level: int) -> str:
        """Convert the code object back into a string of Python code.

        :return: The code as a string of Python code.
        :rtype: str
        """
        indentation_str: str = " " * self.indentation
        indented_code: str = apply_indentation(
            indentation=indentation_str, line_of_code=self.code_content
        )
        return indented_code


DocumentationStorageType = Dict[str, Union[str, int]]


class DocumentationStorage:
    """Stores Python code as string."""

    @typechecked
    def __init__(
        self,
        documentation_content: str,
        indentation: int,
    ):
        self.documentation_content: str = documentation_content
        self.indentation: int = indentation

    @typechecked
    def to_json_dict(self) -> DocumentationStorageType:
        """Convert the DocumentationStorage object to a dictionary
        representation.

        :return: The dictionary representation of the
            DocumentationStorage object.
        :rtype: dict
        """
        return {
            "documentation_content": self.documentation_content,
            "indentation": self.indentation,
        }

    # pylint: disable=W0613
    @typechecked
    def to_python_string(self, ind_level: int) -> str:
        """Convert the code object back into a string of Python code.

        :return: The code as a string of Python code.
        :rtype: str
        """
        # Include 4 spaces indentation.
        # indentation: str = " " * ind_level
        indentation: str = " " * self.indentation

        return f'{indentation}"""{self.documentation_content}"""'


MethodStorageType = Dict[
    str, Dict[str, Union[List, str]]  # type: ignore[type-arg]
]


class MethodsStorage:
    """Stores a Python methods, containing:

    1. Documentation of methods
    2. Name of arguments.
    3. Type of arguments.
    4. Return type of arguments.
    5. Child classes and methods.
    """

    # pylint: disable=R0913
    @typechecked
    def __init__(
        self,
        arguments: List[ArgStorage],
        children: List[
            Union[
                "ClassStorage",
                CodeStorage,
                DocumentationStorage,
                "MethodsStorage",
            ]
        ],
        documentation: str,
        name: str,
        returnType: TypeStorage,
    ):
        self.arguments: List[ArgStorage] = arguments
        self.documentation: str = documentation
        self.name: str = name
        self.returnType: TypeStorage = returnType

        self.children: List[
            Union[
                ClassStorage, CodeStorage, DocumentationStorage, MethodsStorage
            ]
        ] = children

    @typechecked
    def to_json_dict(
        self,
    ) -> MethodStorageType:
        """Convert the MethodsStorage object to a dictionary representation.

        :return: The dictionary representation of the MethodsStorage
            object.
        :rtype: dict
        """

        return {
            "method": {
                "arguments": [arg.to_json_dict() for arg in self.arguments],
                "children": [child.to_json_dict() for child in self.children],
                "documentation": self.documentation,
                "name": self.name,
                "returnType": self.returnType.the_type,
            }
        }

    @typechecked
    def to_python_string(self, ind_level: int) -> str:
        """Convert the method object back into a string of Python code.

        :return: The method object as a string of Python code.
        :rtype: str
        """
        arguments: str = " ".join(
            list(
                map(
                    lambda arg: arg.to_python_string(),
                    self.arguments,
                )
            )
        )
        # Remove trailing ", " if it exists.
        arguments = re.sub(r",\s*$", "", arguments)
        lines: List[str] = []

        # Include 4 spaces indentation.
        indentation: str = " " * ind_level

        # Include start of method.
        method_definition: str
        if self.returnType.the_type == "":
            method_definition = f"{indentation}def {self.name}({arguments}):"
        else:
            method_definition = (
                f"{indentation}def {self.name}({arguments}) -> "
                + f"{self.returnType.the_type}:"
            )
        lines.append(method_definition)
        for child in self.children:
            lines.append(child.to_python_string(ind_level=ind_level + 4))
        single_string = "\n".join(lines)
        return single_string


ClassStorageType = Dict[
    str, Dict[str, Union[List, str]]  # type: ignore[type-arg]
]


class ClassStorage:
    """Stores a Python class in strings, such that it can be exported to a JSON
    file.

    A class contains:
        1. Documentation of classes.
        2. Classes within classes.
        3. Arguments of classes:
            3.1. Name of arguments.
            3.2. Type of arguments.
        4. Methods within classes
            4.1. Documentation of methods
            4.2. Name of arguments.
            4.3. Type of arguments.
            4.4. Return type of arguments.
    """

    # pylint: disable=R0913
    @typechecked
    def __init__(
        self,
        documentation: str,
        name: str,
        arguments: List[ArgStorage],
        children: List[
            Union[
                "ClassStorage",
                CodeStorage,
                DocumentationStorage,
                MethodsStorage,
            ]
        ],
        returnType: TypeStorage,
    ):
        self.arguments: List[ArgStorage] = arguments

        self.children: List[
            Union[
                ClassStorage, CodeStorage, DocumentationStorage, MethodsStorage
            ]
        ] = children
        self.documentation: str = documentation
        self.name: str = name
        self.returnType: TypeStorage = returnType

    @typechecked
    def to_json_dict(
        self,
    ) -> ClassStorageType:
        """Convert the ClassStorage object to a dictionary representation.

        :return: The dictionary representation of the ClassStorage
            object.
        :rtype: dict
        """
        return {
            "class": {
                "arguments": [arg.to_json_dict() for arg in self.arguments],
                "children": [child.to_json_dict() for child in self.children],
                "documentation": self.documentation,
                "name": self.name,
                "returnType": self.returnType.the_type,
            }
        }

    @typechecked
    def to_python_string(self, ind_level: int) -> str:
        """Convert the class object back into a string of Python code.

        :return: The method object as a string of Python code.
        :rtype: str
        """
        # TODO: remove arguments because they are stored in the __init__ method
        lines: List[str] = []

        # Include 4 spaces indentation.
        indentation: str = " " * ind_level

        # Include start of method.
        lines.append(f"{indentation}class {self.name}:")
        lines.append(f"{indentation}    {self.documentation}")
        for child in self.children:
            lines.append(child.to_python_string(ind_level=ind_level + 4))
        single_string = "\n".join(lines)

        return single_string


JsonContentType = Dict[
    str,
    Union[
        str,  # For Docstring value.
        # pylint: disable=R0801
        List[
            Union[
                ClassStorageType,
                CodeStorageType,
                DocumentationStorageType,
                MethodStorageType,
            ]
        ],
    ],
]


# pylint: disable=R0903
class JsonContent:
    """Stores the content of a Python file as a structure that can be exported
    to a JSON file."""

    @typechecked
    def __init__(
        self,
        docstring: Docstring,
        code_elems: List[
            Union[
                ClassStorage,
                CodeStorage,
                DocumentationStorage,
                MethodsStorage,
            ]
        ],
    ):
        self.docstring: Docstring = docstring
        # pylint: disable=R0801
        self.code_elems: List[
            Union[
                ClassStorage,
                CodeStorage,
                DocumentationStorage,
                MethodsStorage,
            ]
        ] = code_elems

    @typechecked
    def to_dict(
        self,
    ) -> JsonContentType:
        """Convert the JsonContent object to a JSON string representation.

        :return: The JSON string representation of the JsonContent
            object.
        :rtype: str
        """
        data: JsonContentType = {
            "docstring": self.docstring.docstring,
            "code_elems": [elem.to_json_dict() for elem in self.code_elems],
        }
        return data

    @typechecked
    def to_python_string(self) -> str:
        """Convert the method object back into a string of Python code.

        :return: The method object as a string of Python code.
        :rtype: str
        """
        # TODO: remove arguments because they are stored in the __init__ method
        lines: List[str] = []

        # Include start of file with docstring.
        lines.append(f'"""{self.docstring.to_python_string()}"""')
        for child in self.code_elems:
            lines.append(child.to_python_string(ind_level=0))
        single_string = "\n".join(lines)

        return single_string


@typechecked
def type_to_string(some_type: type) -> str:
    """Converts a Type into the string that type has in Python code."""
    type_mapping = {
        int: "int",
        str: "str",
        float: "float",
        ArgStorage: "ArgStorage",
        ClassStorage: "ClassStorage",
        CodeStorage: "CodeStorage",
        JsonContent: "JsonContent",
        MethodsStorage: "MethodsStorage",
        List: "List",
        Dict: "Dict",
        type(None): "None",
    }

    # pylint: disable=C0201
    if some_type not in type_mapping.keys():
        raise KeyError(f"Error, type:{some_type} was not yet in type_mapping.")
    return type_mapping[some_type]


@typechecked
def apply_indentation(indentation: str, line_of_code: str) -> str:
    """Apply indentation after newline characters in the code.

    Args:
        indentation (str): The string to be used for indentation.
        code (str): The code string containing newline characters.

    Returns:
        str: The code string with indentation applied after newline characters.
    """
    # Split the code into individual lines using newline character as delimiter
    lines = line_of_code.split("\n")

    # Iterate through each line and apply indentation if necessary
    indented_lines = [
        indentation + line if line.strip() else line for line in lines
    ]

    # Join the indented lines back together using newline character
    indented_code = "\n".join(indented_lines)

    return indented_code
