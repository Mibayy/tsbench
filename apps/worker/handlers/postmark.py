"""Handler: postmark."""
from apps.worker.dispatcher import Dispatcher

_dispatcher = Dispatcher()

def handle_postmark_event(event: dict) -> dict:
    """Incoming postmark webhook handler."""
    return _dispatcher.dispatch('webhook', event)
