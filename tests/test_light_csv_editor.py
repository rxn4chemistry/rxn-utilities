import filecmp
from pathlib import Path
from typing import Iterator, List

import pytest

from rxn.utilities.basic import identity
from rxn.utilities.files import (
    named_temporary_directory,
    dump_list_to_file,
    load_list_from_file,
    PathLike,
)
from rxn.utilities.light_csv_editor import LightCsvEditor


@pytest.fixture
def temp_dir() -> Iterator[Path]:
    with named_temporary_directory() as path:
        yield path


def assert_files_identical(file1: PathLike, file2: PathLike) -> None:
    """Verify that two files have the same content.

    Preferred to filecmp.cmp(), in order to get a more sensible error
    message when failing.
    """
    content1 = load_list_from_file(file1)
    content2 = load_list_from_file(file2)
    assert content1 == content2


def test_identity(temp_dir: Path) -> None:
    input_file = temp_dir / "input"
    output_file = temp_dir / "output"
    expected_file = temp_dir / "expected"

    # Input
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], input_file)

    csv_editor = LightCsvEditor(["a"], ["a"], identity)

    csv_editor.process(input_file, output_file)

    # expected
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], expected_file)
    assert_files_identical(output_file, expected_file)


def test_overwrite_one_column(temp_dir: Path) -> None:
    input_file = temp_dir / "input"
    output_file = temp_dir / "output"
    expected_file = temp_dir / "expected"

    # Input
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], input_file)

    def fn(values: List[str]) -> List[str]:
        return [v.upper() for v in values]

    csv_editor = LightCsvEditor(["a"], ["a"], fn)

    csv_editor.process(input_file, output_file)

    # expected
    dump_list_to_file(["a,b,c", "FIRST,line,1", "SECOND,line,2"], expected_file)
    assert_files_identical(output_file, expected_file)
