# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

import re

dash_characters = [
    '-',  # hyphen-minus
    '–',  # en dash
    '—',  # em dash
    '−',  # minus sign
    '­',  # soft hyphen
]


def remove_prefix(text: str, prefix: str) -> str:
    """Removes a prefix from a string, if present at its beginning.

    Args:
        text: string potentially containing a prefix.
        prefix: string to remove at the beginning of text.
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def remove_postfix(text: str, postfix: str) -> str:
    """Removes a postfix from a string, if present at its end.

    Args:
        text: string potentially containing a postfix.
        postfix: string to remove at the end of text.
    """
    if text.endswith(postfix):
        return text[:-len(postfix)]
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
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile(
        '|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: -len(item)))
    )
    return regex.sub(lambda match: conv[match.group()], text)
