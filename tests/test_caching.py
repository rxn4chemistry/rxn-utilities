import typing

from rxn.utilities.caching import cached_on_disk


@typing.no_type_check  # Note: no type checking because the "f.counter" syntax is hacky.
def test_cached_on_disk() -> None:
    @cached_on_disk
    def f(a: str) -> None:
        """Dummy function doc."""

        # This function variable makes it possible to keep track of how
        # many times it is being called in the test.
        f.counter += 1

    f.counter = 0

    # Docstring is preserved
    assert "Dummy function doc." in f.__doc__

    # Calling the first time increases the counter.
    f("dummy 1")
    assert f.counter == 1

    # Calling a second time with the same argument does not increase it.
    f("dummy 1")
    assert f.counter == 1

    # Calling by kwarg makes a difference.
    # NB: this is not ideal, but diskcache has no mechanism to do better.
    f(a="dummy 1")
    assert f.counter == 2

    # Calling a second time by kwarg keeps the same count.
    f(a="dummy 1")
    assert f.counter == 2

    # Calling with another value increases the counter
    f("dummy 2")
    assert f.counter == 3
