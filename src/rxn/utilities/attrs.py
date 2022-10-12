"""Helper functions for handling classes defined with the package attrs."""

from __future__ import annotations  # for ``Type[Any]``

from typing import Any, Iterable, List, Tuple, Type

from attr import Attribute


def get_class_attributes(cls: Type[Any]) -> Iterable[Attribute[Any]]:
    """
    Return the attributes of a class declared with the attrs library.
    """
    return cls.__attrs_attrs__  # type: ignore


def get_variables(cls: Type[Any]) -> List[str]:
    """
    Return the names of the variables for a class declared with the attrs
    library.
    """
    return [attribute.name for attribute in get_class_attributes(cls)]


def get_variables_and_types(cls: Type[Any]) -> List[Tuple[str, Type[Any]]]:
    """
    Return the names of the variables and corresponding types for a class
    declared with the attrs library.
    """
    result = []
    for attribute in get_class_attributes(cls):
        t = attribute.type
        assert t is not None
        result.append((attribute.name, t))
    return result


def get_variables_and_type_names(cls: Type[Any]) -> List[Tuple[str, str]]:
    """
    Return the names of the variables and corresponding type names for a class
    declared with the attrs library.
    """
    # If the attribute __name__ exists, take this (human-friendly), else
    # take the type directly
    return [
        (variable, getattr(t, "__name__", str(t)))
        for variable, t in get_variables_and_types(cls)
    ]
