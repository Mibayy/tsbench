"""Pydantic-like schemas for reports."""

class ReportCreate:
    """Create payload for Report."""
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id

class ReportUpdate:
    """Update payload for Report."""
    def __init__(self, name: str = '', archived: bool = False):
        self.name = name
        self.archived = archived

class ReportResponse:
    """Read payload for Report."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
