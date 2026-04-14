"""Handler: stripe."""
from apps.worker.dispatcher import Dispatcher

_dispatcher = Dispatcher()

def handle_stripe_event(event: dict) -> dict:
    """Incoming stripe webhook handler."""
    return _dispatcher.dispatch('webhook', event)
