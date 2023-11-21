"""Ask a question to chatgpt3.5 through the website interface."""

import hashlib
import random  # nosec
import time
from typing import List, Optional, Tuple

from browsercontroller.playwright.get_driver_with_persistent_context import (
    init_playwright_with_context,
    init_playwright_with_context_and_video,
)
from playwright.sync_api._generated import Locator, Page, Playwright, Video
from typeguard import typechecked

from jsonmodipy.chatgpt35.conversations.Conversation import Gpt_conversation
from jsonmodipy.chatgpt35.conversations.Gpt_message import Gpt_message
from jsonmodipy.chatgpt35.helper import (
    fill_in_question_input_form,
    get_chat_uuid_from_url,
    get_chatgpt_conversation,
    has_conversation_id,
)
from jsonmodipy.chatgpt35.login_chatgpt35 import ensure_chatgpt35_login
from jsonmodipy.Hardcoded import Hardcoded


@typechecked
def ask_chatgpt35(
    *,
    password: str,
    username: str,
    question: str,
    conversation: Optional[Gpt_conversation] = None,
    record_video: Optional[bool] = False,
) -> Gpt_conversation:
    """Asks a question to chatgpt3.5 and returns the accompanying chat."""
    playwright: Playwright
    page: Page
    video: Video

    # playwright, page = initialise_playwright_browsercontroller(
    # playwright, page = initialise_playwright_browsercontroller_with_cookies(
    if record_video:
        playwright, page, video = init_playwright_with_context_and_video(
            start_url="https://chat.openai.com/",
            browsertype="firefox",
            headless=False,
            stealthmode=True,
            user_data_dir=Hardcoded().user_data_dir,
        )

    else:
        playwright, page = init_playwright_with_context(
            start_url="https://chat.openai.com/",
            browsertype="firefox",
            headless=False,
            stealthmode=True,
            user_data_dir=Hardcoded().user_data_dir,
        )

    ensure_chatgpt35_login(page=page, password=password, username=username)
    if conversation is not None:
        go_to_chat(conversation=conversation, page=page)

    conversation = submit_question_chatgpt35(
        conversation=conversation,
        page=page,
        question=question,
    )
    parse_response_chatgpt35(
        conversation=conversation,
        page=page,
        question=question,
    )

    if record_video:
        # pprint(dir(video))
        # input("Saving video_path.")
        # video_path = video.path()
        # input("GOt video_path.")
        # video_path = video.stop()
        # page.close()
        # pprint(video_path)
        # pprint(dir(video_path))

        video.save_as(path="/home/name/Downloads/video.mp4")
        # input("Saved video")

    # TODO: return conversation.
    playwright.stop()
    return conversation


def go_to_chat(conversation: Gpt_conversation, page: Page) -> None:
    """Goes to a chatid of a pre-existing conversation."""

    chat_url: str = f"https://chat.openai.com/c/{conversation.chat_uuid}"
    page.goto(chat_url)
    time.sleep(random.randint(5000, 25000) / 1000.0)  # nosec

    # Verify url is valid.
    if page.url != chat_url:
        raise ValueError(
            f"Error, expected the url to be:\n{chat_url}, found:\n{page.url}"
        )

    # Verify chat uuid is valid.
    chat_uuid: str = get_chat_uuid_from_url(some_url=page.url)
    if chat_uuid != conversation.chat_uuid:
        raise ValueError(
            f"Error, expected the chat_uuid to be:\n{conversation.chat_uuid},"
            + f" found:\n{chat_uuid}"
        )
    # TODO: verify the previous conversations were found.


def submit_question_chatgpt35(
    *, page: Page, question: str, conversation: Optional[Gpt_conversation]
) -> Gpt_conversation:
    """Submits a question to chatgpt."""

    question_with_sha: str = inject_deterministic_question_sha_into_question(
        question=question
    )
    question_input_box: Locator = fill_in_question_input_form(
        page=page,
        text=question_with_sha,
    )
    question_input_box.press("Enter")

    time.sleep(random.randint(5000, 25000) / 1000.0)  # nosec
    if conversation is not None:
        new_parent_id: int = conversation.messages[-1].id_in_browser
        print("TODO: use the deterministc question sha to find the id.")
        # TODO: probably copy the code from the else statement.
        new_question: Gpt_message = Gpt_message(
            creator="user",
            id_in_browser=new_parent_id + 1,
            message_str=question,
            parent_id_in_browser=new_parent_id,
        )

        conversation.add_message(
            new_msg=new_question,
            chat_uuid=get_chat_uuid_from_url(some_url=page.url),
        )
    else:
        max_message_id_in_browser: int = get_max_message_id_in_browser(
            page=page
        )
        question_sha: str = get_deterministic_sha(string_to_hash=question)
        question_message_id_in_browser: int = (
            get_question_message_id_in_browser(
                page=page,
                max_message_id_in_browser=max_message_id_in_browser,
                question_sha=question_sha,
            )
        )
        gpt_message: Gpt_message = Gpt_message(
            creator="user",
            id_in_browser=question_message_id_in_browser,
            message_str=question,
            parent_id_in_browser=None,
        )

        conversation = Gpt_conversation(
            messages=[gpt_message],
            chat_uuid=get_chat_uuid_from_url(some_url=page.url),
        )
    return conversation


@typechecked
def inject_deterministic_question_sha_into_question(question: str) -> str:
    """Prepends the sha of the question into the question."""
    question_sha: str = get_deterministic_sha(string_to_hash=question)
    new_question: str = (
        "Ignore this question sha, it is for personal logging purposes:"
        + f"{question_sha}\n{question}"
    )
    new_question_sha: str = get_deterministic_sha(string_to_hash=new_question)
    if new_question_sha == question_sha:
        raise ValueError(
            "Error, after injecting sha into question, the new sha should "
            + "change."
        )
    return new_question


@typechecked
def get_deterministic_sha(string_to_hash: str) -> str:
    """Calculate a deterministic SHA-256 hash of a string.

    Args:
        string_to_hash (str): The input string to be hashed.

    Returns:
        str: The hexadecimal representation of the SHA-256 hash.

    Example:
        >>> input_string = "Hello, World!"
        >>> hashed_value = get_deterministic_sha(input_string)
        >>> print(hashed_value)
        'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146'
    """
    # Encode the string as bytes (UTF-8 encoding is commonly used)
    encoded_string = string_to_hash.encode("utf-8")

    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the encoded bytes
    sha256.update(encoded_string)

    # Get the hexadecimal representation of the hash
    hashed_string = sha256.hexdigest()

    return hashed_string


@typechecked
def get_question_message_id_in_browser(
    *, page: Page, max_message_id_in_browser: int, question_sha: str
) -> int:
    """Checks, at most, the last two found message id's and gets the message
    content of those ids.

    Then it adds the message_id_in_browser belonging to the message that
    has the sha of that question in it.
    """
    messages_to_check: List[Tuple[int, str]] = []
    if has_conversation_id(page=page, turn_nr=max_message_id_in_browser - 1):
        messages_to_check.append(
            (
                max_message_id_in_browser - 1,
                get_chatgpt_conversation(
                    page=page,
                    turn_nr=max_message_id_in_browser - 1,
                ),
            )
        )
    if has_conversation_id(page=page, turn_nr=max_message_id_in_browser):
        messages_to_check.append(
            (
                max_message_id_in_browser,
                get_chatgpt_conversation(
                    page=page,
                    turn_nr=max_message_id_in_browser,
                ),
            )
        )
    else:
        raise ValueError(
            "Error, expected a conversation for the max_message_id_in_browser."
        )
    if question_sha in messages_to_check[0][1]:
        return messages_to_check[0][0]
    if question_sha in messages_to_check[1][1]:
        return messages_to_check[1][0]
    raise ValueError("Error, expected to find question sha in message.")


@typechecked
def get_max_message_id_in_browser(*, page: Page) -> int:
    """Gets the chat message id (message_id_in_browser) from the browser."""
    i: int = 0
    for i in range(0, 10):
        if has_conversation_id(page=page, turn_nr=i):
            max_counter: int = i
            while has_conversation_id(page=page, turn_nr=max_counter + 1):
                max_counter += 1
            return max_counter
    raise ValueError("Error, did not find a conversation id for chatgpt3.5.")


@typechecked
def parse_response_chatgpt35(
    *, conversation: Gpt_conversation, page: Page, question: str
) -> None:
    """Retrieves the response by ChatGPT3.5 and adds it to the conversation."""
    max_message_id_in_browser: int = get_max_message_id_in_browser(page=page)
    question_sha: str = get_deterministic_sha(string_to_hash=question)
    question_message_id_in_browser: int = get_question_message_id_in_browser(
        page=page,
        max_message_id_in_browser=max_message_id_in_browser,
        question_sha=question_sha,
    )
    if question_message_id_in_browser != max_message_id_in_browser - 1:
        print(f"question_id:{question_message_id_in_browser}")
        print(f"max_id:{max_message_id_in_browser}")
        raise ValueError(
            "Error, expected the answer id to be the question id +1."
        )

    answer: str = get_chatgpt_conversation(
        page=page,
        turn_nr=max_message_id_in_browser,
    )
    gpt_message: Gpt_message = Gpt_message(
        creator="chatgpt3.5",
        id_in_browser=max_message_id_in_browser,
        message_str=answer,
        parent_id_in_browser=question_message_id_in_browser,
    )

    conversation.add_message(
        new_msg=gpt_message,
        chat_uuid=get_chat_uuid_from_url(some_url=page.url),
    )
