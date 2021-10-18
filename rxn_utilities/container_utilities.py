# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

import itertools
from typing import (
    Sequence, Any, Iterable, Optional, Callable, Set, List, Iterator, Tuple, TypeVar, cast,
    Generator
)

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

    key = cast(Callable[[T], V], key)  # necessary for mypy

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


def chunker(
    iterable: Iterable[T],
    chunk_size: int,
    fill_value: Optional[T] = None,
    filter_out_none: bool = False
) -> Generator[List[T], None, None]:
    """
    Iterate through an iterable in chunks of given size.

    Adapted from "grouper" function in the itertools documentation:
    https://docs.python.org/3/library/itertools.html#itertools-recipes

    Args:
        iterable: some iterable to create chunks from.
        chunk_size: size of the chunks.
        fill_value: value to fill in if the last chunk is too small.
        filter_out_none: whether to remove from the chunks, especially in order
            to not fill the last chunk if it is too small.

    Returns:
        Iterator over lists representing the chunks.
    """

    # These two lines: same as the "grouper" function in the itertools doc.
    args = [iter(iterable)] * chunk_size
    tuple_iterable = itertools.zip_longest(*args, fillvalue=fill_value)

    # convert to lists instead of tuples
    list_iterable = (list(chunk) for chunk in tuple_iterable)

    if filter_out_none:
        yield from ([item for item in chunk if item is not None] for chunk in list_iterable)

    yield from list_iterable
