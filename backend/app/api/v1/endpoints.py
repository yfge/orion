from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...deps.db import get_db
from ...repository import endpoints as repo
from ...schemas.endpoints import EndpointCreate, EndpointList, EndpointOut, EndpointUpdate, SendTestRequest, SendTestResponse
from ...services.sender.http_sender import HttpSender
from ...repository import endpoints as repo
from ...repository import dispatches as dispatch_repo
from ...schemas.dispatches import DispatchCreate, DispatchList, DispatchOut, DispatchUpdate, EndpointDispatchCreate


router = APIRouter(tags=["endpoints"])


@router.post("/systems/{system_bid}/endpoints", response_model=EndpointOut, status_code=status.HTTP_201_CREATED)
def create_endpoint(system_bid: str, payload: EndpointCreate, db: Session = Depends(get_db)):
    try:
        obj = repo.create_endpoint(
            db,
            system_bid=system_bid,
            name=payload.name,
            transport=payload.transport,
            adapter_key=payload.adapter_key,
            endpoint_url=payload.endpoint_url,
            config=payload.config,
            auth_profile_bid=payload.auth_profile_bid,
            status=payload.status or 0,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Business system not found")
    db.commit()
    db.refresh(obj)
    # shape for output
    out = {
        "notification_api_bid": obj.notification_api_bid,
        "business_system_bid": system_bid,
        "name": obj.name,
        "transport": obj.transport,
        "adapter_key": obj.adapter_key,
        "endpoint_url": obj.endpoint_url,
        "config": obj.config,
        "auth_profile_bid": payload.auth_profile_bid,
        "status": obj.status,
    }
    return out


@router.get("/systems/{system_bid}/endpoints", response_model=EndpointList)
def list_endpoints(system_bid: str, db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0), q: str | None = Query(default=None)):
    items, total = repo.list_endpoints(db, system_bid=system_bid, limit=limit, offset=offset, q=q)
    shaped = [
        {
            "notification_api_bid": it.notification_api_bid,
            "business_system_bid": getattr(it, "business_system_bid", system_bid),
            "name": it.name,
            "transport": it.transport,
            "adapter_key": it.adapter_key,
            "endpoint_url": it.endpoint_url,
            "config": it.config,
            "auth_profile_bid": getattr(it, "auth_profile_bid", None),
            "status": it.status,
        }
        for it in items
    ]
    return {"items": shaped, "total": total, "limit": limit, "offset": offset}


@router.get("/endpoints/{endpoint_bid}", response_model=EndpointOut)
def get_endpoint(endpoint_bid: str, db: Session = Depends(get_db)):
    obj = repo.get_by_bid(db, endpoint_bid)
    if not obj:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return {
        "notification_api_bid": obj.notification_api_bid,
        "business_system_bid": getattr(obj, "business_system_bid", ""),
        "name": obj.name,
        "transport": obj.transport,
        "adapter_key": obj.adapter_key,
        "endpoint_url": obj.endpoint_url,
        "config": obj.config,
        "auth_profile_bid": getattr(obj, "auth_profile_bid", None),
        "status": obj.status,
    }


@router.patch("/endpoints/{endpoint_bid}", response_model=EndpointOut)
def update_endpoint(endpoint_bid: str, payload: EndpointUpdate, db: Session = Depends(get_db)):
    obj = repo.update_by_bid(
        db,
        endpoint_bid,
        name=payload.name,
        transport=payload.transport,
        adapter_key=payload.adapter_key,
        endpoint_url=payload.endpoint_url,
        config=payload.config,
        auth_profile_bid=payload.auth_profile_bid,
        status=payload.status,
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    db.commit()
    db.refresh(obj)
    return {
        "notification_api_bid": obj.notification_api_bid,
        "business_system_bid": getattr(obj, "business_system_bid", ""),
        "name": obj.name,
        "transport": obj.transport,
        "adapter_key": obj.adapter_key,
        "endpoint_url": obj.endpoint_url,
        "config": obj.config,
        "auth_profile_bid": payload.auth_profile_bid,
        "status": obj.status,
    }


@router.delete("/endpoints/{endpoint_bid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_endpoint(endpoint_bid: str, db: Session = Depends(get_db)):
    ok = repo.soft_delete_by_bid(db, endpoint_bid)
    if not ok:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    db.commit()
    return None


@router.post("/endpoints/{endpoint_bid}/send-test", response_model=SendTestResponse)
def send_test(endpoint_bid: str, payload: SendTestRequest, db: Session = Depends(get_db)):
    obj = repo.get_by_bid(db, endpoint_bid)
    if not obj:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    if (obj.transport or "http") != "http":
        raise HTTPException(status_code=400, detail="Only HTTP endpoints support send-test")

    endpoint_dict = {
        "adapter_key": obj.adapter_key or "http.generic",
        "endpoint_url": obj.endpoint_url,
        "config": (obj.config or {}) | {"url": obj.endpoint_url},
        "auth_type": None,
        "auth_config": None,
    }
    # Build payload for Feishu/Mailgun if applicable
    msg: dict
    if (obj.adapter_key or "").startswith("http.feishu"):
        msg = {"msg_type": "text", "content": {"text": payload.text}}
    elif (obj.adapter_key or "").lower().startswith("http.mailgun"):
        cfg = obj.config or {}
        to = cfg.get("to")
        if not to:
            raise HTTPException(status_code=400, detail="Mailgun send-test requires 'to' in endpoint config")
        from_addr = cfg.get("from") or "orion@example.com"
        msg = {
            "from": from_addr,
            "to": to,
            "subject": "Orion Test",
            "text": payload.text,
        }
    elif (obj.adapter_key or "").lower().startswith("http.sendgrid"):
        cfg = obj.config or {}
        to = cfg.get("to")
        if not to:
            raise HTTPException(status_code=400, detail="SendGrid send-test requires 'to' in endpoint config")
        from_addr = cfg.get("from") or "orion@example.com"
        msg = {
            "personalizations": [{"to": [{"email": to}] }],
            "from": {"email": from_addr},
            "subject": "Orion Test",
            "content": [{"type": "text/plain", "value": payload.text}],
        }
    else:
        msg = {"text": payload.text}

    sender = HttpSender()
    try:
        result = sender.send(endpoint=endpoint_dict, payload=msg)
        return SendTestResponse(status_code=int(result.get("status_code", 0)), body=result.get("body"))
    except Exception as e:  # pragma: no cover
        raise HTTPException(status_code=502, detail=f"Send failed: {e}")


# Optionally list all endpoints (across systems)
@router.get("/endpoints", response_model=EndpointList)
def list_all_endpoints(db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=1000), offset: int = Query(0, ge=0), q: str | None = Query(default=None)):
    items, total = repo.list_all_endpoints(db, limit=limit, offset=offset, q=q)
    shaped = [
        {
            "notification_api_bid": it.notification_api_bid,
            "business_system_bid": getattr(it, "business_system_bid", None),
            "name": it.name,
            "transport": it.transport,
            "adapter_key": it.adapter_key,
            "endpoint_url": it.endpoint_url,
            "config": it.config,
            "auth_profile_bid": getattr(it, "auth_profile_bid", None),
            "status": it.status,
        }
        for it in items
    ]
    return {"items": shaped, "total": total, "limit": limit, "offset": offset}


# Dispatches (message -> endpoint)
@router.post("/message-definitions/{message_bid}/dispatches", response_model=DispatchOut, status_code=status.HTTP_201_CREATED)
def create_dispatch(message_bid: str, payload: DispatchCreate, db: Session = Depends(get_db)):
    try:
        obj = dispatch_repo.create_dispatch(db, message_bid=message_bid, endpoint_bid=payload.endpoint_bid, mapping=payload.mapping, enabled=payload.enabled)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    db.commit()
    db.refresh(obj)
    shaped = dispatch_repo.get_by_bid(db, obj.message_dispatch_bid)
    return {
        "message_dispatch_bid": obj.message_dispatch_bid,
        "message_definition_bid": message_bid,
        "endpoint_bid": getattr(shaped, "endpoint_bid", payload.endpoint_bid) if shaped else payload.endpoint_bid,
        "endpoint_name": getattr(shaped, "endpoint_name", None) if shaped else None,
        "business_system_bid": getattr(shaped, "business_system_bid", None) if shaped else None,
        "mapping": obj.mapping,
        "enabled": obj.enabled,
        "status": obj.status,
    }


@router.get("/message-definitions/{message_bid}/dispatches", response_model=DispatchList)
def list_dispatches(message_bid: str, db: Session = Depends(get_db), limit: int = Query(100, ge=1, le=500), offset: int = Query(0, ge=0)):
    items, total = dispatch_repo.list_by_message(db, message_bid=message_bid, limit=limit, offset=offset)
    shaped = [
        {
            "message_dispatch_bid": it.message_dispatch_bid,
            "message_definition_bid": message_bid,
            "endpoint_bid": getattr(it, "endpoint_bid", None),
            "endpoint_name": getattr(it, "endpoint_name", None),
            "business_system_bid": getattr(it, "business_system_bid", None),
            "mapping": it.mapping,
            "enabled": it.enabled,
            "status": it.status,
        }
        for it in items
    ]
    return {"items": shaped, "total": total, "limit": limit, "offset": offset}


@router.get("/dispatches/{dispatch_bid}", response_model=DispatchOut)
def get_dispatch(dispatch_bid: str, db: Session = Depends(get_db)):
    obj = dispatch_repo.get_by_bid(db, dispatch_bid)
    if not obj:
        raise HTTPException(status_code=404, detail="Dispatch not found")
    return {
        "message_dispatch_bid": obj.message_dispatch_bid,
        "message_definition_bid": getattr(obj, "message_definition_bid", ""),
        "endpoint_bid": getattr(obj, "endpoint_bid", ""),
        "endpoint_name": getattr(obj, "endpoint_name", None),
        "business_system_bid": getattr(obj, "business_system_bid", None),
        "mapping": obj.mapping,
        "enabled": obj.enabled,
        "status": obj.status,
    }


@router.patch("/dispatches/{dispatch_bid}", response_model=DispatchOut)
def update_dispatch(dispatch_bid: str, payload: DispatchUpdate, db: Session = Depends(get_db)):
    try:
        obj = dispatch_repo.update_by_bid(db, dispatch_bid, endpoint_bid=payload.endpoint_bid, mapping=payload.mapping, enabled=payload.enabled)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    if not obj:
        raise HTTPException(status_code=404, detail="Dispatch not found")
    db.commit()
    db.refresh(obj)
    shaped = dispatch_repo.get_by_bid(db, dispatch_bid)
    return {
        "message_dispatch_bid": obj.message_dispatch_bid,
        "message_definition_bid": getattr(shaped, "message_definition_bid", "") if shaped else "",
        "endpoint_bid": getattr(shaped, "endpoint_bid", "") if shaped else (payload.endpoint_bid or ""),
        "endpoint_name": getattr(shaped, "endpoint_name", None) if shaped else None,
        "business_system_bid": getattr(shaped, "business_system_bid", None) if shaped else None,
        "mapping": obj.mapping,
        "enabled": obj.enabled,
        "status": obj.status,
    }


@router.delete("/dispatches/{dispatch_bid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dispatch(dispatch_bid: str, db: Session = Depends(get_db)):
    ok = dispatch_repo.soft_delete_by_bid(db, dispatch_bid)
    if not ok:
        raise HTTPException(status_code=404, detail="Dispatch not found")
    db.commit()
    return None


@router.get("/endpoints/{endpoint_bid}/dispatches", response_model=DispatchList)
def list_dispatches_by_endpoint(endpoint_bid: str, db: Session = Depends(get_db), limit: int = Query(100, ge=1, le=500), offset: int = Query(0, ge=0)):
    items, total = dispatch_repo.list_by_endpoint(db, endpoint_bid=endpoint_bid, limit=limit, offset=offset)
    shaped = [
        {
            "message_dispatch_bid": it.message_dispatch_bid,
            "message_definition_bid": getattr(it, "message_definition_bid", None),
            "endpoint_bid": endpoint_bid,
            "endpoint_name": None,
            "business_system_bid": None,
            "mapping": it.mapping,
            "enabled": it.enabled,
            "status": it.status,
        }
        for it in items
    ]
    return {"items": shaped, "total": total, "limit": limit, "offset": offset}


@router.post("/endpoints/{endpoint_bid}/dispatches", response_model=DispatchOut, status_code=status.HTTP_201_CREATED)
def create_dispatch_for_endpoint(endpoint_bid: str, payload: EndpointDispatchCreate, db: Session = Depends(get_db)):
    try:
        obj = dispatch_repo.create_dispatch(db, message_bid=payload.message_definition_bid, endpoint_bid=endpoint_bid, mapping=payload.mapping, enabled=payload.enabled)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    db.commit()
    db.refresh(obj)
    shaped = dispatch_repo.get_by_bid(db, obj.message_dispatch_bid)
    return {
        "message_dispatch_bid": obj.message_dispatch_bid,
        "message_definition_bid": payload.message_definition_bid,
        "endpoint_bid": endpoint_bid,
        "endpoint_name": getattr(shaped, "endpoint_name", None) if shaped else None,
        "business_system_bid": getattr(shaped, "business_system_bid", None) if shaped else None,
        "mapping": obj.mapping,
        "enabled": obj.enabled,
        "status": obj.status,
    }
