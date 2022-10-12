import functools
import logging
from typing import Callable, TypeVar

from diskcache import Cache
from typing_extensions import ParamSpec

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

Params = ParamSpec("Params")
ReturnType = TypeVar("ReturnType")


def cached_on_disk(func: Callable[Params, ReturnType]) -> Callable[Params, ReturnType]:
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
    def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> ReturnType:
        logger.debug(
            f"Cache miss: function {func.__name__}, args: {args}, kwargs: {kwargs}."
        )

        return func(*args, **kwargs)

    return cache.memoize()(wrapper)  # type: ignore
