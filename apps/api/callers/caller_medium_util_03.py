"""Caller 3 of medium_util."""
from packages.utils.targeted import medium_util

def do_it_3(payload: dict) -> dict:
    """Invoke medium_util."""
    return medium_util(payload)
