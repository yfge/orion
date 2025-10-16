"""make wechat message send_record nullable

Revision ID: 0007
Revises: 0006
Create Date: 2025-10-16

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0007"
down_revision: str | None = "0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "wechat_official_account_messages",
        "send_record_bid",
        existing_type=sa.String(length=32),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "wechat_official_account_messages",
        "send_record_bid",
        existing_type=sa.String(length=32),
        nullable=False,
    )
