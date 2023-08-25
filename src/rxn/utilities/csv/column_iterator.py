from typing import Iterator

from ..files import PathLike
from .csv_iterator import CsvIterator


def iterate_csv_column(
    csv_file: PathLike, column: str, delimiter: str = ","
) -> Iterator[str]:
    """
    Iterate through a specific column of a CSV file.

    The CSV file is iterated through one line at a time, so that the memory footprint
    remains very small, even for large files.

    Args:
        csv_file: CSV file.
        column: Column to iterate through.
        delimiter: CSV delimiter.

    Raises:
        FileNotFoundError: if the file does not exist. Note: the exception is raised not
            raised if the iterator is not consumed.
        ValueError: if the column is not valid. Note: the exception is raised not
            raised if the iterator is not consumed.

    Returns:
        iterator through the values in the selected column.
    """
    with open(csv_file, "rt") as f:
        csv_iterator = CsvIterator.from_stream(f, delimiter=delimiter)
        column_index = csv_iterator.column_index(column_name=column)
        yield from (row[column_index] for row in csv_iterator.rows)
