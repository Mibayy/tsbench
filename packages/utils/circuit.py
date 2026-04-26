import threading
import time


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

    def __init__(self, failure_threshold: int = 5, reset_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self._state = self.CLOSED
        self._failures = 0
        self._opened_at = 0.0
        self._lock = threading.Lock()

    def _transition_if_ready(self):
        if self._state == self.OPEN and (time.monotonic() - self._opened_at) >= self.reset_timeout:
            self._state = self.HALF_OPEN

    def call(self, fn, *args, **kwargs):
        with self._lock:
            self._transition_if_ready()
            if self._state == self.OPEN:
                raise CircuitOpenError("Circuit is OPEN")
            current_state = self._state

        try:
            result = fn(*args, **kwargs)
        except Exception:
            with self._lock:
                if current_state == self.HALF_OPEN:
                    self._state = self.OPEN
                    self._opened_at = time.monotonic()
                else:
                    self._failures += 1
                    if self._failures >= self.failure_threshold:
                        self._state = self.OPEN
                        self._opened_at = time.monotonic()
            raise

        with self._lock:
            if current_state == self.HALF_OPEN:
                self._state = self.CLOSED
            self._failures = 0
        return result
