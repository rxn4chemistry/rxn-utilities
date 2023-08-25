from __future__ import annotations

import csv
from typing import Iterator, List, TextIO, Type, TypeVar

_CsvIteratorT = TypeVar("_CsvIteratorT", bound="CsvIterator")


class CsvIterator:
    """Class to easily iterate through CSV files while having easy
    access to the column names.

    Note: the choice to not handle the file opening/closing in this
    class is on purpose. This avoids issue with keeping track of
    which files are open and when to close them.

    Examples:
        >>> with open("some_file.csv", "rt") as f:
        ...     csv_iterator = CsvIterator.from_stream(f)
        ...     area_index = csv_iterator.column_index("area")
        ...     price_index = csv_iterator.column_index("price")
        ...     for row in csv_iterator.rows:
        ...         price = row[price_index]
        ...         area = row[area_index]
    """

    def __init__(self, columns: List[str], rows: Iterator[List[str]]):
        self.columns = columns
        self.rows = rows

    def column_index(self, column_name: str) -> int:
        """
        Get the index corresponding to the given column.

        Args:
            column_name: column to look up.

        Raises:
            ValueError: if the column does not exist.

        Returns:
            the index for the given column.
        """
        try:
            return self.columns.index(column_name)
        except ValueError:
            raise ValueError(f'Column "{column_name}" not found in {self.columns}.')

    @classmethod
    def from_stream(
        cls: Type[_CsvIteratorT], stream: TextIO, delimiter: str = ","
    ) -> _CsvIteratorT:
        """Instantiate from a stream or file object.

        Args:
            stream: stream or file object to instantiate from.
            delimiter: CSV delimiter.
        """
        reader = csv.reader(stream, delimiter=delimiter)
        header = next(reader)
        return cls(columns=header, rows=reader)

    def to_stream(
        self, file: TextIO, delimiter: str = ",", line_terminator: str = "\n"
    ) -> None:
        writer = csv.writer(file, delimiter=delimiter, lineterminator=line_terminator)
        writer.writerow(self.columns)
        writer.writerows(self.rows)
