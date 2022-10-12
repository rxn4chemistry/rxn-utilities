import re

from rxn.utilities.regex import (
    alternation,
    capturing,
    integer_number_regex,
    optional,
    real_number_regex,
    scientific_number_regex,
)


def full_match(regex: str, string: str) -> bool:
    """Returns true if the given regex matches the string exactly."""
    m = re.match(f"^{regex}$", string)
    return m is not None


def test_integer() -> None:
    assert full_match(integer_number_regex, "2")
    assert full_match(integer_number_regex, "23")
    assert full_match(integer_number_regex, "-10")
    assert full_match(integer_number_regex, "0")

    assert not full_match(integer_number_regex, "1 ")
    assert not full_match(integer_number_regex, " 1")
    assert not full_match(integer_number_regex, "1.")
    assert not full_match(integer_number_regex, "1.0")
    assert not full_match(integer_number_regex, "~1")
    assert not full_match(integer_number_regex, "-")
    assert not full_match(integer_number_regex, "+")


def test_real_number() -> None:
    assert full_match(real_number_regex, "2")
    assert full_match(real_number_regex, "23")
    assert full_match(real_number_regex, "2.0")
    assert full_match(real_number_regex, "0.993")
    assert full_match(real_number_regex, "-0.9")
    assert full_match(real_number_regex, "-10")
    assert full_match(real_number_regex, "+10.9")

    assert not full_match(real_number_regex, "1 ")
    assert not full_match(real_number_regex, " 1")
    assert not full_match(real_number_regex, "1.")
    assert not full_match(real_number_regex, ".1")
    assert not full_match(real_number_regex, "~1")
    assert not full_match(real_number_regex, "-")
    assert not full_match(real_number_regex, "+")


def test_scientific_number() -> None:
    assert full_match(scientific_number_regex, "2")
    assert full_match(scientific_number_regex, "+10.9")
    assert full_match(scientific_number_regex, "2E3")
    assert full_match(scientific_number_regex, "2.333E+3")
    assert full_match(scientific_number_regex, "2.333E-3")
    assert full_match(scientific_number_regex, "-2.333e-3")

    assert not full_match(scientific_number_regex, ".1")
    assert not full_match(scientific_number_regex, "-2e-3e")
    assert not full_match(scientific_number_regex, "-2ee-3")
    assert not full_match(scientific_number_regex, "-2F-3")


def test_capturing() -> None:
    number = r"\d+"

    regex_without_capture = f"value: {number}"
    regex_with_capture = f"value: {capturing(number)}"

    text = "value: 123"
    match_without_capture = re.match(regex_without_capture, text)
    match_with_capture = re.match(regex_with_capture, text)

    assert match_without_capture is not None
    assert match_with_capture is not None
    assert len(match_without_capture.groups()) == 0
    assert len(match_with_capture.groups()) == 1


def test_alternation() -> None:
    choices = ["house", "dog", "tree"]

    regex_with_capture = f"I have a {alternation(choices, capture_group=True)}"
    regex_without_capture = f"I have a {alternation(choices)}"

    match_1 = re.match(regex_with_capture, "I have a tree")
    assert match_1 is not None
    assert len(match_1.groups()) == 1

    match_2 = re.match(regex_with_capture, "I have a dog")
    assert match_2 is not None
    assert match_2.group(1) == "dog"

    assert re.match(regex_with_capture, "I have a cat") is None

    match_3 = re.match(regex_without_capture, "I have a house")
    assert match_3 is not None
    assert len(match_3.groups()) == 0

    assert re.match(regex_without_capture, "I have a building") is None


def test_optional() -> None:
    three_digit_number = r"\d\d\d"
    optional_non_capturing_suffix = optional(f" {three_digit_number}")
    optional_capturing_suffix = optional(f" {three_digit_number}", capture_group=True)

    regex_without_capture = "number" + optional_non_capturing_suffix
    regex_with_capture = "number" + optional_capturing_suffix

    assert re.findall(regex_without_capture, "This is a number") == ["number"]
    assert re.findall(regex_without_capture, "This is a number 003") == ["number 003"]
    assert re.findall(regex_without_capture, "This is a dummy 003") == []
    assert re.findall(regex_with_capture, "This is a number") == [""]
    assert re.findall(regex_with_capture, "This is a number 003") == [" 003"]
    assert re.findall(regex_with_capture, "This is a dummy 003") == []
