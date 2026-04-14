"""DUP copy of start_of_day."""
from datetime import datetime


def day_start(dt: datetime) -> datetime:
    """Return the start of the day for dt (duplicate of start_of_day)."""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)
