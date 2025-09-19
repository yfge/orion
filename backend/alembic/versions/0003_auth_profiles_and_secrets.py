"""
Add auth_profiles and secrets; link notification_apis.auth_profile_id

Revision ID: 0003
Revises: 0002
Create Date: 2025-09-19 00:00:01Z
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "secrets",
        sa.Column("secret_bid", sa.String(length=32), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("status", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.UniqueConstraint("key"),
    )
    op.create_index("ix_secrets_bid", "secrets", ["secret_bid"], unique=True)

    op.create_table(
        "auth_profiles",
        sa.Column("auth_profile_bid", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("config", sa.JSON(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("status", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
    )
    op.create_index("ix_auth_profiles_bid", "auth_profiles", ["auth_profile_bid"], unique=True)

    # Add FK from notification_apis.auth_profile_id to auth_profiles.id (nullable)
    with op.batch_alter_table("notification_apis") as batch_op:
        batch_op.create_foreign_key(
            "fk_notification_apis_auth_profile",
            "auth_profiles",
            ["auth_profile_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("notification_apis") as batch_op:
        batch_op.drop_constraint("fk_notification_apis_auth_profile", type_="foreignkey")

    op.drop_index("ix_auth_profiles_bid", table_name="auth_profiles")
    op.drop_table("auth_profiles")

    op.drop_index("ix_secrets_bid", table_name="secrets")
    op.drop_table("secrets")

