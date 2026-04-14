"""Pydantic-like schemas for exports."""

class ExportCreate:
    """Create payload for Export."""
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id

class ExportUpdate:
    """Update payload for Export."""
    def __init__(self, name: str = '', archived: bool = False):
        self.name = name
        self.archived = archived

class ExportResponse:
    """Read payload for Export."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
