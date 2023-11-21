"""Stores a single message."""
from typing import Dict, List, Optional, Union

from typeguard import typechecked

from jsonmodipy.PythonStructures import ArgStorage


# pylint: disable=R0903
# pylint: disable=R0913
# pylint: disable=R0902
class Gpt_message:
    """Stores a single message in a conversation.

    Attributes:
        message (str): The content of the message.
        creator (str): Who wrote the message, gpt, or user.
    """

    @typechecked
    def __init__(
        self,
        creator: str,
        id_in_browser: int,
        message_str: str,
        parent_id_in_browser: Optional[int] = None,
        expected_args: Optional[List[ArgStorage]] = None,
        is_runnability: Optional[bool] = None,
        is_tests_pass: Optional[bool] = None,
        is_pre_commit_passes: Optional[bool] = None,
        is_compilability: Optional[bool] = None,
        is_completeness: Optional[bool] = None,
        is_applied: Optional[bool] = None,
    ):
        """Initializes a new Gpt_message object.

        Args:
            message (str): The content of the message.
            creator (str): Who wrote the message, gpt, or user.
        """

        self.expected_args: Union[None, List[ArgStorage]] = expected_args
        self.id_in_browser: int = id_in_browser

        self.message_str: str = message_str
        if creator in ["user", "chatgpt3.5"]:
            self.creator: str = creator
        else:
            raise ValueError(
                "Error, multiple chat participants not yet supported. Got:"
                + f"{creator}."
            )

        if parent_id_in_browser:
            self.parent_id_in_browser: Union[int, None] = parent_id_in_browser
        else:
            self.parent_id_in_browser = None

        if is_runnability is not None:
            self.is_runnability: bool = is_runnability
        if is_tests_pass is not None:
            self.is_tests_pass: bool = is_tests_pass

        if is_pre_commit_passes is not None:
            self.is_pre_commit_passes: bool = is_pre_commit_passes

        if is_compilability is not None:
            self.is_compilability: bool = is_compilability

        if is_completeness is not None:
            self.is_completeness: bool = is_completeness

        if is_applied is not None:
            self.is_applied: bool = is_applied

    @typechecked
    def has_parent(self) -> bool:
        """Returns True if a parent_id_in_browser is stored in the Gpt_message,
        False otherwise."""
        if self.parent_id_in_browser:
            return True
        return False

    @typechecked
    def to_string(
        self,
    ) -> str:
        """Converts the conversation to a string."""
        message_str: str = f"creator={self.creator}\n"
        message_str += f"id_in_browser={self.id_in_browser}\n"
        if self.has_parent():
            message_str += (
                f"parent_id_in_browser={self.parent_id_in_browser}\n"
            )
        message_str += f"message_str={self.message_str}\n"

        return message_str

    @typechecked
    def to_json(
        self,
    ) -> Dict[str, Union[int, str, List[Dict[str, str]]]]:
        """Converts the conversation to a json dict."""
        message: Dict[str, Union[int, str, List[Dict[str, str]]]] = {}
        message["creator"] = self.creator
        message["id_in_browser"] = self.id_in_browser

        # Trivial isinstance for typechecking.
        if self.has_parent() and isinstance(self.parent_id_in_browser, int):
            message["parent_id_in_browser"] = self.parent_id_in_browser
        message["message_str"] = self.message_str

        if self.expected_args:
            some_list: List[Dict[str, str]] = []
            for arg in self.expected_args:
                some_list.append(arg.to_json_dict())
            if len(some_list) > 0:
                message["expected_args"] = some_list
        return message

    @typechecked
    def set_expected_args(
        self,
        expected_args: List[ArgStorage],
    ) -> None:
        """Stores the expected args that are assumed to belong to this message,
        into the object."""
        self.expected_args = expected_args
