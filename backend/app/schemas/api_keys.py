from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ApiKeyCreate(BaseModel):
    name: str
    description: str | None = None


class ApiKeyOut(BaseModel):
    api_key_bid: str
    name: str
    prefix: str | None = None
    suffix: str | None = None
    status: int
    created_at: datetime


class ApiKeyList(BaseModel):
    items: list[ApiKeyOut]
    total: int
    limit: int
    offset: int


class ApiKeyCreateResponse(BaseModel):
    api_key_bid: str
    name: str
    token: str = Field(description="The raw token. Shown only once.")
    prefix: str | None = None
    suffix: str | None = None
