import errno
import os
import shutil
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Iterable, Iterator, List, Union

from typing_extensions import TypeAlias

PathLike: TypeAlias = Union[str, os.PathLike]


def load_list_from_file(filename: PathLike) -> List[str]:
    return list(iterate_lines_from_file(filename))


def iterate_lines_from_file(filename: PathLike) -> Generator[str, None, None]:
    with open(filename, "rt") as f:
        for line in f:
            yield line.strip()


def dump_list_to_file(values: Iterable[str], filename: PathLike) -> None:
    with open(filename, "wt") as f:
        for v in values:
            f.write(f"{v}\n")


def count_lines(filename: PathLike) -> int:
    return sum(1 for _ in open(filename))


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
                    if exc.winerror == error_invalid_name:  # type: ignore
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
