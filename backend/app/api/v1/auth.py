from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...core.security import create_access_token, verify_password
from ...deps.db import get_db
from ...repository.users import create_user, get_by_username
from ...schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserOut


router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if get_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    user = create_user(db, payload.username, payload.password, payload.email)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_by_username(db, payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=user.user_bid)
    return TokenResponse(access_token=token)

