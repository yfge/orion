from pydantic import BaseModel, Field, HttpUrl


class BusinessSystemBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    base_url: str | None = Field(default=None, max_length=1024)
    auth_method: str | None = Field(default=None, max_length=64)
    app_id: str | None = Field(default=None, max_length=255)
    app_secret: str | None = Field(default=None, max_length=255)
    status: int | None = 0


class BusinessSystemCreate(BusinessSystemBase):
    pass


class BusinessSystemUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    base_url: str | None = Field(default=None, max_length=1024)
    auth_method: str | None = Field(default=None, max_length=64)
    app_id: str | None = Field(default=None, max_length=255)
    app_secret: str | None = Field(default=None, max_length=255)
    status: int | None = None


class BusinessSystemOut(BaseModel):
    business_system_bid: str
    name: str
    base_url: str | None = None
    auth_method: str | None = None
    app_id: str | None = None
    app_secret: str | None = None
    status: int

    class Config:
        from_attributes = True


class BusinessSystemList(BaseModel):
    items: list[BusinessSystemOut]
    total: int
    limit: int
    offset: int

