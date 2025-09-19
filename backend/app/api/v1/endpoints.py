from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...deps.db import get_db
from ...repository import endpoints as repo
from ...schemas.endpoints import EndpointCreate, EndpointList, EndpointOut, EndpointUpdate


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
