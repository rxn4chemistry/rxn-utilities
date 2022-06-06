import itertools
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    cast,
)

T = TypeVar("T")
V = TypeVar("V")


def all_identical(sequence: Sequence[Any]) -> bool:
    """Evaluates whether all the elements of a sequence are identical."""
    return all(s == sequence[0] for s in sequence)


def remove_duplicates(
    seq: Iterable[T], key: Optional[Callable[[T], V]] = None
) -> List[T]:
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


# Make it possible to test whether a value was provided at all (See Python Cookbook 7.5).
_no_value: T = object()  # type: ignore


def chunker(
    iterable: Iterable[T],
    chunk_size: int,
    fill_value: T = _no_value,
) -> Generator[List[T], None, None]:
    """
    Iterate through an iterable in chunks of given size.

    Adapted from "grouper" function in the itertools documentation:
    https://docs.python.org/3/library/itertools.html#itertools-recipes

    Args:
        iterable: some iterable to create chunks from.
        chunk_size: size of the chunks.
        fill_value: value to fill in if the last chunk is too small. If nothing
            is specified, the last chunk may be smaller.

    Returns:
        Iterator over lists representing the chunks.
    """

    # These two lines: same as the "grouper" function in the itertools doc.
    # In zip_longest, we do not give the user-provided fill value, which
    # would make it complicated to differentiate with the case where nothing
    # was given further below.
    args = [iter(iterable)] * chunk_size
    tuple_iterable = itertools.zip_longest(*args, fillvalue=_no_value)

    for chunk_tuple in tuple_iterable:
        # convert to list instead of tuples, remove the fill value
        chunk = [value for value in chunk_tuple if value is not _no_value]

        # If the user provided a fill value, add it.
        if len(chunk) != chunk_size and fill_value is not _no_value:
            n_missing = chunk_size - len(chunk)
            chunk += [fill_value] * n_missing

        yield chunk
