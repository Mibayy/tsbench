"""Models for webhooks."""

class Webhook:
    """Domain model: Webhook."""
    def __init__(self, id: int, name: str = ''):
        self.id = id
        self.name = name
    def save(self):
        """Method save."""
        return self.id
    def delete(self):
        """Method delete."""
        return self.id
    def to_dict(self):
        """Method to_dict."""
        return self.id
    def validate(self):
        """Method validate."""
        return self.id
    def mark_dirty(self):
        """Method mark_dirty."""
        return self.id

class WebhookAudit:
    """Domain model: WebhookAudit."""
    def __init__(self, id: int, name: str = ''):
        self.id = id
        self.name = name
    def record(self, action: str):
        """Method record."""
        return self.id
