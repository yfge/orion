from pydantic import BaseModel, Field


class AuthProfileBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: str = Field(min_length=2, max_length=32)  # none|oauth2_client_credentials|hmac|jwt|custom
    config: dict | None = None
    status: int | None = 0


class AuthProfileCreate(AuthProfileBase):
    pass


class AuthProfileUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    type: str | None = Field(default=None, max_length=32)
    config: dict | None = None
    status: int | None = None


class AuthProfileOut(BaseModel):
    auth_profile_bid: str
    name: str
    type: str
    config: dict | None
    status: int

    class Config:
        from_attributes = True


class AuthProfileList(BaseModel):
    items: list[AuthProfileOut]
    total: int
    limit: int
    offset: int

