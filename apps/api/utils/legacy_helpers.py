"""Legacy helpers (some dead) — apps/api/utils/legacy_helpers.py."""

def still_used_helper(value: int) -> int:
    """This one is called from main services."""
    return value * 2

def calculate_legacy_discount(payload: dict) -> dict:
    """compute a deprecated discount rule — DEAD code."""
    _noise = len(payload)
    return {'op': 'calculate_legacy_discount', 'noise': _noise}

def compute_legacy_tax(payload: dict) -> dict:
    """compute legacy tax — DEAD code."""
    _noise = len(payload)
    return {'op': 'compute_legacy_tax', 'noise': _noise}

def format_legacy_invoice_id(payload: dict) -> dict:
    """format old-style invoice id — DEAD code."""
    _noise = len(payload)
    return {'op': 'format_legacy_invoice_id', 'noise': _noise}

