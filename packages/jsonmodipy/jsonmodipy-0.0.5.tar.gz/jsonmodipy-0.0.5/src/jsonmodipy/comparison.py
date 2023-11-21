"""Compares the content of two files as though they do not have new line
characters."""
import copy

from typeguard import typechecked


@typechecked
def get_without_empty_lines(*, text: str) -> str:
    """Returns the text where all new lines are removed, and where all multi-
    spaces are replaced with a single space."""
    copied_text: str = copy.deepcopy(text)
    without_empty_lines: str = remove_empty_lines(text=copied_text)
    return without_empty_lines


@typechecked
def remove_empty_lines(*, text: str) -> str:
    """Remove lines from the input text that only contain spaces and/or tabs.

    Args:
        text (str): The input text containing lines.

    Returns:
        str: The text with lines containing only spaces and/or tabs removed.
    """
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    return "\n".join(non_empty_lines)


@typechecked
def remove_comment_lines(*, text: str) -> str:
    """Remove comment lines from the input text.

    Args:
        text (str): The input text containing lines.

    Returns:
        str: The text with lines containing only spaces and/or tabs removed.
    """
    lines = text.splitlines()
    non_comment_lines = [
        line for line in lines if not has_leading_hashtag(line=line)
    ]
    return "\n".join(non_comment_lines)


@typechecked
def has_leading_hashtag(*, line: str) -> bool:
    """Returns True if a line starts with a hashtag after spaces or tabs.

    Args:
        text (str): The input text containing lines.

    Returns:
        str: The text with lines containing only spaces and/or tabs removed.
    """
    if len(line) == 0:
        return False
    for char in line:
        if char not in [" ", "\n", "    "]:
            if char == "#":
                return True
            return False
    raise ValueError(f"Error, unexpected leading character development:{line}")


@typechecked
def remove_newline_chars(text: str) -> str:
    """Removes newline characters from a given string.

    Args:
        text (str): The input string with newline characters.

    Returns:
        str: The input string with newline characters removed.
    """
    return text.replace("\n", "")


@typechecked
def replace_multiple_spaces_with_single_space(text: str) -> str:
    """Replace all occurrences of multiple spaces with a single space in the
    input text.

    Args:
        text (str): The input text containing spaces.

    Returns:
        str: The text with multiple spaces replaced by a single space.
    """
    return " ".join(text.split())


@typechecked
def equal_without_multi_spaces(original: str, reconstructed: str) -> bool:
    """Compares two strings after removing newline characters and checks if
    they are identical.

    Args:
        s1 (str): The first input string.
        s2 (str): The second input string.

    Returns:
        bool: True if the strings are identical without newline characters,
        False otherwise.
    """
    original_wo_comments: str = remove_comment_lines(text=original)
    print(f"original_collapsed={original_wo_comments}")
    reconstructed_wo_comments: str = remove_comment_lines(text=reconstructed)
    print(f"reconstructed_collapsed={reconstructed_wo_comments}")

    original_without_multispace: str = (
        replace_multiple_spaces_with_single_space(
            remove_newline_chars(original_wo_comments)
        )
    )
    reconstructed_without_multispace: str = (
        replace_multiple_spaces_with_single_space(
            remove_newline_chars(reconstructed_wo_comments)
        )
    )
    return original_without_multispace == reconstructed_without_multispace
