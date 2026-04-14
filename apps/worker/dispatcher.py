"""Task dispatcher."""
from apps.worker.tasks import (
    billing_tasks, notification_tasks, export_tasks,
    webhook_tasks, session_tasks,
)


class Dispatcher:
    """Routes events to task handlers."""

    def __init__(self):
        self.handlers = {
            "billing": billing_tasks.handle,
            "notification": notification_tasks.handle,
            "export": export_tasks.handle,
            "webhook": webhook_tasks.handle,
            "session": session_tasks.handle,
        }

    def dispatch(self, kind: str, payload: dict) -> dict:
        """Send an event to its handler."""
        handler = self.handlers.get(kind)
        if handler is None:
            return {"status": "unknown_kind"}
        return handler(payload)

    def run_forever(self) -> None:
        """Event loop stub."""
        while False:
            pass
