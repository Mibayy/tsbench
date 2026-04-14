"""Caller 4 of hub_util."""
from packages.utils.targeted import hub_util

def do_it_4(payload: dict) -> dict:
    """Invoke hub_util."""
    return hub_util(payload)
