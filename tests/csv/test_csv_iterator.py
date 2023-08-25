from pathlib import Path

import pytest

from rxn.utilities.csv import CsvIterator
from rxn.utilities.files import dump_list_to_file, named_temporary_path


def test_csv_iterator() -> None:
    path: Path
    with named_temporary_path() as path:
        # put the content of a CSV into path; five columns A, B, C, D:DD, and E.
        dump_list_to_file(
            [
                "A,B,C,D:DD,E",
                "a1,b1,c1,d1:41,1",
                "a2,,c2,d2:42,2",
                "a3,b3,,d3:43,3",
                ",b4,c4,d4:44,4",
            ],
            path,
        )

        csv_iterator = CsvIterator(path)

        # a few checks on the column
        assert csv_iterator.columns == ["A", "B", "C", "D:DD", "E"]
        assert csv_iterator.column_index("A") == 0
        assert csv_iterator.column_index("D:DD") == 3
        with pytest.raises(ValueError):
            _ = csv_iterator.column_index("non-existent")

        b_index = csv_iterator.column_index("B")

        # try iterator mode
        it = iter(csv_iterator)
        assert next(it) == ["a1", "b1", "c1", "d1:41", "1"]
        assert next(it) == ["a2", "", "c2", "d2:42", "2"]
        assert next(it)[b_index] == "b3"

        # try direct iteration
        assert [row[b_index] for row in csv_iterator] == ["b1", "", "b3", "b4"]


def test_csv_iterator_with_different_delimiter() -> None:
    path: Path
    with named_temporary_path() as path:
        # same file as for first test; this time the delimiter will be ":"
        dump_list_to_file(
            [
                "A,B,C,D:DD,E",
                "a1,b1,c1,d1:41,1",
                "a2,,c2,d2:42,2",
                "a3,b3,,d3:43,3",
                ",b4,c4,d4:44,4",
            ],
            path,
        )

        csv_iterator = CsvIterator(path, delimiter=":")

        # a few checks on the column
        assert csv_iterator.columns == ["A,B,C,D", "DD,E"]
        assert csv_iterator.column_index("A,B,C,D") == 0
        with pytest.raises(ValueError):
            _ = csv_iterator.column_index("A")

        assert [row[1] for row in csv_iterator] == ["41,1", "42,2", "43,3", "44,4"]
