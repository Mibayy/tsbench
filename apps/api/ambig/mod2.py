"""AMBIG-001 part 2."""


def create_user(tenant_id: int, email: str) -> dict:
    """Create a tenant user (AMBIG target 1/2)."""
    return {"tenant_id": tenant_id, "email": email, "module": "mod2"}


def process_event(kind: str, payload: dict) -> dict:
    """Process an event (AMBIG target 2/2)."""
    return {"kind": kind, "payload": payload, "module": "mod2"}
