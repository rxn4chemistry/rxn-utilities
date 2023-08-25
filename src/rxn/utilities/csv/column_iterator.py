import csv
from typing import Iterator

from ..files import PathLike


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
        RuntimeError: if the column is not valid. Note: the exception is raised not
            raised if the iterator is not consumed.

    Returns:
        iterator through the values in the selected column.
    """
    with open(csv_file, "rt") as f:
        reader = csv.reader(f, delimiter=delimiter)

        header = next(reader)
        try:
            column_index = header.index(column)
        except ValueError:
            raise RuntimeError(f'"{csv_file}" has no column "{column}".')

        yield from (row[column_index] for row in reader)
