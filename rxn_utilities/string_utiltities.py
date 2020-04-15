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
