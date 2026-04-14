"""CYCLE-001 part A."""
from apps.api.cycles import mod_b


def a_call():
    """A calls B."""
    return mod_b.b_call()


def a_leaf():
    """Leaf of A."""
    return 1
