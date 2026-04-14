"""Pydantic-like schemas for members."""

class MemberCreate:
    """Create payload for Member."""
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id

class MemberUpdate:
    """Update payload for Member."""
    def __init__(self, name: str = '', archived: bool = False):
        self.name = name
        self.archived = archived

class MemberResponse:
    """Read payload for Member."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
