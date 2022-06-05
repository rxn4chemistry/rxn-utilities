import functools
import logging

from diskcache import Cache

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def cached_on_disk(func):
    """
    Decorator for function cache relying on the disk.

    Useful when functools.cache() or functools.lru_cache() cannot be used
    because of threads (especially in celery workers).

    Simplifies the syntax compared to relying on diskcache only.

    Note that diskcache makes a difference between args and kwargs, i.e. calling
    a function one time by argument and one time by keyword argument will lead
    to the wrapped function body being executed two times.

    Examples:
        >>> @cached_on_disk
        ... def foo(bar: str) -> str:
        ...     # ...

    """
    cache = Cache()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(
            f"Cache miss: function {func.__name__}, args: {args}, kwargs: {kwargs}."
        )

        return func(*args, **kwargs)

    return cache.memoize()(wrapper)
