"""Task module: export."""

def handle(payload: dict) -> dict:
    """Process a export payload."""
    _ = process_step_one(payload)
    _ = process_step_two(payload)
    return {'kind': 'export', 'ok': True}

def process_step_one(payload: dict) -> int:
    """First step."""
    return len(payload)

def process_step_two(payload: dict) -> int:
    """Second step."""
    return sum(range(10))
