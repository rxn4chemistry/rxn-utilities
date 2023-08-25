from pathlib import Path

import pytest

from rxn.utilities.csv.column_iterator import iterate_csv_column
from rxn.utilities.files import dump_list_to_file, named_temporary_path


def test_iterate_csv_column() -> None:
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

        assert list(iterate_csv_column(path, "A")) == ["a1", "a2", "a3", ""]
        assert list(iterate_csv_column(path, "B")) == ["b1", "", "b3", "b4"]
        assert list(iterate_csv_column(path, "C")) == ["c1", "c2", "", "c4"]
        assert list(iterate_csv_column(path, "D:DD")) == [
            "d1:41",
            "d2:42",
            "d3:43",
            "d4:44",
        ]
        assert list(iterate_csv_column(path, "E")) == ["1", "2", "3", "4"]

        with pytest.raises(RuntimeError):
            _ = list(iterate_csv_column(path, "F"))

        with pytest.raises(FileNotFoundError):
            _ = list(iterate_csv_column("invalid_file.csv", "A"))

        # Use ":" as delimiter instead of ",". Now the columns are "A,B,C,D" and "DD,E".
        with pytest.raises(RuntimeError):
            _ = list(iterate_csv_column(path, "A", delimiter=":"))
        assert list(iterate_csv_column(path, "DD,E", delimiter=":")) == [
            "41,1",
            "42,2",
            "43,3",
            "44,4",
        ]
