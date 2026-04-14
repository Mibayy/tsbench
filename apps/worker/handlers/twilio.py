"""Handler: twilio."""
from apps.worker.dispatcher import Dispatcher

_dispatcher = Dispatcher()

def handle_twilio_event(event: dict) -> dict:
    """Incoming twilio webhook handler."""
    return _dispatcher.dispatch('webhook', event)
