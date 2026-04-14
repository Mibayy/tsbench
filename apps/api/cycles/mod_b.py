"""CYCLE-001 part B."""
from apps.api.cycles import mod_a


def b_call():
    """B calls A."""
    return mod_a.a_leaf()
