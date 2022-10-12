from typing import Iterable, Optional

from rxn.utilities.containers import all_identical, chunker, pairwise, remove_duplicates


def test_all_identical() -> None:
    assert all_identical([])
    assert all_identical([1])
    assert all_identical([1, 1, 1])
    assert not all_identical([1, 2])
    assert not all_identical([1, "1"])


def test_remove_duplicates() -> None:
    l_int = [2, 2, 5, 2, 6]
    assert remove_duplicates(l_int) == [2, 5, 6]

    l_str = ["1", "a", "word", "a", "wor", "w", "1"]
    assert remove_duplicates(l_str) == ["1", "a", "word", "wor", "w"]

    l_tuples = [(3, 3), (3, 2), (2, 2), (3, 3), (1, 1), (3, 3)]
    assert remove_duplicates(l_tuples) == [(3, 3), (3, 2), (2, 2), (1, 1)]


def test_remove_duplicates_with_key() -> None:
    class DummyStruct:
        def __init__(self, a: int, b: int):
            self.a = a
            self.b = b

    # we will remove duplicates based on the second value, i.e. only a1,
    # a2, a3, a6 will remain.
    a1 = DummyStruct(1, 5)
    a2 = DummyStruct(2, 3)
    a3 = DummyStruct(3, 4)
    a4 = DummyStruct(4, 5)
    a5 = DummyStruct(5, 3)
    a6 = DummyStruct(6, 6)

    li = [a1, a2, a3, a4, a5, a6]

    assert remove_duplicates(li, key=lambda x: x.b) == [a1, a2, a3, a6]


def test_pairwise() -> None:
    some_list = [1, 2, "3", 4, "5", "end"]

    expected = [(1, 2), (2, "3"), ("3", 4), (4, "5"), ("5", "end")]

    assert list(pairwise(some_list)) == expected


def test_chunker() -> None:
    some_list: Iterable[Optional[int]] = range(1, 10)  # Numbers 1 to 9

    # By default, nothing is filled
    assert list(chunker(some_list, 4)) == [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9],
    ]

    # custom fill value
    assert list(chunker(some_list, 4, fill_value=-1)) == [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, -1, -1, -1],
    ]
    assert list(chunker(some_list, 4, fill_value=None)) == [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, None, None, None],
    ]

    # When the size is an exact multiple, no need to fill
    assert list(chunker(some_list, 3, fill_value=-1)) == [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
