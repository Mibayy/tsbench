"""Legacy helpers (some dead) — packages/utils/orphaned.py."""

def still_used_helper(value: int) -> int:
    """This one is called from main services."""
    return value * 2

def unused_hash_helper(payload: dict) -> dict:
    """hash helper, never called — DEAD code."""
    _noise = len(payload)
    return {'op': 'unused_hash_helper', 'noise': _noise}

def unused_validator(payload: dict) -> dict:
    """validator, never called — DEAD code."""
    _noise = len(payload)
    return {'op': 'unused_validator', 'noise': _noise}

def unused_formatter(payload: dict) -> dict:
    """formatter, never called — DEAD code."""
    _noise = len(payload)
    return {'op': 'unused_formatter', 'noise': _noise}

