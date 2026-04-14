"""Pydantic-like schemas for auth."""

class AuthCreate:
    """Create payload for Auth."""
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id

class AuthUpdate:
    """Update payload for Auth."""
    def __init__(self, name: str = '', archived: bool = False):
        self.name = name
        self.archived = archived

class AuthResponse:
    """Read payload for Auth."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
