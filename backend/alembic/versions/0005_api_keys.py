"""add api_keys table

Revision ID: 0005
Revises: 0004
Create Date: 2025-09-21

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0005"
down_revision: str | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "api_keys",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("status", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("owner_user_bid", sa.String(length=32), nullable=False),
        sa.Column("api_key_bid", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("prefix", sa.String(length=16), nullable=True),
        sa.Column("suffix", sa.String(length=16), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
    )
    op.create_index("ix_api_keys_api_key_bid", "api_keys", ["api_key_bid"], unique=True)
    op.create_index("ix_api_keys_owner_user_bid", "api_keys", ["owner_user_bid"], unique=False)
    op.create_index("ix_api_keys_token_hash", "api_keys", ["token_hash"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_api_keys_token_hash", table_name="api_keys")
    op.drop_index("ix_api_keys_api_key_bid", table_name="api_keys")
    op.drop_table("api_keys")
