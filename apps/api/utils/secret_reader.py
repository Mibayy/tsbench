"""Reads some env vars."""
import os


def get_secret_config() -> dict:
    """Load secret config (reads SECRET_UNDECLARED_TOKEN)."""
    return {
        "token": os.environ.get("SECRET_UNDECLARED_TOKEN", ""),
        "region": os.environ.get("TSBENCH_HIDDEN_REGION", "us-east-1"),
    }
