import csv
import io


def parse_csv(text: str, *, has_header: bool = True) -> list[dict]:
    buf = io.StringIO(text)
    if has_header:
        reader = csv.DictReader(buf)
        return [dict(row) for row in reader]
    reader = csv.reader(buf)
    return [
        {f"col_{i}": value for i, value in enumerate(row)}
        for row in reader
    ]
