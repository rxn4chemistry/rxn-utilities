import pytest

from rxn.utilities.strings import (
    dash_characters,
    escape_latex,
    remove_postfix,
    remove_prefix,
)


def test_dash_characters() -> None:
    # dash-minus
    assert "\u002d" in dash_characters
    # en-dash
    assert "\u2013" in dash_characters
    # em-dash
    assert "\u2014" in dash_characters

    # assert that they are all different
    assert len(dash_characters) == len(set(dash_characters))

    # assert that they all have length one
    assert all(len(c) == 1 for c in dash_characters)


def test_remove_prefix() -> None:
    s = "one two three four"

    assert remove_prefix(s, "one ") == "two three four"
    assert remove_prefix(s, "One ") == s
    assert remove_prefix(s, "two") == s

    with pytest.raises(ValueError):
        _ = remove_prefix(s, "two", raise_if_missing=True)


def test_remove_postfix() -> None:
    s = "one two three four"

    assert remove_postfix(s, " four") == "one two three"
    assert remove_postfix(s, "Four") == s
    assert remove_postfix(s, "two") == s

    with pytest.raises(ValueError):
        _ = remove_postfix(s, "two", raise_if_missing=True)


def test_tex_escape() -> None:
    assert escape_latex("30%") == r"30\%"
