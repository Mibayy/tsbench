"""Caller 1 of small_util."""
from packages.utils.targeted import small_util

def do_it_1(payload: dict) -> dict:
    """Invoke small_util."""
    return small_util(payload)
