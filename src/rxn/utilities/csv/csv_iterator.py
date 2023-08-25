from __future__ import annotations

import csv
from typing import Iterator, List, TextIO

from ..files import PathLike


class CsvIterator:
    """Class to easily iterate through CSV files while having easy
    access to the column names.

    Examples:
        >>> csv_iterator = CsvIterator("some_file.csv")
        >>> area_index = csv_iterator.column_index("area")
        >>> price_index = csv_iterator.column_index("price")
        >>> for row in csv_iterator:
        ...     price = row[price_index]
        ...     area = row[area_index]
    """

    def __init__(self, csv_file: PathLike, delimiter: str = ","):
        self.delimiter = delimiter
        self.csv_file = csv_file
        self.columns = self._read_header()

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
            raise ValueError(f'"{self.csv_file}" has no column "{column_name}".')

    def __iter__(self) -> Iterator[List[str]]:
        """
        Iterate through the rows of the CSV.

        Yields:
            list of strings for each row of the CSV.
        """
        with open(self.csv_file, "rt") as f:
            reader = self._instantiate_reader(f)
            # ignore the header
            _ = next(reader)
            # yield from the remaining lines
            yield from reader

    def _read_header(self) -> List[str]:
        with open(self.csv_file, "rt") as f:
            return next(self._instantiate_reader(f))

    def _instantiate_reader(self, file: TextIO) -> Iterator[List[str]]:
        return csv.reader(file, delimiter=self.delimiter)
