"""Facilitates asking a question to ChatGPT through CLI."""
import re
from typing import Dict, List, Union

from typeguard import typechecked

from jsonmodipy.chatgpt35.conversations.Gpt_message import Gpt_message


# pylint: disable=R0903
class Gpt_conversation:
    """A class to represent a conversation with ChatGPT.

    Attributes:
        messages (List[str]): A sequence/chain of messages.
        chat_id: (str): A UUID used by ChatGPT to refer to a chat.
    """

    @typechecked
    def __init__(
        self,
        messages: List[Gpt_message],
        chat_uuid: str,
    ):
        """Initializes a new Gpt_conversation object.

        Args:
            messages (List[str]): A sequence/chain of messages.
        chat_id: (str): A UUID used by ChatGPT to refer to a chat.
        """
        verify_messages(messages)
        self.messages: List[Gpt_message] = messages
        self.chat_uuid: str = chat_uuid

    @typechecked
    def add_message(
        self,
        chat_uuid: str,
        new_msg: Gpt_message,
    ) -> None:
        """Adds a new message to the messages chain for this chat."""
        if self.chat_uuid != chat_uuid:
            raise ValueError(
                f"Error, expected chat_uuid:{self.chat_uuid}, got:{chat_uuid}"
            )
        assert_is_valid_uuid_format(uuid_str=chat_uuid)

        self.chat_uuid = chat_uuid
        self.messages.append(new_msg)
        verify_messages(messages=self.messages)

    @typechecked
    def to_string(
        self,
    ) -> str:
        """Converts the conversation to a string."""
        conversation_str: str = f"chat_uuid={self.chat_uuid}\n"
        for i, message in enumerate(self.messages):
            conversation_str += f"\n\ni={i}\n"
            conversation_str += message.to_string()

        return conversation_str

    @typechecked
    def to_json(
        self,
    ) -> Dict[
        str, Union[str, List[Dict[str, Union[int, str, List[Dict[str, str]]]]]]
    ]:
        """Converts the conversation to a string."""
        conversation: Dict[
            str,
            Union[str, List[Dict[str, Union[int, str, List[Dict[str, str]]]]]],
        ] = {}
        conversation["chat_uuid"] = self.chat_uuid
        messages: List[Dict[str, Union[int, str, List[Dict[str, str]]]]] = []
        for message in self.messages:
            messages.append(message.to_json())

        conversation["messages"] = messages
        return conversation


@typechecked
def are_all_different(nums: List[int]) -> bool:
    """Returns True if the list elements are all unique, False otherwise."""
    return len(nums) == len(set(nums))


@typechecked
def verify_messages(messages: List[Gpt_message]) -> None:
    """Verifies the messages are a valid sequence. Raises an error if:

    - The first message has a parent_id_in_browser.
    - The id_in browser of the child does not refer to the id_in_browser
    of the parent.
    - A consecutive message does not have a parent_id_in_browser.
    - There is are two identical parent_id_in_browser values in a message
    sequence.
    """
    # Check if the first message has a parent_id_in_browser.
    if len(messages) > 0:
        if messages[0].has_parent():
            raise ValueError(
                "Error, the first message in a sequence/chat can not have "
                + "a parent."
            )

        # pylint: disable=C0200
        for i in range(0, len(messages)):
            if i > 0:
                # Checks whether all consecutive messages have a
                # parent_id_in_browser. (superfluous due to above check).
                if messages[i].parent_id_in_browser is None:
                    raise ValueError(
                        "Error, the consecutive messages after the first"
                        + "message, must have a parent_id_in_browser value"
                    )

            # Check if the id_in_browser of the child message refers to the
            # id_in_browser of the parent.
            if i + 1 < len(messages) and (
                messages[i].id_in_browser
                != messages[i + 1].parent_id_in_browser
            ):
                print(f"messages[i]={messages[i].message_str}")
                print(f"messages[i+1]={messages[i + 1].message_str}")
                raise ValueError(
                    "Error, the id_in_browser of the messages is not "
                    + f"consecutive for:{messages[i].id_in_browser} and:"
                    + f"{messages[i + 1].parent_id_in_browser}"
                )

        # Check there is are no two identical parent_id_in_browser values
        # in a message sequence.
        ids_in_browser: List[int] = list(
            map(lambda message: message.id_in_browser, messages)
        )
        if not are_all_different(nums=ids_in_browser):
            raise ValueError(
                "Error, the id_in_browser values for each message in a "
                + "chat should be unique."
            )


@typechecked
def assert_is_valid_uuid_format(*, uuid_str: str) -> None:
    """Throws error if the chatgpt35 chat uuid does not have a valid format."""
    if not is_valid_uuid_format(uuid_str=uuid_str):
        raise ValueError(
            "Error, expected a 32 char alphanumeric uuid (with dashes), "
            + f"got:{uuid_str}"
        )


@typechecked
def is_valid_uuid_format(*, uuid_str: str) -> bool:
    """Returns True if the uuid consists of 32 alphanumeric characters and
    dashes.

    False otherwise.
    """
    # Define a regular expression pattern for UUID format
    uuid_pattern = re.compile(r"^[0-9a-fA-F-]+$")

    # Remove dashes from the string and check its length
    non_dash_chars = uuid_str.replace("-", "")
    if len(non_dash_chars) == 32:
        # Verify if the string matches the UUID pattern
        if uuid_pattern.match(uuid_str):
            return True

    return False
