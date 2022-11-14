from rxn.utilities.files import (
    count_lines,
    dump_list_to_file,
    is_path_creatable,
    load_list_from_file,
    named_temporary_path,
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


def test_dump_and_load_list() -> None:
    original_list = ["some", "random", "words"]

    with named_temporary_path() as tmp_path:
        dump_list_to_file(original_list, tmp_path)
        loaded_list = load_list_from_file(tmp_path)

    assert loaded_list == original_list


def test_count_lines() -> None:
    lines = ["dummy", "dumm", "dum"]
    with named_temporary_path() as tmp_path:
        dump_list_to_file(lines, tmp_path)

        # Test with argument given as str and Path
        assert count_lines(str(tmp_path)) == len(lines)
        assert count_lines(tmp_path) == len(lines)
