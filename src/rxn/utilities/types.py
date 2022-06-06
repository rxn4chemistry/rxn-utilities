"""Custom types used in RXN projects."""
from enum import Enum
from typing import Type, TypeVar

T = TypeVar("T", bound="RxnEnum")


class RxnEnum(Enum):
    """
    Custom enum with additional functions for string conversion.

    Has the following functionality compared to a standard Enum:
    * to_string() to generate a lowercase representation of the instance.
    * from_string(value) to instantiate from a string.
    * Constructor is valid both with a string and with another enum instance.
    """

    def to_string(self) -> str:
        """
        Convert the enum to a string representation (all lowercase).
        """
        return self.name.lower()

    @classmethod
    def from_string(cls: Type[T], value: str) -> T:
        """
        Construct the enum from a string, i.e. from the the strings of its
        possible values.

        Args:
            value: string to convert to an instance of the Enum.

        Raises:
            ValueError if the value is not found.

        Returns:
            An instance of the Enum.
        """
        try:
            return cls[value.upper()]
        except KeyError as e:
            allowed_values = [v.to_string() for v in cls]
            allowed_values_str = ", ".join(allowed_values)
            raise ValueError(
                f'Invalid value: "{value}". Only the following are allowed: {allowed_values_str}.'
            ) from e

    @classmethod
    def _missing_(cls: Type[T], value) -> T:
        """
        Overriden to allow instantiation from both string and enum value.
        """
        return cls.from_string(value)
