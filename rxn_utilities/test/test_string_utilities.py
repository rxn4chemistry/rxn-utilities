from rxn_utilities.string_utiltities import remove_prefix, remove_postfix


def test_remove_prefix():
    s = 'one two three four'

    assert remove_prefix(s, 'one ') == 'two three four'
    assert remove_prefix(s, 'One ') == s
    assert remove_prefix(s, 'two') == s


def test_remove_postfix():
    s = 'one two three four'

    assert remove_postfix(s, ' four') == 'one two three'
    assert remove_postfix(s, 'Four') == s
    assert remove_postfix(s, 'two') == s
