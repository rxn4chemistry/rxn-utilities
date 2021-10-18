# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

from rxn_utilities.container_utilities import all_identical, remove_duplicates, pairwise, chunker


def test_all_identical():
    assert all_identical([])
    assert all_identical([1])
    assert all_identical([1, 1, 1])
    assert not all_identical([1, 2])
    assert not all_identical([1, '1'])


def test_remove_duplicates():
    l_int = [2, 2, 5, 2, 6]
    assert remove_duplicates(l_int) == [2, 5, 6]

    l_str = ['1', 'a', 'word', 'a', 'wor', 'w', '1']
    assert remove_duplicates(l_str) == ['1', 'a', 'word', 'wor', 'w']

    l_tuples = [(3, 3), (3, 2), (2, 2), (3, 3), (1, 1), (3, 3)]
    assert remove_duplicates(l_tuples) == [(3, 3), (3, 2), (2, 2), (1, 1)]


def test_remove_duplicates_with_key():

    class DummyStruct:

        def __init__(self, a, b):
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


def test_pairwise():
    some_list = [1, 2, '3', 4, '5', 'end']

    expected = [(1, 2), (2, '3'), ('3', 4), (4, '5'), ('5', 'end')]

    assert list(pairwise(some_list)) == expected


def test_chunker():
    some_list = list(range(1, 10))  # Numbers 1 to 9

    # Default fill value is None
    assert list(chunker(some_list, 4)) == [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, None, None, None],
    ]

    # custom fill value
    assert list(chunker(some_list, 4, fill_value=-1)) == [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, -1, -1, -1],
    ]

    # Filter out the None values
    assert list(chunker(some_list, 4, filter_out_none=True)) == [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9],
    ]

    # NB: filtering out the None values also removes what was present in initial list
    other_list = [1, 2, None, None, None, None, 7, 8, 9]
    assert list(chunker(other_list, 4, filter_out_none=True)) == [
        [1, 2],
        [7, 8],
        [9],
    ]
