from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends

from ..db.session import SessionLocal


def get_db() -> Iterator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DBSession = Annotated[SessionLocal, Depends(get_db)]

