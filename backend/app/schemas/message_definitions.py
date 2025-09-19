from pydantic import BaseModel, Field


class MessageDefBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: str | None = Field(default=None, max_length=64)
    schema: dict | None = None
    status: int | None = 0


class MessageDefCreate(MessageDefBase):
    pass


class MessageDefUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    type: str | None = Field(default=None, max_length=64)
    schema: dict | None = None
    status: int | None = None


class MessageDefOut(BaseModel):
    message_definition_bid: str
    name: str
    type: str | None
    schema: dict | None
    status: int

    class Config:
        from_attributes = True


class MessageDefList(BaseModel):
    items: list[MessageDefOut]
    total: int
    limit: int
    offset: int

