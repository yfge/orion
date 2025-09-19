from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..core.security import hash_password
from ..db.models import User


def get_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username, User.is_deleted == False)  # noqa: E712
    return db.execute(stmt).scalar_one_or_none()


def create_user(db: Session, username: str, password: str, email: str | None = None) -> User:
    user = User(username=username, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.flush()
    return user


def list_users(db: Session, limit: int = 50, offset: int = 0) -> list[User]:
    stmt = (
        select(User)
        .where(User.is_deleted == False)  # noqa: E712
        .order_by(User.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.execute(stmt).scalars())

