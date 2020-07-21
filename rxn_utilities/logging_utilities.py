import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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
