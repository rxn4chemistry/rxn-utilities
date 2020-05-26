from typing import Optional

import attr

from rxn_utilities.attrs_utilities import get_variables, get_variables_and_types


@attr.s(auto_attribs=True)
class DummyClass:
    variable_1: float
    variable_2: str
    variable_3: Optional[int]


def test_get_variables():
    assert get_variables(DummyClass) == [
        'variable_1',
        'variable_2',
        'variable_3',
    ]


def test_get_variables_and_types():
    assert get_variables_and_types(DummyClass) == [
        ('variable_1', 'float'),
        ('variable_2', 'str'),
        ('variable_3', 'typing.Union[int, NoneType]'),
    ]
