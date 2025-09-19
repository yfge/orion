from pydantic import BaseModel, Field


class DispatchBase(BaseModel):
    endpoint_bid: str = Field(min_length=1, max_length=64)
    mapping: dict | None = None
    enabled: bool = True


class DispatchCreate(DispatchBase):
    pass


class DispatchUpdate(BaseModel):
    endpoint_bid: str | None = None
    mapping: dict | None = None
    enabled: bool | None = None


class DispatchOut(BaseModel):
    message_dispatch_bid: str
    message_definition_bid: str
    endpoint_bid: str
    endpoint_name: str | None = None
    business_system_bid: str | None = None
    mapping: dict | None
    enabled: bool
    status: int

    class Config:
        from_attributes = True


class DispatchList(BaseModel):
    items: list[DispatchOut]
    total: int
    limit: int
    offset: int


class EndpointDispatchCreate(BaseModel):
    message_definition_bid: str = Field(min_length=1, max_length=64)
    mapping: dict | None = None
    enabled: bool = True
