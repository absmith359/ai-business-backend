from fastapi import APIRouter
from services.referral_service import (
    track_referral,
    get_referrals_for_rep,
    get_referrals_for_business
)

router = APIRouter(prefix="/referrals", tags=["Referrals"])

@router.post("/track")
def track_referral_route(payload: dict):
    return track_referral(payload)

@router.get("/rep/{rep_id}")
def referrals_for_rep(rep_id: str):
    return get_referrals_for_rep(rep_id)

@router.get("/business/{business_id}")
def referrals_for_business(business_id: str):
    return get_referrals_for_business(business_id)