# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED
"""Test utilities."""
import os
import tempfile
from types import TracebackType
from typing import Optional, Type


class FileFromContent:
    """
    Create a temporary file with a given content.
    Inspired by: https://stackoverflow.com/a/54053967/10032558.
    """

    def __init__(self, content: str) -> None:
        """
        Initialize the file with a content.

        Args:
            content (str): content of the file.
        """
        self.file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        with self.file as fp:
            fp.write(content)

    @property
    def filename(self) -> str:
        """
        Get the name of the file.

        Returns:
            str: the file name.
        """
        return self.file.name

    def __enter__(self) -> 'FileFromContent':
        """Enter the `with` block."""
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]] = None,
        value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None
    ) -> None:
        """
        Exit the `with` block.

        Args:
            type (Type[BaseException]): the exception type. Defaults to None.
            value (BaseException): the exception. Defaults to None.
            traceback: (TracebackType): the type of the traceback. Defaults to None.
        """
        os.unlink(self.filename)
