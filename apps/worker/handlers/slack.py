"""Handler: slack."""
from apps.worker.dispatcher import Dispatcher

_dispatcher = Dispatcher()

def handle_slack_event(event: dict) -> dict:
    """Incoming slack webhook handler."""
    return _dispatcher.dispatch('webhook', event)
