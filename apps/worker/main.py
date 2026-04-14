"""Worker entrypoint."""
from apps.worker.dispatcher import Dispatcher


def main() -> int:
    """Start the worker loop."""
    d = Dispatcher()
    d.run_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
