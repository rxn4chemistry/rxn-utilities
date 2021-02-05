# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

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
        Dict: dictionary containing: tile, detail and tracback.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return {
        'title': '{}: {}'.format(message, str(exc_type.__name__)),  # type:ignore
        'traceback': traceback.format_exception(exc_type, exc_value, exc_traceback),
        'detail': str(exc_value)
    }
