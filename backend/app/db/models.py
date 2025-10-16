import uuid

from sqlalchemy import JSON, Boolean, DateTime, Integer, SmallInteger, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


def gen_bid() -> str:
    return uuid.uuid4().hex


class TimestampMixin:
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class BaseFieldsMixin(TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default="0", nullable=False)
    status: Mapped[int] = mapped_column(SmallInteger, server_default="0", nullable=False)


class BusinessSystem(Base, BaseFieldsMixin):
    __tablename__ = "business_systems"

    business_system_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    base_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    auth_method: Mapped[str | None] = mapped_column(String(64), nullable=True)
    app_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    app_secret: Mapped[str | None] = mapped_column(String(255), nullable=True)

    apis: Mapped[list["NotificationAPI"]] = relationship(
        "NotificationAPI",
        viewonly=True,
        primaryjoin="foreign(NotificationAPI.business_system_bid)==BusinessSystem.business_system_bid",
    )


class NotificationAPI(Base, BaseFieldsMixin):
    __tablename__ = "notification_apis"

    notification_api_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    business_system_bid: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    endpoint_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    request_schema: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    response_schema: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Extensibility: transport + adapter + config + optional auth profile
    transport: Mapped[str | None] = mapped_column(String(16), nullable=True)  # e.g., http, mq
    adapter_key: Mapped[str | None] = mapped_column(
        String(64), nullable=True
    )  # e.g., http.generic, mq.kafka
    config: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # adapter-specific
    auth_profile_bid: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)

    business_system: Mapped[BusinessSystem] = relationship(
        back_populates="apis",
        viewonly=True,
        primaryjoin="foreign(NotificationAPI.business_system_bid)==BusinessSystem.business_system_bid",
    )
    dispatches: Mapped[list["MessageDispatch"]] = relationship(
        back_populates="notification_api",
        viewonly=True,
        primaryjoin="foreign(MessageDispatch.notification_api_bid)==NotificationAPI.notification_api_bid",
    )


class Secret(Base, BaseFieldsMixin):
    __tablename__ = "secrets"

    secret_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class AuthProfile(Base, BaseFieldsMixin):
    __tablename__ = "auth_profiles"

    auth_profile_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(32))  # none|oauth2_client_credentials|hmac|jwt|custom
    config: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class MessageDefinition(Base, BaseFieldsMixin):
    __tablename__ = "message_definitions"

    message_definition_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    schema: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    dispatches: Mapped[list["MessageDispatch"]] = relationship(
        back_populates="message_definition",
        viewonly=True,
        primaryjoin="foreign(MessageDispatch.message_definition_bid)==MessageDefinition.message_definition_bid",
    )


class MessageDispatch(Base, BaseFieldsMixin):
    __tablename__ = "message_dispatches"

    message_dispatch_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    message_definition_bid: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    notification_api_bid: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    mapping: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, server_default="1", nullable=False)

    message_definition: Mapped[MessageDefinition] = relationship(
        back_populates="dispatches",
        viewonly=True,
        primaryjoin="foreign(MessageDispatch.message_definition_bid)==MessageDefinition.message_definition_bid",
    )
    notification_api: Mapped[NotificationAPI] = relationship(
        back_populates="dispatches",
        viewonly=True,
        primaryjoin="foreign(MessageDispatch.notification_api_bid)==NotificationAPI.notification_api_bid",
    )


class SendRecord(Base, BaseFieldsMixin):
    __tablename__ = "send_records"

    send_record_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    message_definition_bid: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    notification_api_bid: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    send_time: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)

    details: Mapped[list["SendDetail"]] = relationship(
        back_populates="send_record",
        viewonly=True,
        primaryjoin="foreign(SendDetail.send_record_bid)==SendRecord.send_record_bid",
    )
    wechat_message: Mapped["WechatOfficialAccountMessage"] = relationship(
        viewonly=True,
        uselist=False,
        primaryjoin="foreign(WechatOfficialAccountMessage.send_record_bid)==SendRecord.send_record_bid",
    )


class SendDetail(Base, BaseFieldsMixin):
    __tablename__ = "send_details"

    send_detail_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    send_record_bid: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    notification_api_bid: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    attempt_no: Mapped[int] = mapped_column(Integer, server_default="1", nullable=False)
    request_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    response_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    sent_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    send_record: Mapped[SendRecord] = relationship(
        back_populates="details",
        viewonly=True,
        primaryjoin="foreign(SendDetail.send_record_bid)==SendRecord.send_record_bid",
    )


class User(Base, BaseFieldsMixin):
    __tablename__ = "users"

    user_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)


class ApiKey(Base, BaseFieldsMixin):
    __tablename__ = "api_keys"

    api_key_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    owner_user_bid: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)  # sha256 hex
    prefix: Mapped[str | None] = mapped_column(
        String(16), nullable=True
    )  # first 6-8 chars for display
    suffix: Mapped[str | None] = mapped_column(
        String(16), nullable=True
    )  # last 4-6 chars for display
    description: Mapped[str | None] = mapped_column(Text, nullable=True)



class WechatOfficialAccountToken(Base, BaseFieldsMixin):
    __tablename__ = "wechat_official_account_tokens"
    __table_args__ = (
        UniqueConstraint("app_id", name="uq_wechat_official_account_tokens_app_id"),
    )

    wechat_token_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    app_id: Mapped[str] = mapped_column(String(64), nullable=False)
    access_token: Mapped[str] = mapped_column(String(512), nullable=False)
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    fetched_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    environment: Mapped[str | None] = mapped_column(String(32), nullable=True)
    trace_id: Mapped[str | None] = mapped_column(String(64), nullable=True)


class WechatOfficialAccountMessage(Base, BaseFieldsMixin):
    __tablename__ = "wechat_official_account_messages"
    __table_args__ = (
        UniqueConstraint(
            "send_record_bid", name="uq_wechat_official_account_messages_send_record_bid"
        ),
    )

    wechat_message_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    send_record_bid: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    app_id: Mapped[str] = mapped_column(String(64), nullable=False)
    to_user: Mapped[str] = mapped_column(String(128), nullable=False)
    template_id: Mapped[str] = mapped_column(String(64), nullable=False)
    language: Mapped[str | None] = mapped_column(String(16), nullable=True)
    link_type: Mapped[str | None] = mapped_column(String(16), nullable=True)
    link_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    mini_program_app_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    mini_program_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    data_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    raw_request: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    state: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    vendor_msg_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    last_error_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)
    queued_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    last_attempt_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)

    events: Mapped[list["WechatOfficialAccountEvent"]] = relationship(
        back_populates="message",
        viewonly=True,
        primaryjoin="foreign(WechatOfficialAccountEvent.wechat_message_bid)==WechatOfficialAccountMessage.wechat_message_bid",
    )


class WechatOfficialAccountEvent(Base, BaseFieldsMixin):
    __tablename__ = "wechat_official_account_events"

    wechat_event_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    wechat_message_bid: Mapped[str | None] = mapped_column(String(32), index=True, nullable=True)
    vendor_msg_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    status_text: Mapped[str | None] = mapped_column(String(32), nullable=True)
    error_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    occurred_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    raw_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    message: Mapped[WechatOfficialAccountMessage | None] = relationship(
        back_populates="events",
        viewonly=True,
        primaryjoin="foreign(WechatOfficialAccountEvent.wechat_message_bid)==WechatOfficialAccountMessage.wechat_message_bid",
    )
