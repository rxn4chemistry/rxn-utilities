from rxn_utilities.container_utilities import all_identical, remove_duplicates


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
