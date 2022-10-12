from enum import auto

import pytest

from rxn.utilities.types import RxnEnum


class DummyEnum(RxnEnum):
    """
    Concrete Enum for testing RxnEnum.
    """

    ITALY = auto()
    SWITZERLAND = auto()
    GERMANY = auto()


def test_rxn_enum() -> None:
    # Instantiation from enum
    assert DummyEnum(DummyEnum.ITALY) == DummyEnum.ITALY
    assert DummyEnum(DummyEnum.GERMANY) == DummyEnum.GERMANY

    # Instantiation from string
    assert DummyEnum("italy") == DummyEnum.ITALY
    assert DummyEnum("Italy") == DummyEnum.ITALY
    assert DummyEnum("ITALY") == DummyEnum.ITALY

    # from_string
    assert DummyEnum.from_string("italy") == DummyEnum.ITALY
    assert DummyEnum.from_string("GERMANY") == DummyEnum.GERMANY

    # to_string
    assert DummyEnum.ITALY.to_string() == "italy"

    # exceptions
    with pytest.raises(ValueError) as exc_info:
        DummyEnum("zurich")
    expected_exception_string = (
        'Invalid value: "zurich". Only the following are allowed: '
        "italy, switzerland, germany."
    )
    assert expected_exception_string in str(exc_info)
