import itertools
from typing import Sequence, Any, Iterable, Optional, Callable, Set, List, Iterator, Tuple, TypeVar

T = TypeVar('T')
V = TypeVar('V')


def all_identical(sequence: Sequence[Any]) -> bool:
    """Evaluates whether all the elements of a sequence are identical."""
    return all(s == sequence[0] for s in sequence)


def remove_duplicates(seq: Iterable[T], key: Optional[Callable[[T], V]] = None) -> List[T]:
    """Remove duplicates and preserve order.

    Adapted from https://stackoverflow.com/a/480227

    Args:
        seq: sequence to remove duplicates from.
        key: what to base duplicates on, must be hashable.
            Defaults to the elements of seq.
    """
    if key is None:

        def key(x: T) -> V:
            return x  # type: ignore

    assert key is not None  # Necessary for mypy

    seen: Set[V] = set()
    seen_add = seen.add
    return [x for x in seq if not (key(x) in seen or seen_add(key(x)))]


def pairwise(s: List[T]) -> Iterator[Tuple[T, T]]:
    """
    Iterates over neighbors in a list.

    s -> (s0,s1), (s1,s2), (s2, s3), ...

    From https://stackoverflow.com/a/5434936
    """

    a, b = itertools.tee(s)
    next(b, None)
    return zip(a, b)
