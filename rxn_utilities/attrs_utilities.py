from typing import Type, Iterable, List, Tuple

from attr import Attribute


def get_class_attributes(cls: Type) -> Iterable[Attribute]:
    """
    Return the attributes of a class declared with the attrs library.
    """
    return cls.__attrs_attrs__  # type: ignore


def get_variables(cls: Type) -> List[str]:
    """
    Return the names of the variables for a class declared with the attrs
    library.
    """
    return [attribute.name for attribute in get_class_attributes(cls)]


def get_variables_and_types(cls: Type) -> List[Tuple[str, str]]:
    """
    Return the names of the variables and corresponding types for a class
    declared with the attrs library.
    """
    result = []
    for attribute in get_class_attributes(cls):
        # If the attribute __name__ exists, take this (human-friendly), else
        # take the type directly
        t = getattr(attribute.type, "__name__", str(attribute.type))
        result.append((attribute.name, t))
    return result
