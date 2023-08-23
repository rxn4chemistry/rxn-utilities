from pathlib import Path
from typing import Iterator, List

import pytest
from attr import define

from rxn.utilities.basic import identity
from rxn.utilities.files import (
    PathLike,
    dump_list_to_file,
    load_list_from_file,
    named_temporary_directory,
)
from rxn.utilities.light_csv_editor import LightCsvEditor


@define
class FileTriplet:
    in_: Path  # Note: underscore because "in" is not allowed
    out: Path
    expected: Path


@pytest.fixture
def temp_dir() -> Iterator[FileTriplet]:
    with named_temporary_directory() as path:
        yield FileTriplet(path / "in", path / "out", path / "expected")


def assert_files_identical(file1: PathLike, file2: PathLike) -> None:
    """Verify that two files have the same content.

    Preferred to filecmp.cmp(), in order to get a more sensible error
    message when failing.
    """
    content1 = load_list_from_file(file1)
    content2 = load_list_from_file(file2)
    assert content1 == content2


def test_identity(files: FileTriplet) -> None:
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], files.in_)

    csv_editor = LightCsvEditor(["a"], ["a"], identity)

    csv_editor.process(files.in_, files.out)

    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], files.expected)
    assert_files_identical(files.out, files.expected)


def test_overwrite_one_column(files: FileTriplet) -> None:
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], files.in_)

    def fn(values: List[str]) -> List[str]:
        return [v.upper() for v in values]

    csv_editor = LightCsvEditor(["a"], ["a"], fn)

    csv_editor.process(files.in_, files.out)

    dump_list_to_file(["a,b,c", "FIRST,line,1", "SECOND,line,2"], files.expected)
    assert_files_identical(files.out, files.expected)
