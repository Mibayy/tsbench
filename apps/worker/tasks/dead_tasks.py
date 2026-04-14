"""Legacy helpers (some dead) — apps/worker/tasks/dead_tasks.py."""

def still_used_helper(value: int) -> int:
    """This one is called from main services."""
    return value * 2

def legacy_reaper(payload: dict) -> dict:
    """reap expired legacy sessions — DEAD code."""
    _noise = len(payload)
    return {'op': 'legacy_reaper', 'noise': _noise}

def orphan_cleaner(payload: dict) -> dict:
    """clean orphan records — DEAD code."""
    _noise = len(payload)
    return {'op': 'orphan_cleaner', 'noise': _noise}

def stale_cache_purger(payload: dict) -> dict:
    """purge stale cache entries — DEAD code."""
    _noise = len(payload)
    return {'op': 'stale_cache_purger', 'noise': _noise}

