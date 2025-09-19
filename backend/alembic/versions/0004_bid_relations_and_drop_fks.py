"""
Migrate relations to BID-based and drop physical FKs; backfill data

Revision ID: 0004
Revises: 0003
Create Date: 2025-09-19 00:00:02Z
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)

    def has_column(table: str, col: str) -> bool:
        return any(c["name"] == col for c in insp.get_columns(table))

    def create_index_safe(name: str, table: str, cols: list[str]):
        try:
            existing = {ix["name"] for ix in insp.get_indexes(table)}
        except Exception:
            existing = set()
        if name not in existing:
            op.create_index(name, table, cols)

    def drop_fk_constraints_for_columns(table: str, columns: list[str]):
        # Drop any FK constraints referencing given columns (vendor-specific names)
        res = bind.execute(sa.text(
            """
            SELECT CONSTRAINT_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME IN :cols
              AND REFERENCED_TABLE_NAME IS NOT NULL
            GROUP BY CONSTRAINT_NAME
            """
        ), {"table": table, "cols": tuple(columns)})
        for row in res:
            cname = row[0]
            try:
                op.execute(sa.text(f"ALTER TABLE {table} DROP FOREIGN KEY `{cname}`"))
            except Exception:
                pass

    # notification_apis
    if not has_column("notification_apis", "business_system_bid"):
        op.add_column("notification_apis", sa.Column("business_system_bid", sa.String(length=32), nullable=True))
    if not has_column("notification_apis", "auth_profile_bid"):
        op.add_column("notification_apis", sa.Column("auth_profile_bid", sa.String(length=32), nullable=True))
    create_index_safe("ix_notification_apis_bs_bid", "notification_apis", ["business_system_bid"])
    create_index_safe("ix_notification_apis_ap_bid", "notification_apis", ["auth_profile_bid"])
    # backfill
    if has_column("notification_apis", "business_system_id"):
        op.execute(
            """
            UPDATE notification_apis n
            JOIN business_systems b ON n.business_system_id = b.id
            SET n.business_system_bid = b.business_system_bid
            """
        )
    if has_column("notification_apis", "auth_profile_id"):
        op.execute(
            """
            UPDATE notification_apis n
            LEFT JOIN auth_profiles a ON n.auth_profile_id = a.id
            SET n.auth_profile_bid = a.auth_profile_bid
            """
        )
    if has_column("notification_apis", "business_system_bid"):
        with op.batch_alter_table("notification_apis") as batch:
            batch.alter_column("business_system_bid", existing_type=sa.String(length=32), nullable=False)
    # drop old columns
    # drop FKs related to old id columns then drop columns
    drop_fk_constraints_for_columns("notification_apis", ["business_system_id", "auth_profile_id"])
    with op.batch_alter_table("notification_apis") as batch:
        for col in ("business_system_id", "auth_profile_id"):
            if has_column("notification_apis", col):
                batch.drop_column(col)

    # message_dispatches
    if not has_column("message_dispatches", "message_definition_bid"):
        op.add_column("message_dispatches", sa.Column("message_definition_bid", sa.String(length=32), nullable=True))
    if not has_column("message_dispatches", "notification_api_bid"):
        op.add_column("message_dispatches", sa.Column("notification_api_bid", sa.String(length=32), nullable=True))
    create_index_safe("ix_message_dispatches_msg_bid", "message_dispatches", ["message_definition_bid"])
    create_index_safe("ix_message_dispatches_ep_bid", "message_dispatches", ["notification_api_bid"])
    if has_column("message_dispatches", "message_definition_id"):
        op.execute(
            """
            UPDATE message_dispatches d
            JOIN message_definitions m ON d.message_definition_id = m.id
            SET d.message_definition_bid = m.message_definition_bid
            """
        )
    if has_column("message_dispatches", "notification_api_id"):
        op.execute(
            """
            UPDATE message_dispatches d
            JOIN notification_apis n ON d.notification_api_id = n.id
            SET d.notification_api_bid = n.notification_api_bid
            """
        )
    with op.batch_alter_table("message_dispatches") as batch:
        batch.alter_column("message_definition_bid", existing_type=sa.String(length=32), nullable=False)
        batch.alter_column("notification_api_bid", existing_type=sa.String(length=32), nullable=False)
    # drop FKs then old id columns
    drop_fk_constraints_for_columns("message_dispatches", ["message_definition_id", "notification_api_id"])
    with op.batch_alter_table("message_dispatches") as batch:
        for col in ("message_definition_id", "notification_api_id"):
            if has_column("message_dispatches", col):
                batch.drop_column(col)

    # send_records
    if not has_column("send_records", "message_definition_bid"):
        op.add_column("send_records", sa.Column("message_definition_bid", sa.String(length=32), nullable=True))
    if not has_column("send_records", "notification_api_bid"):
        op.add_column("send_records", sa.Column("notification_api_bid", sa.String(length=32), nullable=True))
    create_index_safe("ix_send_records_msg_bid", "send_records", ["message_definition_bid"])
    create_index_safe("ix_send_records_ep_bid", "send_records", ["notification_api_bid"])
    if has_column("send_records", "message_definition_id"):
        op.execute(
            """
            UPDATE send_records r
            JOIN message_definitions m ON r.message_definition_id = m.id
            SET r.message_definition_bid = m.message_definition_bid
            """
        )
    if has_column("send_records", "notification_api_id"):
        op.execute(
            """
            UPDATE send_records r
            JOIN notification_apis n ON r.notification_api_id = n.id
            SET r.notification_api_bid = n.notification_api_bid
            """
        )
    with op.batch_alter_table("send_records") as batch:
        batch.alter_column("message_definition_bid", existing_type=sa.String(length=32), nullable=False)
        batch.alter_column("notification_api_bid", existing_type=sa.String(length=32), nullable=False)
    drop_fk_constraints_for_columns("send_records", ["message_definition_id", "notification_api_id"])
    with op.batch_alter_table("send_records") as batch:
        for col in ("message_definition_id", "notification_api_id"):
            if has_column("send_records", col):
                batch.drop_column(col)

    # send_details
    if not has_column("send_details", "send_record_bid"):
        op.add_column("send_details", sa.Column("send_record_bid", sa.String(length=32), nullable=True))
    if not has_column("send_details", "notification_api_bid"):
        op.add_column("send_details", sa.Column("notification_api_bid", sa.String(length=32), nullable=True))
    create_index_safe("ix_send_details_record_bid", "send_details", ["send_record_bid"])
    create_index_safe("ix_send_details_ep_bid", "send_details", ["notification_api_bid"])
    if has_column("send_details", "send_record_id"):
        op.execute(
            """
            UPDATE send_details d
            JOIN send_records r ON d.send_record_id = r.id
            SET d.send_record_bid = r.send_record_bid
            """
        )
    if has_column("send_details", "notification_api_id"):
        op.execute(
            """
            UPDATE send_details d
            JOIN notification_apis n ON d.notification_api_id = n.id
            SET d.notification_api_bid = n.notification_api_bid
            """
        )
    with op.batch_alter_table("send_details") as batch:
        batch.alter_column("send_record_bid", existing_type=sa.String(length=32), nullable=False)
        batch.alter_column("notification_api_bid", existing_type=sa.String(length=32), nullable=False)
    drop_fk_constraints_for_columns("send_details", ["send_record_id", "notification_api_id"])
    with op.batch_alter_table("send_details") as batch:
        for col in ("send_record_id", "notification_api_id"):
            if has_column("send_details", col):
                batch.drop_column(col)


def downgrade() -> None:
    # This migration is one-way due to data backfill and FK drops.
    pass
