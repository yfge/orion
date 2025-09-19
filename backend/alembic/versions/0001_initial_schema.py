"""
Initial database schema

Revision ID: 0001
Revises: 
Create Date: 2025-09-17 00:00:00Z
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _common_columns():
    return [
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("status", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
    ]


def upgrade() -> None:
    # business_systems
    op.create_table(
        "business_systems",
        sa.Column("business_system_bid", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("base_url", sa.String(length=1024), nullable=True),
        sa.Column("auth_method", sa.String(length=64), nullable=True),
        sa.Column("app_id", sa.String(length=255), nullable=True),
        sa.Column("app_secret", sa.String(length=255), nullable=True),
        *_common_columns(),
    )
    op.create_index("ix_business_systems_bid", "business_systems", ["business_system_bid"], unique=True)

    # notification_apis
    op.create_table(
        "notification_apis",
        sa.Column("notification_api_bid", sa.String(length=32), nullable=False),
        sa.Column("business_system_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("endpoint_url", sa.String(length=1024), nullable=False),
        sa.Column("request_schema", sa.JSON(), nullable=True),
        sa.Column("response_schema", sa.JSON(), nullable=True),
        *_common_columns(),
        sa.ForeignKeyConstraint(["business_system_id"], ["business_systems.id"], ondelete="RESTRICT"),
    )
    op.create_index("ix_notification_apis_bid", "notification_apis", ["notification_api_bid"], unique=True)

    # message_definitions
    op.create_table(
        "message_definitions",
        sa.Column("message_definition_bid", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=64), nullable=True),
        sa.Column("schema", sa.JSON(), nullable=True),
        *_common_columns(),
    )
    op.create_index(
        "ix_message_definitions_bid",
        "message_definitions",
        ["message_definition_bid"],
        unique=True,
    )

    # message_dispatches
    op.create_table(
        "message_dispatches",
        sa.Column("message_dispatch_bid", sa.String(length=32), nullable=False),
        sa.Column("message_definition_id", sa.Integer(), nullable=False),
        sa.Column("notification_api_id", sa.Integer(), nullable=False),
        sa.Column("mapping", sa.JSON(), nullable=True),
        sa.Column("enabled", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        *_common_columns(),
        sa.ForeignKeyConstraint(["message_definition_id"], ["message_definitions.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["notification_api_id"], ["notification_apis.id"], ondelete="RESTRICT"),
    )
    op.create_index("ix_message_dispatches_bid", "message_dispatches", ["message_dispatch_bid"], unique=True)
    op.create_unique_constraint(
        "uq_message_dispatches_pair",
        "message_dispatches",
        ["message_definition_id", "notification_api_id"],
    )

    # send_records
    op.create_table(
        "send_records",
        sa.Column("send_record_bid", sa.String(length=32), nullable=False),
        sa.Column("message_definition_id", sa.Integer(), nullable=False),
        sa.Column("notification_api_id", sa.Integer(), nullable=False),
        sa.Column("send_time", sa.DateTime(), nullable=True),
        sa.Column("result", sa.JSON(), nullable=True),
        sa.Column("remark", sa.Text(), nullable=True),
        *_common_columns(),
        sa.ForeignKeyConstraint(["message_definition_id"], ["message_definitions.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["notification_api_id"], ["notification_apis.id"], ondelete="RESTRICT"),
    )
    op.create_index("ix_send_records_bid", "send_records", ["send_record_bid"], unique=True)

    # send_details
    op.create_table(
        "send_details",
        sa.Column("send_detail_bid", sa.String(length=32), nullable=False),
        sa.Column("send_record_id", sa.Integer(), nullable=False),
        sa.Column("notification_api_id", sa.Integer(), nullable=False),
        sa.Column("attempt_no", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("request_payload", sa.JSON(), nullable=True),
        sa.Column("response_payload", sa.JSON(), nullable=True),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        *_common_columns(),
        sa.ForeignKeyConstraint(["send_record_id"], ["send_records.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["notification_api_id"], ["notification_apis.id"], ondelete="RESTRICT"),
    )
    op.create_index("ix_send_details_bid", "send_details", ["send_detail_bid"], unique=True)

    # users
    op.create_table(
        "users",
        sa.Column("user_bid", sa.String(length=32), nullable=False),
        sa.Column("username", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        *_common_columns(),
    )
    op.create_index("ix_users_bid", "users", ["user_bid"], unique=True)
    op.create_unique_constraint("uq_users_username", "users", ["username"])


def downgrade() -> None:
    op.drop_constraint("uq_users_username", "users", type_="unique")
    op.drop_index("ix_users_bid", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_send_details_bid", table_name="send_details")
    op.drop_table("send_details")

    op.drop_index("ix_send_records_bid", table_name="send_records")
    op.drop_table("send_records")

    op.drop_constraint("uq_message_dispatches_pair", "message_dispatches", type_="unique")
    op.drop_index("ix_message_dispatches_bid", table_name="message_dispatches")
    op.drop_table("message_dispatches")

    op.drop_index("ix_message_definitions_bid", table_name="message_definitions")
    op.drop_table("message_definitions")

    op.drop_index("ix_notification_apis_bid", table_name="notification_apis")
    op.drop_table("notification_apis")

    op.drop_index("ix_business_systems_bid", table_name="business_systems")
    op.drop_table("business_systems")
