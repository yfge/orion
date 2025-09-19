import uuid

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    func,
)
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
        back_populates="business_system", cascade="all, delete-orphan"
    )


class NotificationAPI(Base, BaseFieldsMixin):
    __tablename__ = "notification_apis"

    notification_api_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    business_system_id: Mapped[int] = mapped_column(
        ForeignKey("business_systems.id", ondelete="RESTRICT"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    endpoint_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    request_schema: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    response_schema: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    business_system: Mapped[BusinessSystem] = relationship(back_populates="apis")
    dispatches: Mapped[list["MessageDispatch"]] = relationship(
        back_populates="notification_api", cascade="all, delete-orphan"
    )


class MessageDefinition(Base, BaseFieldsMixin):
    __tablename__ = "message_definitions"

    message_definition_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    schema: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    dispatches: Mapped[list["MessageDispatch"]] = relationship(
        back_populates="message_definition", cascade="all, delete-orphan"
    )


class MessageDispatch(Base, BaseFieldsMixin):
    __tablename__ = "message_dispatches"

    message_dispatch_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    message_definition_id: Mapped[int] = mapped_column(
        ForeignKey("message_definitions.id", ondelete="RESTRICT"), nullable=False
    )
    notification_api_id: Mapped[int] = mapped_column(
        ForeignKey("notification_apis.id", ondelete="RESTRICT"), nullable=False
    )
    mapping: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, server_default="1", nullable=False)

    message_definition: Mapped[MessageDefinition] = relationship(back_populates="dispatches")
    notification_api: Mapped[NotificationAPI] = relationship(back_populates="dispatches")


class SendRecord(Base, BaseFieldsMixin):
    __tablename__ = "send_records"

    send_record_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    message_definition_id: Mapped[int] = mapped_column(
        ForeignKey("message_definitions.id", ondelete="RESTRICT"), nullable=False
    )
    notification_api_id: Mapped[int] = mapped_column(
        ForeignKey("notification_apis.id", ondelete="RESTRICT"), nullable=False
    )
    send_time: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)

    details: Mapped[list["SendDetail"]] = relationship(
        back_populates="send_record", cascade="all, delete-orphan"
    )


class SendDetail(Base, BaseFieldsMixin):
    __tablename__ = "send_details"

    send_detail_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    send_record_id: Mapped[int] = mapped_column(
        ForeignKey("send_records.id", ondelete="CASCADE"), nullable=False
    )
    notification_api_id: Mapped[int] = mapped_column(
        ForeignKey("notification_apis.id", ondelete="RESTRICT"), nullable=False
    )
    attempt_no: Mapped[int] = mapped_column(Integer, server_default="1", nullable=False)
    request_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    response_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    sent_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    send_record: Mapped[SendRecord] = relationship(back_populates="details")


class User(Base, BaseFieldsMixin):
    __tablename__ = "users"

    user_bid: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, default=gen_bid, nullable=False
    )
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
