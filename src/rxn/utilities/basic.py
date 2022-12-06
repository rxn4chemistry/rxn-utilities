import random
from contextlib import contextmanager
from typing import Iterator, Optional, TypeVar

T = TypeVar("T")


def identity(x: T) -> T:
    return x


@contextmanager
def sandboxed_random_context() -> Iterator[None]:
    """
    Enter a context that will not affect the Python random state.

    This works by saving the random state at the beginning of the context
    and resetting it when exiting the context.

    Examples:
        >>> with sandboxed_random_context():
        ...     _ = random.random()  # has no effect outside of the context
    """
    random_state = random.getstate()
    try:
        yield
    finally:
        random.setstate(random_state)


@contextmanager
def temporary_random_seed(seed: Optional[int]) -> Iterator[None]:
    """
    Set a random seed in a context, to avoid side effects.

    Examples:
        >>> with temporary_random_seed(101):
        ...     # ``a`` will always have the same value
        ...     a = random.random()

    Args:
        seed: seed, directly forwarded to random.seed(). ``None`` means using
            the system time.
    """
    with sandboxed_random_context():
        random.seed(seed)
        yield
