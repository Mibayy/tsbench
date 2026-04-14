"""Pydantic-like schemas for notifications."""

class NotificationCreate:
    """Create payload for Notification."""
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id

class NotificationUpdate:
    """Update payload for Notification."""
    def __init__(self, name: str = '', archived: bool = False):
        self.name = name
        self.archived = archived

class NotificationResponse:
    """Read payload for Notification."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
