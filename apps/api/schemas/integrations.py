"""Pydantic-like schemas for integrations."""

class IntegrationCreate:
    """Create payload for Integration."""
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id

class IntegrationUpdate:
    """Update payload for Integration."""
    def __init__(self, name: str = '', archived: bool = False):
        self.name = name
        self.archived = archived

class IntegrationResponse:
    """Read payload for Integration."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
