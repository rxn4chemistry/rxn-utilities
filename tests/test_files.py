from pathlib import Path

import pytest

from rxn.utilities.files import (
    count_lines,
    dump_list_to_file,
    dump_tuples_to_files,
    ensure_directory_exists_and_is_empty,
    is_path_creatable,
    iterate_csv_column,
    iterate_tuples_from_files,
    load_list_from_file,
    named_temporary_directory,
    named_temporary_path,
    paths_are_identical,
    raise_if_paths_are_identical,
    stable_shuffle,
)


def test_named_temporary_path() -> None:
    # Basic checks when no file or directory is created at that path
    with named_temporary_path() as path:
        assert is_path_creatable(path)
        assert not path.exists()
    assert not path.exists()

    # create file, make sure it is deleted
    with named_temporary_path() as path:
        path.touch()
        assert path.exists()
    assert not path.exists()

    # create file, without deleting it
    with named_temporary_path(delete=False) as path:
        path.touch()
        assert path.exists()
    assert path.exists()

    # create directory with no files, make sure it is deleted
    with named_temporary_path() as path:
        path.mkdir()
        assert path.exists()
    assert not path.exists()

    # create directory with files and directories, make sure it is deleted
    with named_temporary_path() as path:
        path.mkdir()
        (path / "foo").mkdir()
        (path / "foo" / "bar").touch()
        (path / "foo.bar").touch()
        assert set(path.iterdir()) == {path / "foo", path / "foo.bar"}
    assert not path.exists()

    # create directory with files and directories, without deleting
    with named_temporary_path(delete=False) as path:
        path.mkdir()
        (path / "foo").mkdir()
        (path / "foo" / "bar").touch()
        (path / "foo.bar").touch()
        assert set(path.iterdir()) == {path / "foo", path / "foo.bar"}
    assert set(path.iterdir()) == {path / "foo", path / "foo.bar"}


def test_named_temporary_directory() -> None:
    # Basic checks - empty directory, deleted automatically
    with named_temporary_directory() as path:
        assert path.exists()
        assert path.is_dir()
        is_empty = not any(path.iterdir())
        assert is_empty
    assert not path.exists()

    # create directory, without deleting it
    with named_temporary_directory(delete=False) as path:
        pass
    assert path.exists()

    # create directory with files and directories, make sure it is deleted
    with named_temporary_directory() as path:
        (path / "foo").mkdir()
        (path / "foo" / "bar").touch()
        (path / "foo.bar").touch()
        assert set(path.iterdir()) == {path / "foo", path / "foo.bar"}
    assert not path.exists()

    # create directory with files and directories, without deleting
    with named_temporary_directory(delete=False) as path:
        (path / "foo").mkdir()
        (path / "foo" / "bar").touch()
        (path / "foo.bar").touch()
        assert set(path.iterdir()) == {path / "foo", path / "foo.bar"}
    assert set(path.iterdir()) == {path / "foo", path / "foo.bar"}


def test_dump_and_load_list() -> None:
    original_list = ["some", "random", "words", " with", "    ", "spaces  "]

    with named_temporary_path() as tmp_path:
        dump_list_to_file(original_list, tmp_path)
        loaded_list = load_list_from_file(tmp_path)

    assert loaded_list == original_list

    # Test that it works with different newline characters
    hardcoded_newline_characters = "some\nrandom\nwords\n with\n    \nspaces  "
    for newline_character in ["\r", "\r\n", "\n"]:
        with named_temporary_path() as tmp_path:
            with open(tmp_path, "w", newline=newline_character) as f:
                f.write(hardcoded_newline_characters)
            loaded_list = load_list_from_file(tmp_path)
        assert loaded_list == original_list


def test_dump_and_load_tuples() -> None:
    original_tuples = [
        ("a1", "b1", "c1"),
        ("a2", "b2", "c2"),
        ("a3", "b3", "c3"),
        ("a4", "b4", "c4"),
    ]
    with named_temporary_path() as p1, named_temporary_path() as p2, named_temporary_path() as p3:
        dump_tuples_to_files(original_tuples, [p1, p2, p3])
        loaded_tuples = list(iterate_tuples_from_files([p1, p2, p3]))
        first_file_list = load_list_from_file(p1)

    assert loaded_tuples == original_tuples
    assert first_file_list == ["a1", "a2", "a3", "a4"]


def test_load_tuples_inconsistent_line_counts() -> None:
    with named_temporary_path() as p1, named_temporary_path() as p2, named_temporary_path() as p3:
        # The third file has one line more
        dump_list_to_file(["a", "b", "c"], p1)
        dump_list_to_file(["a", "b", "c"], p2)
        dump_list_to_file(["a", "b", "c", "d"], p3)
        with pytest.raises(ValueError):
            _ = list(iterate_tuples_from_files([p1, p2, p3]))

        # Now the third file has one line too few
        dump_list_to_file(["a", "b"], p3)
        with pytest.raises(ValueError):
            _ = list(iterate_tuples_from_files([p1, p2, p3]))


def test_dump_tuples_incorrect_sizes() -> None:
    too_long_tuple = [
        ("a", "b", "c"),
        ("a", "b", "c", "d"),
        ("a", "b", "c"),
    ]

    too_short_tuple = [
        ("a", "b", "c"),
        ("a", "b", "c", "d"),
        ("a", "b", "c"),
    ]

    with named_temporary_path() as p1, named_temporary_path() as p2, named_temporary_path() as p3:
        with pytest.raises(ValueError):
            dump_tuples_to_files(too_long_tuple, [p1, p2, p3])

        with pytest.raises(ValueError):
            dump_tuples_to_files(too_short_tuple, [p1, p2, p3])


def test_count_lines() -> None:
    lines = ["dummy", "dumm", "dum"]
    with named_temporary_path() as tmp_path:
        dump_list_to_file(lines, tmp_path)

        # Test with argument given as str and Path
        assert count_lines(str(tmp_path)) == len(lines)
        assert count_lines(tmp_path) == len(lines)


def test_stable_shuffle() -> None:
    # We will generate a few files based on tuples of values (all "a*" go to the
    # first file, "b*" to the second, etc). Then we check that after stable-shuffling,
    # the tuples still match (all "*1" together, etc.).
    original_tuples = [(f"a{i}", f"b{i}", f"c{i}") for i in range(1, 21)]
    with named_temporary_path() as p1, named_temporary_path() as p2, named_temporary_path() as p3:
        dump_tuples_to_files(original_tuples, [p1, p2, p3])

        # we shuffle the files in-place with the same seed
        stable_shuffle(p1, p1, 42)
        stable_shuffle(p2, p2, 42)
        stable_shuffle(p3, p3, 42)
        loaded_tuples = list(iterate_tuples_from_files([p1, p2, p3]))
        # The lists must be different, but their set identical
        assert loaded_tuples != original_tuples
        assert set(loaded_tuples) == set(original_tuples)

        # Control: re-shuffle but with different seeds -> the tuples will be mixed
        stable_shuffle(p1, p1, 42)
        stable_shuffle(p2, p2, 43)
        stable_shuffle(p3, p3, 44)
        loaded_tuples = list(iterate_tuples_from_files([p1, p2, p3]))
        assert set(loaded_tuples) != set(original_tuples)


def test_paths_are_identical() -> None:
    assert paths_are_identical("f.txt", "f.txt")
    assert paths_are_identical("f.txt", Path("f.txt"))

    # relative path vs path built from cwd()
    assert paths_are_identical("f.txt", Path.cwd() / "f.txt")

    # relative path vs path going into dir and back
    assert paths_are_identical("f.txt", "b/../f.txt")

    assert not paths_are_identical("f.txt", Path("f.txt"), "g.txt")
    assert not paths_are_identical("f.txt", "f.csv")
    assert not paths_are_identical("f.txt", "g.txt")
    assert not paths_are_identical("f.txt", "b/f.txt")


def test_raise_if_paths_are_identical() -> None:
    # No exception
    raise_if_paths_are_identical("f.txt", "f.csv")

    with pytest.raises(ValueError):
        raise_if_paths_are_identical("f.txt", Path.cwd() / "f.txt")


def test_ensure_directory_exists_and_is_empty() -> None:
    path: Path
    with named_temporary_path() as path:
        # Calling the function on the path creates it as a directory
        assert not path.exists()
        ensure_directory_exists_and_is_empty(path)
        assert path.exists()
        assert path.is_dir()

        # Calling it a second time does nothing
        ensure_directory_exists_and_is_empty(path)

        # Creating a file inside it and calling it again -> will fail
        (path / "foo").touch()
        with pytest.raises(RuntimeError):
            ensure_directory_exists_and_is_empty(path)


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
