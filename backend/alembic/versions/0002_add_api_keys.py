"""add api_keys table

Revision ID: 0002_add_api_keys
Revises: 0001_initial_schema
Create Date: 2025-09-21

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0002_add_api_keys"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "api_keys",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False
        ),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("status", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("api_key_bid", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("prefix", sa.String(length=16), nullable=True),
        sa.Column("suffix", sa.String(length=16), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
    )
    op.create_index("ix_api_keys_api_key_bid", "api_keys", ["api_key_bid"], unique=True)
    op.create_index("ix_api_keys_token_hash", "api_keys", ["token_hash"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_api_keys_token_hash", table_name="api_keys")
    op.drop_index("ix_api_keys_api_key_bid", table_name="api_keys")
    op.drop_table("api_keys")
