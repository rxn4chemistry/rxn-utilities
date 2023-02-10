import math
from typing import Tuple


def get_multipliers(a: int, b: int) -> Tuple[int, int]:
    """
    Get the multipliers m_a and m_b so that m_a * a == m_b * b.

    Raises:
        ValueError: If one of the numbers is not strictly positive.

    Returns:
        Tuple: multiplier for a, multiplier for b.
    """
    if a < 1 or b < 1:
        raise ValueError(
            f"Can't determine multipliers for non-strictly-positive numbers ({a} and {b})"
        )

    # Lowest common multiplier, https://stackoverflow.com/a/51716959
    lcm = abs(a * b) // math.gcd(a, b)

    return lcm // a, lcm // b


def get_multiplier(a: int, b: int) -> int:
    """
    Get the multiplier m so that m * a == b.

    Raises:
        ValueError: If b is not exactly a multiplier of a (possibly forwarded from
            get_multipliers).

    Returns:
        multiplier for a.
    """

    m_a, m_b = get_multipliers(a, b)

    # if the multiplier for b is not 1, it means that b is not a multiple of a.
    if m_b != 1:
        raise ValueError(f"{b} is not a multiple of {a}.")

    return m_a
