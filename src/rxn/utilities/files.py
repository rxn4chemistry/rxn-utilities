import csv
import errno
import os
import random
import shutil
import sys
import tempfile
from contextlib import ExitStack, contextmanager
from pathlib import Path
from typing import Iterable, Iterator, List, Tuple, Union

from typing_extensions import TypeAlias

from .basic import temporary_random_seed
from .containers import all_identical

PathLike: TypeAlias = Union[str, os.PathLike]


def load_list_from_file(filename: PathLike) -> List[str]:
    return list(iterate_lines_from_file(filename))


def iterate_lines_from_file(filename: PathLike) -> Iterator[str]:
    with open(filename, "rt") as f:
        for line in f:
            yield line.rstrip("\r\n")


def dump_list_to_file(values: Iterable[str], filename: PathLike) -> None:
    with open(filename, "wt") as f:
        for v in values:
            f.write(f"{v}\n")


def count_lines(filename: PathLike) -> int:
    return sum(1 for _ in open(filename))


def iterate_tuples_from_files(
    filenames: List[PathLike],
) -> Iterator[Tuple[str, ...]]:
    """
    Read from several files at once, and put the values from the same lines numbers
    into tuples.

    Args:
        filenames: files to read.

    Returns:
        iterator over the generated tuples.
    """
    # Make sure the files have the same lengths. This is not the optimal solution
    # and in principle, one could detect unequal lengths when reading the files.
    # However, an easy solution is available only from Python 3.10:
    # https://stackoverflow.com/q/32954486
    if not all_identical([count_lines(file) for file in filenames]):
        raise ValueError("Not all the files have identical lengths")

    # Opening several files at once;
    # See https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack
    with ExitStack() as stack:
        files = [stack.enter_context(open(fname, "rt")) for fname in filenames]
        iterators = [(line.rstrip("\r\n") for line in f) for f in files]
        yield from zip(*iterators)


def dump_tuples_to_files(
    values: Iterable[Tuple[str, ...]], filenames: List[PathLike]
) -> None:
    """Write tuples to multiple files (1st tuple value ends up in 1st file, etc.).

    Args:
        values: tuples to write to files.
        filenames: files to create.
    """
    # Opening several files at once;
    # See https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack
    with ExitStack() as stack:
        files = [stack.enter_context(open(fname, "wt")) for fname in filenames]
        number_files = len(files)
        for value_tuple in values:
            if len(value_tuple) != number_files:
                raise ValueError(
                    f"Tuple {value_tuple} has incorrect size (expected: {number_files})."
                )
            for value, f in zip(value_tuple, files):
                f.write(f"{value}\n")


def stable_shuffle(input_file: PathLike, output_file: PathLike, seed: int) -> None:
    """
    Shuffle a file in a deterministic order (the same seed always reorders
    files of the same number of lines identically).

    Useful, as an example, to shuffle a source and target files identically.
    """

    # Note we use the context manager to avoid side effects of setting the seed.
    with temporary_random_seed(seed):
        lines = load_list_from_file(input_file)
        random.shuffle(lines)
        dump_list_to_file(lines, output_file)


@contextmanager
def named_temporary_path(delete: bool = True) -> Iterator[Path]:
    """
    Get the path for a temporary file or directory, without creating it (can
    be especially useful in tests).

    This is similar to tempfile.NamedTemporaryFile, when the file is not
    to be actually opened, and one is just interested in obtaining a writable /
    readable path to optionally delete at the end of the context.

    This function was originally created to bypass a limitation of NamedTemporaryFile
    on Windows (https://stackoverflow.com/q/23212435), which becomes relevant when
    one does not want the file to be opened automatically. The solution is
    inspired by https://stackoverflow.com/a/58955530.

    Args:
        delete: whether to delete the file when exiting the context

    Examples:
        >>> with named_temporary_path() as temporary_path:
        ...     # do something on the temporary path.
        ...     # The file or directory at that path will be deleted at the
        ...     # end of the context, except if delete=False.
    """

    base_temp_dir = Path(tempfile.gettempdir())
    temporary_path = base_temp_dir / os.urandom(24).hex()
    try:
        yield temporary_path
    finally:
        if delete and temporary_path.exists():
            if temporary_path.is_file():
                temporary_path.unlink()
            else:
                shutil.rmtree(temporary_path)


@contextmanager
def named_temporary_directory(delete: bool = True) -> Iterator[Path]:
    """
    Get the path for a temporary directory and create it.

    Relies on ``named_temporary_path`` to provide a context manager that will
    automatically delete the directory when leaving the context.

    Args:
        delete: whether to delete the file when exiting the context

    Examples:
        >>> with named_temporary_directory() as temporary_directory:
        ...     # do something with the temporary directory.
        ...     # The directory will be deleted at the
        ...     # end of the context, except if delete=False.
    """

    with named_temporary_path(delete=delete) as path:
        path.mkdir()
        yield path


def is_pathname_valid(pathname: PathLike) -> bool:
    """
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.

    Copied from https://stackoverflow.com/a/34102855. More details there.
    """
    pathname = str(pathname)
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        _, pathname = os.path.splitdrive(pathname)

        root_dirname = (
            os.environ.get("HOMEDRIVE", "C:")
            if sys.platform == "win32"
            else os.path.sep
        )
        assert os.path.isdir(root_dirname)

        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as exc:
                if hasattr(exc, "winerror"):
                    error_invalid_name = 123
                    if exc.winerror == error_invalid_name:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError:
        return False
    else:
        return True


def is_path_creatable(pathname: PathLike) -> bool:
    """
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.

    Copied from https://stackoverflow.com/a/34102855. More details there.
    """
    pathname = str(pathname)
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


def is_path_exists_or_creatable(pathname: PathLike) -> bool:
    """
    `True` if the passed pathname is a valid pathname for the current OS _and_
    either currently exists or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.

    Copied from https://stackoverflow.com/a/34102855. More details there.
    """
    pathname = str(pathname)
    try:
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname)
        )
    except OSError:
        return False


def paths_are_identical(*paths: PathLike) -> bool:
    """Whether paths, possibly given in a mix of absolute and relative formats,
    point to the same file."""
    real_paths = {os.path.realpath(p) for p in paths}
    return len(real_paths) == 1


def raise_if_paths_are_identical(*paths: PathLike) -> None:
    """
    Raise an exception if input and output paths point to the same file.
    """
    if paths_are_identical(*paths):
        paths_str = ", ".join(f'"{p}"' for p in paths)
        raise ValueError(f"The paths {paths_str} must be different.")


def ensure_directory_exists_and_is_empty(directory: Path) -> None:
    """Create a directory if it does not exist already, and raise if not empty."""
    directory.mkdir(parents=True, exist_ok=True)
    directory_contains_files = any(directory.iterdir())
    if directory_contains_files:
        raise RuntimeError(f'The directory "{directory}" is required to be empty.')


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
