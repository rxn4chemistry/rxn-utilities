# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED
import pytest

from rxn_utilities.string_utiltities import (
    dash_characters,
    escape_latex,
    remove_postfix,
    remove_prefix,
)


def test_dash_characters():
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


def test_remove_prefix():
    s = "one two three four"

    assert remove_prefix(s, "one ") == "two three four"
    assert remove_prefix(s, "One ") == s
    assert remove_prefix(s, "two") == s

    with pytest.raises(ValueError):
        _ = remove_prefix(s, "two", raise_if_missing=True)


def test_remove_postfix():
    s = "one two three four"

    assert remove_postfix(s, " four") == "one two three"
    assert remove_postfix(s, "Four") == s
    assert remove_postfix(s, "two") == s

    with pytest.raises(ValueError):
        _ = remove_postfix(s, "two", raise_if_missing=True)


def test_tex_escape():
    assert escape_latex("30%") == r"30\%"
