"""Pydantic-like schemas for sessions."""

class SessionCreate:
    """Create payload for Session."""
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id

class SessionUpdate:
    """Update payload for Session."""
    def __init__(self, name: str = '', archived: bool = False):
        self.name = name
        self.archived = archived

class SessionResponse:
    """Read payload for Session."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
