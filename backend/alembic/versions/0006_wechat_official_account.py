"""wechat official account domain tables

Revision ID: 0006
Revises: 0005
Create Date: 2025-10-16

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "wechat_official_account_tokens",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("status", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("wechat_token_bid", sa.String(length=32), nullable=False),
        sa.Column("app_id", sa.String(length=64), nullable=False),
        sa.Column("access_token", sa.String(length=512), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("environment", sa.String(length=32), nullable=True),
        sa.Column("trace_id", sa.String(length=64), nullable=True),
        sa.UniqueConstraint("app_id", name="uq_wechat_official_account_tokens_app_id"),
    )
    op.create_index(
        "ix_wechat_official_account_tokens_wechat_token_bid",
        "wechat_official_account_tokens",
        ["wechat_token_bid"],
        unique=True,
    )
    op.create_index(
        "ix_wechat_official_account_tokens_app_id",
        "wechat_official_account_tokens",
        ["app_id"],
        unique=False,
    )

    op.create_table(
        "wechat_official_account_messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("status", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("wechat_message_bid", sa.String(length=32), nullable=False),
        sa.Column("send_record_bid", sa.String(length=32), nullable=False),
        sa.Column("app_id", sa.String(length=64), nullable=False),
        sa.Column("to_user", sa.String(length=128), nullable=False),
        sa.Column("template_id", sa.String(length=64), nullable=False),
        sa.Column("language", sa.String(length=16), nullable=True),
        sa.Column("link_type", sa.String(length=16), nullable=True),
        sa.Column("link_url", sa.String(length=1024), nullable=True),
        sa.Column("mini_program_app_id", sa.String(length=64), nullable=True),
        sa.Column("mini_program_path", sa.String(length=255), nullable=True),
        sa.Column("data_payload", sa.JSON(), nullable=True),
        sa.Column("raw_request", sa.JSON(), nullable=True),
        sa.Column("state", sa.String(length=32), server_default=sa.text("'pending'"), nullable=False),
        sa.Column("vendor_msg_id", sa.String(length=64), nullable=True),
        sa.Column("last_error_code", sa.Integer(), nullable=True),
        sa.Column("last_error_message", sa.Text(), nullable=True),
        sa.Column("retry_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("queued_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("last_attempt_at", sa.DateTime(), nullable=True),
        sa.Column("idempotency_key", sa.String(length=128), nullable=True),
        sa.UniqueConstraint(
            "send_record_bid", name="uq_wechat_official_account_messages_send_record_bid"
        ),
    )
    op.create_index(
        "ix_wechat_official_account_messages_wechat_message_bid",
        "wechat_official_account_messages",
        ["wechat_message_bid"],
        unique=True,
    )
    op.create_index(
        "ix_wechat_official_account_messages_send_record_bid",
        "wechat_official_account_messages",
        ["send_record_bid"],
        unique=False,
    )
    op.create_index(
        "ix_wechat_official_account_messages_vendor_msg_id",
        "wechat_official_account_messages",
        ["vendor_msg_id"],
        unique=False,
    )
    op.create_index(
        "ix_wechat_official_account_messages_idempotency_key",
        "wechat_official_account_messages",
        ["idempotency_key"],
        unique=False,
    )

    op.create_table(
        "wechat_official_account_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("status", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("wechat_event_bid", sa.String(length=32), nullable=False),
        sa.Column("wechat_message_bid", sa.String(length=32), nullable=True),
        sa.Column("vendor_msg_id", sa.String(length=64), nullable=True),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("status_text", sa.String(length=32), nullable=True),
        sa.Column("error_code", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("raw_message", sa.Text(), nullable=True),
    )
    op.create_index(
        "ix_wechat_official_account_events_wechat_event_bid",
        "wechat_official_account_events",
        ["wechat_event_bid"],
        unique=True,
    )
    op.create_index(
        "ix_wechat_official_account_events_message_bid",
        "wechat_official_account_events",
        ["wechat_message_bid"],
        unique=False,
    )
    op.create_index(
        "ix_wechat_official_account_events_vendor_msg_id",
        "wechat_official_account_events",
        ["vendor_msg_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_wechat_official_account_events_vendor_msg_id", table_name="wechat_official_account_events")
    op.drop_index("ix_wechat_official_account_events_message_bid", table_name="wechat_official_account_events")
    op.drop_index("ix_wechat_official_account_events_wechat_event_bid", table_name="wechat_official_account_events")
    op.drop_table("wechat_official_account_events")

    op.drop_index("ix_wechat_official_account_messages_idempotency_key", table_name="wechat_official_account_messages")
    op.drop_index("ix_wechat_official_account_messages_vendor_msg_id", table_name="wechat_official_account_messages")
    op.drop_index("ix_wechat_official_account_messages_send_record_bid", table_name="wechat_official_account_messages")
    op.drop_index("ix_wechat_official_account_messages_wechat_message_bid", table_name="wechat_official_account_messages")
    op.drop_table("wechat_official_account_messages")

    op.drop_index("ix_wechat_official_account_tokens_app_id", table_name="wechat_official_account_tokens")
    op.drop_index("ix_wechat_official_account_tokens_wechat_token_bid", table_name="wechat_official_account_tokens")
    op.drop_table("wechat_official_account_tokens")
