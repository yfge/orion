from pydantic import BaseModel, Field


class EndpointBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    transport: str | None = Field(default="http", max_length=16)
    adapter_key: str | None = Field(default=None, max_length=64)
    endpoint_url: str | None = Field(default=None, max_length=1024)
    config: dict | None = None
    auth_profile_bid: str | None = None
    status: int | None = 0


class EndpointCreate(EndpointBase):
    pass


class EndpointUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    transport: str | None = Field(default=None, max_length=16)
    adapter_key: str | None = Field(default=None, max_length=64)
    endpoint_url: str | None = Field(default=None, max_length=1024)
    config: dict | None = None
    auth_profile_bid: str | None = None
    status: int | None = None


class EndpointOut(BaseModel):
    notification_api_bid: str
    business_system_bid: str | None = None
    name: str
    transport: str | None
    adapter_key: str | None
    endpoint_url: str | None
    config: dict | None
    auth_profile_bid: str | None
    status: int

    class Config:
        from_attributes = True


class EndpointList(BaseModel):
    items: list[EndpointOut]
    total: int
    limit: int
    offset: int


class SendTestRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class SendTestResponse(BaseModel):
    status_code: int
    body: dict | str | None = None
