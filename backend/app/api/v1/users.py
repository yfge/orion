from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from ...deps.db import get_db
from ...repository.users import list_users
from ...schemas.auth import UserOut
from ...core.security import decode_token


router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user_bid(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if not sub:
            raise ValueError("missing sub")
        return str(sub)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db), _: str = Depends(get_current_user_bid)):
    return list_users(db, limit=100, offset=0)

