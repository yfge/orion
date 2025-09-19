from pydantic import BaseModel, Field, EmailStr


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    email: EmailStr | None = None
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    user_bid: str
    username: str
    email: str | None = None
    status: int

    class Config:
        from_attributes = True

