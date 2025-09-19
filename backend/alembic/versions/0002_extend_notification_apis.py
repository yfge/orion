"""
Extend notification_apis with transport/adapter_key/config/auth_profile_id

Revision ID: 0002
Revises: 0001
Create Date: 2025-09-19 00:00:00Z
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("notification_apis") as batch_op:
        batch_op.add_column(sa.Column("transport", sa.String(length=16), nullable=True))
        batch_op.add_column(sa.Column("adapter_key", sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column("config", sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column("auth_profile_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("notification_apis") as batch_op:
        batch_op.drop_column("auth_profile_id")
        batch_op.drop_column("config")
        batch_op.drop_column("adapter_key")
        batch_op.drop_column("transport")

