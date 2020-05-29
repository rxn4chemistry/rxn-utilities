"""Error handling utilities."""
import sys
import traceback
from typing import Dict


def handle_exception(message: str) -> Dict:
    """
    Handle an exception returning a dictionary.

    Args:
        message (str): error message to print.

    Returns:
        Dict: dictionart containing: tile, details and tracback.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return {
        'title': '{}: {}'.format(message, str(exc_type.__name__)),  # type:ignore
        'traceback': traceback.format_exception(
            exc_type, exc_value, exc_traceback
        ),
        'details': str(exc_value)
    }
