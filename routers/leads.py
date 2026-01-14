from fastapi import APIRouter, Query
from typing import Optional
from services.lead_service import (
    submit_lead,
    list_leads,
    filter_leads,
    update_lead_status,
)

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/submit")
def submit_lead_route(payload: dict):
    return submit_lead(payload)


@router.get("/{business_id}")
def list_leads_route(business_id: str):
    return list_leads(business_id)


@router.get("/{business_id}/filter")
def filter_leads_route(
    business_id: str,
    status: Optional[str] = Query(None),
    min_score: Optional[int] = Query(None),
    max_score: Optional[int] = Query(None),
):
    return filter_leads(
        business_id=business_id,
        status=status,
        min_score=min_score,
        max_score=max_score,
    )


@router.patch("/{lead_id}/status")
def update_lead_status_route(lead_id: str, payload: dict):
    status = payload.get("status")
    return update_lead_status(lead_id, status)