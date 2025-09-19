from collections.abc import Iterator
import os
import sys

# Ensure project root is on sys.path so 'import backend.*' works
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import create_app
from backend.app.db.base import Base
# Ensure models are imported so metadata is populated
from backend.app.db import models as _models  # noqa: F401
from backend.app.deps.db import get_db


@pytest.fixture(scope="session")
def engine():
    eng = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=eng)
    return eng


@pytest.fixture()
def db_session(engine) -> Iterator:
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def app(db_session):
    app = create_app()

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    return app


@pytest.fixture()
def client(app):
    return TestClient(app)
