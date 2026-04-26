"""Debounce decorator for rate-limiting function calls."""

import functools
import threading
from typing import Any, Callable, TypeVar


F = TypeVar("F", bound=Callable[..., Any])


def debounce(wait: float):
    """
    Decorator: delay calling the wrapped function by `wait` seconds.
    If called again before `wait` elapses, the previous pending call
    is cancelled and a new timer starts. Thread-safe via a lock.
    """
    def decorator(fn):
        lock = threading.Lock()
        state = {"timer": None}

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            with lock:
                timer = state["timer"]
                if timer is not None:
                    timer.cancel()
                new_timer = threading.Timer(wait, fn, args=args, kwargs=kwargs)
                new_timer.daemon = True
                state["timer"] = new_timer
                new_timer.start()

        def cancel():
            with lock:
                if state["timer"] is not None:
                    state["timer"].cancel()
                    state["timer"] = None

        wrapper.cancel = cancel
        return wrapper

    return decorator
