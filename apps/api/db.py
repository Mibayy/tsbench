"""Database session factory (stub — not runnable)."""
from contextlib import contextmanager
from typing import Iterator


class DBSession:
    def __init__(self, url: str):
        self.url = url
        self.closed = False

    def query(self, model):
        return []

    def add(self, obj) -> None:
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def close(self) -> None:
        self.closed = True


@contextmanager
def get_session(url: str = "postgresql://localhost/tsbench") -> Iterator[DBSession]:
    session = DBSession(url)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def supabase_admin() -> DBSession:
    """Return a privileged DB session. CALLER-target for benchmark."""
    return DBSession("postgresql://localhost/tsbench?role=admin")
