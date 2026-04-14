"""Date helpers."""
from datetime import datetime, timedelta


def start_of_day(dt: datetime) -> datetime:
    """Return the start of the day for dt."""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(dt: datetime) -> datetime:
    """Return the end of the day for dt."""
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def days_between(a: datetime, b: datetime) -> int:
    """Number of whole days between two datetimes."""
    return abs((a - b).days)
