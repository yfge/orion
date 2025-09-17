from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    future=True,
    pool_pre_ping=True,  # helps with stale connections (e.g., MySQL timeouts)
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
