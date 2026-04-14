"""Error classes."""


class TsbenchError(Exception):
    """Base error."""


class NotFoundError(TsbenchError):
    """Resource not found."""


class PermissionDenied(TsbenchError):
    """Caller does not have permission."""


class ValidationError(TsbenchError):
    """Invalid input."""
