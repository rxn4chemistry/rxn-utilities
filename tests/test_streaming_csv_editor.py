from pathlib import Path
from typing import Any, Callable, Iterator, List, Tuple

import pytest
from attr import define

from rxn.utilities.containers import all_identical
from rxn.utilities.files import (
    PathLike,
    dump_list_to_file,
    load_list_from_file,
    named_temporary_directory,
)
from rxn.utilities.streaming_csv_editor import StreamingCsvEditor


@define
class FileTriplet:
    directory: Path
    in_: Path  # Note: underscore because "in" is not allowed
    out: Path
    expected: Path


def identity_list(values: List[str]) -> List[str]:
    return values


def identity_str(value: str) -> str:
    return value


@pytest.fixture
def files() -> Iterator[FileTriplet]:
    with named_temporary_directory() as path:
        yield FileTriplet(path, path / "in", path / "out", path / "expected")


def assert_files_identical(*files: PathLike) -> None:
    """Verify that the given files have the same content.

    Preferred to filecmp.cmp(), in order to get a more sensible error
    message when failing.
    """
    contents = [load_list_from_file(file) for file in files]
    assert all_identical(contents), f"Differing contents: {contents}"


def test_identity_on_one_column(files: FileTriplet) -> None:
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], files.in_)

    csv_editor = StreamingCsvEditor(["a"], ["a"], identity_str)
    csv_editor.process(files.in_, files.out)

    assert_files_identical(files.out, files.in_)


def test_identity_on_multiple_columns(files: FileTriplet) -> None:
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], files.in_)

    csv_editor = StreamingCsvEditor(["a", "c"], ["a", "c"], identity_list)
    csv_editor.process(files.in_, files.out)

    assert_files_identical(files.out, files.in_)


def test_identity_replacing_another_column(files: FileTriplet) -> None:
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], files.in_)

    csv_editor = StreamingCsvEditor(["a"], ["c"], identity_list)
    csv_editor.process(files.in_, files.out)

    dump_list_to_file(
        ["a,b,c", "first,line,first", "second,line,second"], files.expected
    )
    assert_files_identical(files.out, files.expected)


def test_identity_adding_a_new_column(files: FileTriplet) -> None:
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], files.in_)

    csv_editor = StreamingCsvEditor(["a"], ["new"], identity_str)
    csv_editor.process(files.in_, files.out)

    dump_list_to_file(
        ["a,b,c,new", "first,line,1,first", "second,line,2,second"], files.expected
    )
    assert_files_identical(files.out, files.expected)


def test_overwrite_one_column(files: FileTriplet) -> None:
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], files.in_)

    def fn(v: str) -> str:
        return v.upper()

    csv_editor = StreamingCsvEditor(["a"], ["a"], fn)

    csv_editor.process(files.in_, files.out)

    dump_list_to_file(["a,b,c", "FIRST,line,1", "SECOND,line,2"], files.expected)
    assert_files_identical(files.out, files.expected)


def test_overwrite_one_and_add_one(files: FileTriplet) -> None:
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], files.in_)

    # the function in this test takes one input and has two outputs
    # the first output is the uppercase, the second one is the first letter
    def fn(value: str) -> List[str]:
        return [value.upper(), value[0]]

    csv_editor = StreamingCsvEditor(["a"], ["c", "new"], fn)

    csv_editor.process(files.in_, files.out)

    dump_list_to_file(
        ["a,b,c,new", "first,line,FIRST,f", "second,line,SECOND,s"], files.expected
    )
    assert_files_identical(files.out, files.expected)


def test_different_callback_formulations(files: FileTriplet) -> None:
    dump_list_to_file(["a,b,c", "first,line,1", "second,line,2"], files.in_)

    # We define multiple functions that should have identical behavior, to test
    # the flexibility of callables given to the StreamingCsvEditor.
    # The first digit is the number of inputs, the second is the number of outputs,
    # the letter indicates the variant (functions differing only in the letter
    # have identical behavior).

    # functions "11": return uppercase
    def fn_11a(value: str) -> str:
        return value.upper()

    def fn_11b(value: List[str]) -> str:
        return value[0].upper()

    def fn_11c(value: Tuple[str]) -> str:
        return value[0].upper()

    def fn_11d(value: Tuple[str]) -> List[str]:
        return [value[0].upper()]

    def fn_11e(value: List[str]) -> Tuple[str]:
        return (value[0].upper(),)

    # functions "12": return uppercase, and then the first letter
    def fn_12a(value: str) -> List[str]:
        return [value.upper(), value[0]]

    def fn_12b(value: str) -> Tuple[str, str]:
        return value.upper(), value[0]

    def fn_12c(values: List[str]) -> List[str]:
        return [values[0].upper(), values[0][0]]

    # functions "21": concatenate after uppercasing the first arg
    def fn_21a(v1: str, v2: str) -> str:
        return v1.upper() + v2

    def fn_21b(values: List[str]) -> str:
        return values[0].upper() + values[1]

    def fn_21c(values: Tuple[str, str]) -> str:
        return values[0].upper() + values[1]

    def fn_21d(v1: str, v2: str) -> List[str]:
        return [v1.upper() + v2]

    def fn_21e(values: Tuple[str, str]) -> List[str]:
        return [values[0].upper() + values[1]]

    def fn_21f(values: List[str]) -> Tuple[str]:
        return (values[0].upper() + values[1],)

    # functions "22": return uppercase of first one, first letter of second one
    def fn_22a(v1: str, v2: str) -> List[str]:
        return [v1.upper(), v2[0]]

    def fn_22b(values: List[str]) -> List[str]:
        return [values[0].upper(), values[1][0]]

    def fn_22c(values: Tuple[str, str]) -> List[str]:
        return [values[0].upper(), values[1][0]]

    def fn_22d(values: List[str]) -> Tuple[str, str]:
        return values[0].upper(), values[1][0]

    all_functions_to_compare: List[
        Tuple[List[Callable[..., Any]], List[str], List[str]]
    ] = [
        ([fn_11a, fn_11b, fn_11c, fn_11d, fn_11e], ["a"], ["c"]),
        ([fn_12a, fn_12b, fn_12c], ["a"], ["c", "new"]),
        ([fn_21a, fn_21b, fn_21c, fn_21d, fn_21e, fn_21f], ["a", "b"], ["new"]),
        ([fn_22a, fn_22b, fn_22c, fn_22d], ["a", "b"], ["new1", "c"]),
    ]

    for functions_to_compare, columns_in, columns_out in all_functions_to_compare:
        files_to_compare: List[Path] = []
        for i, fn in enumerate(functions_to_compare):
            csv_editor = StreamingCsvEditor(columns_in, columns_out, fn)
            file_i = files.directory / f"out_{i}"
            csv_editor.process(files.in_, file_i)
            files_to_compare.append(file_i)

        assert_files_identical(*files_to_compare)


def test_raises_if_function_not_annotated() -> None:
    # parameter not annotated
    with pytest.raises(ValueError):

        def fn1(a) -> str:  # type: ignore[no-untyped-def]
            return a  # type: ignore[no-any-return]

        _ = StreamingCsvEditor(["a"], ["a"], fn1)

    # return type not annotated
    with pytest.raises(ValueError):

        def fn2(a: str):  # type: ignore[no-untyped-def]
            return a

        _ = StreamingCsvEditor(["a"], ["a"], fn2)


def test_raises_for_unsupported_annotations() -> None:
    # int not supported
    with pytest.raises(ValueError):

        def fn1(a: str, b: int) -> str:
            return a + str(b)

        _ = StreamingCsvEditor(["a", "b"], ["a"], fn1)

    # combination of List and str
    with pytest.raises(ValueError):

        def fn2(a: List[str], b: str) -> str:
            return a[0] + b

        _ = StreamingCsvEditor(["a", "b"], ["a"], fn2)
