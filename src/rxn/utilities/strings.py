import re

dash_characters = [
    "-",  # hyphen-minus
    "–",  # en dash
    "—",  # em dash
    "−",  # minus sign
    "­",  # soft hyphen
]


def remove_prefix(text: str, prefix: str, raise_if_missing: bool = False) -> str:
    """Removes a prefix from a string, if present at its beginning.

    Args:
        text: string potentially containing a prefix.
        prefix: string to remove at the beginning of text.
        raise_if_missing: whether to raise a ValueError if the prefix is not found.

    Raises:
        ValueError: if the prefix is not found and raise_if_missing is True.
    """
    if text.startswith(prefix):
        return text[len(prefix) :]

    if raise_if_missing:
        raise ValueError(f'Prefix "{prefix}" not found in "{text}".')

    return text


def remove_postfix(text: str, postfix: str, raise_if_missing: bool = False) -> str:
    """Removes a postfix from a string, if present at its end.

    Args:
        text: string potentially containing a postfix.
        postfix: string to remove at the end of text.
        raise_if_missing: whether to raise a ValueError if the postfix is not found.

    Raises:
        ValueError: if the postfix is not found and raise_if_missing is True.
    """
    if text.endswith(postfix):
        return text[: -len(postfix)]

    if raise_if_missing:
        raise ValueError(f'Postfix "{postfix}" not found in "{text}".')

    return text


def escape_latex(text: str) -> str:
    r"""
    Escape special LaTex characters in a string.

    Adapted from https://stackoverflow.com/a/25875504.

    Example: will convert "30%" to "30\%".

    Args:
        text: string to escape.

    Returns:
        The message escaped to appear correctly in LaTeX.
    """
    conv = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "\\": r"\textbackslash{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }
    regex = re.compile(
        "|".join(
            re.escape(str(key))
            for key in sorted(conv.keys(), key=lambda item: -len(item))
        )
    )
    return regex.sub(lambda match: conv[match.group()], text)
