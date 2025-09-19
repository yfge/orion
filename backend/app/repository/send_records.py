from typing import Tuple, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ..db.models import SendRecord, SendDetail, MessageDefinition, NotificationAPI, BusinessSystem


def list_send_records(
    db: Session,
    *,
    limit: int = 50,
    offset: int = 0,
    message_definition_bid: Optional[str] = None,
    notification_api_bid: Optional[str] = None,
    status: Optional[int] = None,
) -> Tuple[list[SendRecord], int]:
    base = (
        select(
            SendRecord,
            MessageDefinition.name.label("message_name"),
            NotificationAPI.name.label("endpoint_name"),
            BusinessSystem.name.label("business_system_name"),
        )
        .join(
            MessageDefinition,
            SendRecord.message_definition_bid == MessageDefinition.message_definition_bid,
        )
        .join(
            NotificationAPI,
            SendRecord.notification_api_bid == NotificationAPI.notification_api_bid,
        )
        .join(
            BusinessSystem,
            NotificationAPI.business_system_bid == BusinessSystem.business_system_bid,
        )
        .where(SendRecord.is_deleted == False)  # noqa: E712
    )

    if message_definition_bid:
        base = base.where(SendRecord.message_definition_bid == message_definition_bid)
    if notification_api_bid:
        base = base.where(SendRecord.notification_api_bid == notification_api_bid)
    if status is not None:
        base = base.where(SendRecord.status == status)

    rows = db.execute(
        base.order_by(SendRecord.id.desc()).limit(limit).offset(offset)
    ).all()
    items: list[SendRecord] = []
    for rec, msg_name, ep_name, bs_name in rows:
        rec.message_name = msg_name  # type: ignore[attr-defined]
        rec.endpoint_name = ep_name  # type: ignore[attr-defined]
        rec.business_system_name = bs_name  # type: ignore[attr-defined]
        items.append(rec)

    count_q = select(func.count()).select_from(SendRecord).where(SendRecord.is_deleted == False)  # noqa: E712
    if message_definition_bid:
        count_q = count_q.where(SendRecord.message_definition_bid == message_definition_bid)
    if notification_api_bid:
        count_q = count_q.where(SendRecord.notification_api_bid == notification_api_bid)
    if status is not None:
        count_q = count_q.where(SendRecord.status == status)
    total = int(db.execute(count_q).scalar_one())
    return items, total


def get_record_by_bid(db: Session, *, bid: str) -> SendRecord | None:
    row = db.execute(
        select(
            SendRecord,
            MessageDefinition.name.label("message_name"),
            NotificationAPI.name.label("endpoint_name"),
            BusinessSystem.name.label("business_system_name"),
        )
        .join(
            MessageDefinition,
            SendRecord.message_definition_bid == MessageDefinition.message_definition_bid,
        )
        .join(
            NotificationAPI,
            SendRecord.notification_api_bid == NotificationAPI.notification_api_bid,
        )
        .join(
            BusinessSystem,
            NotificationAPI.business_system_bid == BusinessSystem.business_system_bid,
        )
        .where(SendRecord.send_record_bid == bid, SendRecord.is_deleted == False)  # noqa: E712
    ).first()
    if not row:
        return None
    rec, msg_name, ep_name, bs_name = row
    rec.message_name = msg_name  # type: ignore[attr-defined]
    rec.endpoint_name = ep_name  # type: ignore[attr-defined]
    rec.business_system_name = bs_name  # type: ignore[attr-defined]
    return rec


def list_details_by_record(
    db: Session, *, send_record_bid: str, limit: int = 50, offset: int = 0
) -> Tuple[list[SendDetail], int]:
    base = (
        select(SendDetail, NotificationAPI.name.label("endpoint_name"))
        .join(
            NotificationAPI,
            SendDetail.notification_api_bid == NotificationAPI.notification_api_bid,
        )
        .where(
            SendDetail.send_record_bid == send_record_bid,
            SendDetail.is_deleted == False,  # noqa: E712
        )
    )
    rows = db.execute(
        base.order_by(SendDetail.id.asc()).limit(limit).offset(offset)
    ).all()
    items: list[SendDetail] = []
    for det, ep_name in rows:
        det.endpoint_name = ep_name  # type: ignore[attr-defined]
        items.append(det)
    total = int(
        db.execute(
            select(func.count())
            .select_from(SendDetail)
            .where(
                SendDetail.send_record_bid == send_record_bid,
                SendDetail.is_deleted == False,  # noqa: E712
            )
        ).scalar_one()
    )
    return items, total

