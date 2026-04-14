"""Pydantic-like schemas for audit."""

class AuditCreate:
    """Create payload for Audit."""
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id

class AuditUpdate:
    """Update payload for Audit."""
    def __init__(self, name: str = '', archived: bool = False):
        self.name = name
        self.archived = archived

class AuditResponse:
    """Read payload for Audit."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
