import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def setup_celery_logger(
    main_log_file: str = 'worker.log',
    celery_log_file: str = 'celery.log',
    log_level: str = 'INFO'
) -> None:
    """
    Setup logging for celery workers.

    It should be used in `tasks.py` in the following manner:
        >>> from celery.signals import setup_logging
        ... from rxn_utilities.logging_utilities import setup_celery_logger
        ...
        ... @setup_logging.connect
        ... def setup_logger(**kwargs):
        ...     setup_celery_logger()

    Args:
        main_log_file: where the logs (except celery-related) will be written.
        celery_log_file: where the celery-related logs will be written.
        log_level: logging level for main_log_file
    """
    rxn_format = '%(asctime)s %(levelname)-8s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'

    # Logs from the following packages are redirected to their own log file.
    for package in ['celery', 'amqp', 'kombu']:
        package_logger = logging.getLogger(package)
        package_logger.propagate = False
        package_logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(celery_log_file)
        handler.setFormatter(logging.Formatter(rxn_format))
        package_logger.addHandler(handler)

    # The main logger will write logs to a file
    logging.basicConfig(filename=main_log_file, level=log_level, format=rxn_format)


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
