"""Ask a question to chatgpt3.5 through the website interface."""

import random  # nosec
import time

from playwright.sync_api._generated import Locator, Page
from typeguard import typechecked

from jsonmodipy.chatgpt35.helper import (
    click_button_by_text,
    find_element_with_text,
    is_in_cloudfare,
)


@typechecked
def ensure_chatgpt35_login(page: Page, username: str, password: str) -> None:
    """Checks whether the user is logged into chatgpt35, and if not logs in."""
    # Check if page source contains: the username.
    # TODO: verify the username has the format of an email address.
    time.sleep(5)
    if username not in page.content():
        login_chatgpt35(page=page, username=username, password=password)
    if username not in page.content():
        raise SystemError("Error, could not log in.")


@typechecked
def login_chatgpt35(page: Page, username: str, password: str) -> None:
    """Logs into chatgpt35."""
    # TODO: assert url is valid.
    if (
        "https://chat.openai.com/auth/login" not in page.url
        and "https://auth0.openai.com/u/login/" not in page.url
    ):
        raise ValueError(
            "Error, expected:\nhttps://chat.openai.com/auth/login\ngot:\n"
            + f"{page.url}"
        )
    click_login_chatgpt35(page=page)
    resolve_cloudfare_chatpt35(page=page)
    submit_username_and_password(
        page=page,
        username=username,
        password=password,
    )
    click_okay_chatgpt35(page=page)


@typechecked
def click_login_chatgpt35(*, page: Page) -> None:
    """Clicks the login button on the ChatGPT website."""

    time.sleep(random.randint(1500, 5000) / 1000.0)  # nosec

    # Find the button using the data-testid attribute
    page.wait_for_selector('[data-testid="login-button"]', state="visible")
    button_locator: Locator = page.locator('[data-testid="login-button"]')

    # You can interact with the button using the Locator object
    button_locator.scroll_into_view_if_needed()
    button_locator.click()  # Click the button
    button_locator.press("Enter")
    time.sleep(random.randint(1500, 5000) / 1000.0)  # nosec


@typechecked
def resolve_cloudfare_chatpt35(
    *,
    page: Page,
) -> None:
    """Ensures cloudfare can be passed (manually)."""
    if is_in_cloudfare(page=page):
        input("Seeing captcha. Please manually click: I am human.")


@typechecked
def submit_username_and_password(
    *, page: Page, username: str, password: str
) -> None:
    """Submits the chatgpt username and password to the website and logs in."""
    email_input: Locator = find_element_with_text(
        page=page,
        text="#username",
        strict=False,
    )

    email_input.fill(username)

    email_input.press("Enter")

    time.sleep(random.randint(1500, 5000) / 1000.0)  # nosec

    # Locate the password input element by its id
    password_input: Locator = find_element_with_text(
        page=page,
        text="#password",
        strict=False,
    )

    # Fill in the password
    password_input.fill(password)
    password_input.press("Enter")
    input("Logged in?")
    time.sleep(random.randint(5000, 10000) / 1000.0)  # nosec


def click_okay_chatgpt35(
    *,
    page: Page,
) -> None:
    """Clicks the "okay" button if such a prompt appears in the ChatGPT
    website."""
    # Click the okay button.
    has_xpath_okay: bool = click_button_by_text(
        page=page,
        text="Okay, let’s go",
    )
    print(f'Have clicked on "Okay":{has_xpath_okay}')

    time.sleep(random.randint(1500, 5000) / 1000.0)  # nosec
