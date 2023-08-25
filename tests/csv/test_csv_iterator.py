from pathlib import Path
from typing import Iterator

import pytest

from rxn.utilities.csv import CsvIterator
from rxn.utilities.files import dump_list_to_file, named_temporary_path


@pytest.fixture
def tmp_path() -> Iterator[Path]:
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
        yield path


def test_columns(tmp_path: Path) -> None:
    with open(tmp_path, "rt") as f:
        csv_iterator = CsvIterator.from_file(f)

        # a few checks on the column
        assert csv_iterator.columns == ["A", "B", "C", "D:DD", "E"]
        assert csv_iterator.column_index("A") == 0
        assert csv_iterator.column_index("D:DD") == 3
        with pytest.raises(ValueError):
            _ = csv_iterator.column_index("non-existent")


def test_use_with_next(tmp_path: Path) -> None:
    with open(tmp_path, "rt") as f:
        csv_iterator = CsvIterator.from_file(f)

        b_index = csv_iterator.column_index("B")

        it = iter(csv_iterator.rows)
        assert next(it) == ["a1", "b1", "c1", "d1:41", "1"]
        assert next(it) == ["a2", "", "c2", "d2:42", "2"]
        assert next(it)[b_index] == "b3"


def test_direct_iteration(tmp_path: Path) -> None:
    with open(tmp_path, "rt") as f:
        csv_iterator = CsvIterator.from_file(f)
        b_index = csv_iterator.column_index("B")

        assert [row[b_index] for row in csv_iterator.rows] == ["b1", "", "b3", "b4"]


def test_different_delimiter(tmp_path: Path) -> None:
    with open(tmp_path, "rt") as f:
        csv_iterator = CsvIterator.from_file(f, delimiter=":")

        # a few checks on the column
        assert csv_iterator.columns == ["A,B,C,D", "DD,E"]
        assert csv_iterator.column_index("A,B,C,D") == 0
        with pytest.raises(ValueError):
            _ = csv_iterator.column_index("A")

        assert [row[1] for row in csv_iterator.rows] == ["41,1", "42,2", "43,3", "44,4"]
