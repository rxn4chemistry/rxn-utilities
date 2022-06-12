"""Functions to help build regex strings. See examples in the tests."""

from typing import Iterable

integer_number_regex = r"[+-]?[0-9]+"
real_number_regex = r"[+-]?[0-9]+(?:\.[0-9]+)?"
scientific_number_regex = real_number_regex + r"([eE][-+]?[0-9]+)?"


def capturing(initial_regex: str) -> str:
    """Add capturing parentheses to a regex string"""
    return f"({initial_regex})"


def alternation(choices: Iterable[str], capture_group=False) -> str:
    """OR operator"""

    inner_string = "|".join(choices)

    if capture_group:
        return f"({inner_string})"
    else:
        return f"(?:{inner_string})"


def optional(initial_regex: str, capture_group=False) -> str:
    """Creates the regex string to make a group optional"""
    if capture_group:
        return f"({initial_regex})?"
    else:
        return f"(?:{initial_regex})?"
