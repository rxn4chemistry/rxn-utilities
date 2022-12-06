import random

from rxn.utilities.basic import sandboxed_random_context, temporary_random_seed


def _pick_random_integer() -> int:
    """Helper function picking a random integer; can be used as a proxy to
    check if the random state is the same in different contexts."""
    return random.randint(0, 1000000)


def test_sandboxed_random_context() -> None:
    # To test the sandboxed random context, we do an experiment in which we
    # draw a random number after setting the seed, one time with no intervention
    # in-between, and one time after doing sandboxed random operations.
    # As another check, do the same without sandbox.

    random.seed(42)
    no_intervention = _pick_random_integer()

    random.seed(42)
    with sandboxed_random_context():
        random.seed(1111)
        _ = random.randint(0, 10)
        _ = random.random()
    sandboxed_intervention = _pick_random_integer()

    random.seed(42)
    _ = random.random()
    non_sandboxed_intervention = _pick_random_integer()

    assert no_intervention == sandboxed_intervention
    assert no_intervention != non_sandboxed_intervention


def test_sandboxed_random_context_with_exception() -> None:
    # The random state is also reset if an exception was raised
    random.seed(42)
    no_intervention = _pick_random_integer()

    random.seed(42)
    try:
        with sandboxed_random_context():
            random.seed(1111)
            _ = random.randint(0, 10)
            raise RuntimeError()
    except RuntimeError:
        pass
    sandboxed_intervention = _pick_random_integer()

    assert no_intervention == sandboxed_intervention


def test_temporary_random_seed() -> None:
    # 1) check that the random seed is temporary (sandboxed)
    random.seed(42)
    no_intervention = _pick_random_integer()

    random.seed(42)
    with temporary_random_seed(111):
        _ = random.random()
    sandboxed_intervention = _pick_random_integer()

    assert no_intervention == sandboxed_intervention

    # 2) check that the random seed actually does what we want, i.e. we should
    #    get the same value as before also in the context
    random.seed(1111)
    with temporary_random_seed(42):
        inner_value = _pick_random_integer()
    assert inner_value == no_intervention
