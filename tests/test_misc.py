import pytest

from rxn.utilities.misc import get_multiplier, get_multipliers


def test_get_multipliers() -> None:
    assert get_multipliers(1, 1) == (1, 1)
    assert get_multipliers(123, 123) == (1, 1)
    assert get_multipliers(1, 12) == (12, 1)
    assert get_multipliers(12, 1) == (1, 12)
    assert get_multipliers(3, 27) == (9, 1)
    assert get_multipliers(27, 3) == (1, 9)

    assert get_multipliers(2, 3) == (3, 2)
    assert get_multipliers(10, 6) == (3, 5)

    invalid_pairs = [
        (0, 0),
        (-1, -1),
        (-1, 1),
    ]
    for a, b in invalid_pairs:
        with pytest.raises(ValueError):
            _ = get_multipliers(a, b)


def test_get_multiplier() -> None:
    assert get_multiplier(1, 1) == 1
    assert get_multiplier(123, 123) == 1
    assert get_multiplier(1, 12) == 12
    assert get_multiplier(6, 12) == 2
    assert get_multiplier(3, 27) == 9

    invalid_pairs = [
        (0, 0),
        (-1, -1),
        (-1, 1),
        (2, 1),
        (2, 3),
        (3, 2),
    ]
    for a, b in invalid_pairs:
        with pytest.raises(ValueError):
            _ = get_multiplier(a, b)
