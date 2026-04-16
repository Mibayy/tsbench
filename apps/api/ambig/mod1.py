"""AMBIG-001 part 1."""


def create_regular_user(email: str, role: str = "member") -> dict:
    """Create a regular user (AMBIG target 1/2)."""
    return {"email": email, "role": role, "module": "mod1"}


def process_event(event: dict) -> dict:
    """Process an event (AMBIG target 2/2)."""
    return {"event": event, "module": "mod1"}
