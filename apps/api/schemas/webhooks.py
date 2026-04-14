"""Pydantic-like schemas for webhooks."""

class WebhookCreate:
    """Create payload for Webhook."""
    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id

class WebhookUpdate:
    """Update payload for Webhook."""
    def __init__(self, name: str = '', archived: bool = False):
        self.name = name
        self.archived = archived

class WebhookResponse:
    """Read payload for Webhook."""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
