import logging
from enum import Enum
from typing import Iterable, Union

from rxn.utilities.files import PathLike

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class LoggingFormat(Enum):
    """
    Common logging formats used in the RXN universe.
    """

    BASIC = "[%(asctime)s %(levelname)s] %(message)s"
    DETAILED = (
        "%(asctime)s %(levelname)-7s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
    )


def setup_console_logger(
    level: Union[int, str] = "INFO",
    format: Union[LoggingFormat, str] = LoggingFormat.BASIC,
) -> None:
    """
    Set up a logger writing to the console (i.e., to stderr).

    Args:
        level: log level, either as a string ("INFO") or integer (logging.INFO).
        format: log format, as a LoggingFormat value, or a string directly.
    """
    _setup_logger_from_handlers(
        handlers=[logging.StreamHandler()], level=level, format=format
    )


def setup_file_logger(
    filename: PathLike,
    level: Union[int, str] = "INFO",
    format: Union[LoggingFormat, str] = LoggingFormat.BASIC,
) -> None:
    """
    Set up a logger writing to the given file.

    Overwrites the default file mode 'a' with 'w' (i.e., overwrites the file).

    Args:
        level: log level, either as a string ("INFO") or integer (logging.INFO).
        format: log format, as a LoggingFormat value, or a string directly.
    """
    _setup_logger_from_handlers(
        handlers=[logging.FileHandler(filename, mode="w")], level=level, format=format
    )


def setup_console_and_file_logger(
    filename: PathLike,
    level: Union[int, str] = "INFO",
    format: Union[LoggingFormat, str] = LoggingFormat.BASIC,
) -> None:
    """
    Set up a logger writing to both the terminal and the given file.

    Overwrites the default file mode 'a' with 'w' (i.e., overwrites the file).

    Args:
        level: log level, either as a string ("INFO") or integer (logging.INFO).
        format: log format, as a LoggingFormat value, or a string directly.
    """
    _setup_logger_from_handlers(
        handlers=[logging.FileHandler(filename, mode="w"), logging.StreamHandler()],
        level=level,
        format=format,
    )


def _setup_logger_from_handlers(
    handlers: Iterable[logging.Handler],
    level: Union[int, str],
    format: Union[LoggingFormat, str],
) -> None:
    """
    Helper function to avoid duplication in the other setup functions.

    Args:
        handlers: log handlers.
        level: log level, either as a string ("INFO") or integer (logging.INFO).
        format: log format, as a LoggingFormat value, or a string directly.
    """
    if isinstance(format, LoggingFormat):
        format = format.value
    logging.basicConfig(format=format, level=level, handlers=handlers)


def log_debug(message: str) -> None:
    """
    Utility function to log a message with DEBUG level.

    Can be useful for testing purposes, to test logging capabilities from
    another Python package.
    """
    logger.debug(message)


def log_info(message: str) -> None:
    """
    Utility function to log a message with INFO level.

    Can be useful for testing purposes, to test logging capabilities from
    another Python package.
    """
    logger.info(message)


def log_warning(message: str) -> None:
    """
    Utility function to log a message with WARNING level.

    Can be useful for testing purposes, to test logging capabilities from
    another Python package.
    """
    logger.warning(message)


def log_error(message: str) -> None:
    """
    Utility function to log a message with ERROR level.

    Can be useful for testing purposes, to test logging capabilities from
    another Python package.
    """
    logger.error(message)
