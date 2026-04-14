"""Pydantic-like schemas for billing."""

class BillingCreate:
    """Create payload for Billing."""
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id

class BillingUpdate:
    """Update payload for Billing."""
    def __init__(self, name: str = '', archived: bool = False):
        self.name = name
        self.archived = archived

class BillingResponse:
    """Read payload for Billing."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
