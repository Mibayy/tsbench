from datetime import date, timedelta

from dateutil.relativedelta import relativedelta


def expand_date_range(start: str, end: str, *, step: str = "day") -> list[str]:
    from datetime import date, timedelta
    from dateutil.relativedelta import relativedelta

    start_d = date.fromisoformat(start)
    end_d = date.fromisoformat(end)
    if end_d < start_d:
        raise ValueError("end must be >= start")
    if step not in {"day", "week", "month"}:
        raise ValueError(f"invalid step: {step}")

    result: list[str] = []
    current = start_d
    while current <= end_d:
        result.append(current.isoformat())
        if step == "day":
            current += timedelta(days=1)
        elif step == "week":
            current += timedelta(weeks=1)
        else:
            current += relativedelta(months=1)
    return result
