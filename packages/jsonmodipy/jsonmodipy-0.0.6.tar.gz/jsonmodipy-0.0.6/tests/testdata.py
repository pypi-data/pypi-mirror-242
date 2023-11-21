"""File with hardcoded test data."""

from jsonmodipy.chatgpt35.conversations.Conversation import Gpt_conversation
from jsonmodipy.chatgpt35.conversations.Gpt_message import Gpt_message


def create_dummy_conversation_func_docstr() -> Gpt_conversation:
    """Creates a dummy conversation from ChatGPT output for the question: write
    a docstring for the add_two function in file adder.py."""
    user_question: Gpt_message = Gpt_message(
        creator="user",
        id_in_browser=2,
        message_str="This is a question",
        parent_id_in_browser=None,
    )

    gpt_response: Gpt_message = Gpt_message(
        creator="chatgpt3.5",
        id_in_browser=3,
        message_str="""
|Start-response|
|Docstring-core|
Adds an integer value to an incoming number.
|End-Docstring-core|
|Arg1-name|
x
|Arg1-type|
int
|Arg1-description|
The incoming number to which the integer value will be added.
|End-Arg1-description|
|Return-type|
int
|Return-description|
The result of adding 2 to the incoming number.
|End-Return-description|
|End-response|""",
        parent_id_in_browser=2,
    )

    return Gpt_conversation(
        messages=[user_question, gpt_response],
        chat_uuid="1234567890-1234567890-1234567890-ab",
    )
