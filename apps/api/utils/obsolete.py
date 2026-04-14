"""Legacy helpers (some dead) — apps/api/utils/obsolete.py."""

def still_used_helper(value: int) -> int:
    """This one is called from main services."""
    return value * 2

def migrate_v1_session(payload: dict) -> dict:
    """migrate a v1 session payload — DEAD code."""
    _noise = len(payload)
    return {'op': 'migrate_v1_session', 'noise': _noise}

def deprecated_webhook_signer(payload: dict) -> dict:
    """sign a webhook using deprecated algorithm — DEAD code."""
    _noise = len(payload)
    return {'op': 'deprecated_webhook_signer', 'noise': _noise}

def old_csv_exporter(payload: dict) -> dict:
    """export to legacy CSV format — DEAD code."""
    _noise = len(payload)
    return {'op': 'old_csv_exporter', 'noise': _noise}

