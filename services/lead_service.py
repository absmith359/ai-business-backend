import uuid
from datetime import datetime
from typing import Optional, List
from utils.vector_client import supabase
from models.lead import Lead
from services.referral_service import validate_referral_code, track_referral
from services.rep_service import get_rep


# -----------------------------
# Lead scoring
# -----------------------------
def score_lead(data: dict) -> int:
    score = 0

    if data.get("email"):
        score += 20
    if data.get("phone"):
        score += 20
    if data.get("message") and len(data["message"]) > 50:
        score += 20
    if data.get("referral_code"):
        score += 20
    if data.get("rep_id"):
        score += 20

    return min(score, 100)


# -----------------------------
# Create / submit lead
# -----------------------------
def submit_lead(data: dict):
    lead_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    # Optional: validate referral code
    rep_id: Optional[str] = data.get("rep_id")
    referral_code: Optional[str] = data.get("referral_code")

    if referral_code and not rep_id:
        rep = validate_referral_code(referral_code)
        if rep:
            rep_id = rep["id"]

    lead_data = {
        "id": lead_id,
        "business_id": data["business_id"],
        "name": data["name"],
        "email": data.get("email"),
        "phone": data.get("phone"),
        "message": data.get("message"),
        "rep_id": rep_id,
        "referral_code": referral_code,
        "status": "new",
        "score": score_lead(data),
        "created_at": created_at,
    }

    lead = Lead(**lead_data)

    response = supabase.table("leads").insert(lead.dict()).execute()

    if not response.data:
        return {"status": "error", "message": "Failed to create lead"}

    # Track referral if applicable
    if referral_code:
        track_referral({
            "referral_code": referral_code,
            "business_id": data["business_id"],
            "lead_id": lead_id
        })

    # TODO: notifications (email/WhatsApp) can be added here later

    return {
        "status": "success",
        "lead": response.data[0]
    }


# -----------------------------
# List leads for a business
# -----------------------------
def list_leads(business_id: str):
    res = (
        supabase.table("leads")
        .select("*")
        .eq("business_id", business_id)
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "status": "success",
        "leads": res.data
    }


# -----------------------------
# Filter leads
# -----------------------------
def filter_leads(
    business_id: str,
    status: Optional[str] = None,
    min_score: Optional[int] = None,
    max_score: Optional[int] = None
):
    query = (
        supabase.table("leads")
        .select("*")
        .eq("business_id", business_id)
    )

    if status:
        query = query.eq("status", status)
    if min_score is not None:
        query = query.gte("score", min_score)
    if max_score is not None:
        query = query.lte("score", max_score)

    res = query.order("created_at", desc=True).execute()

    return {
        "status": "success",
        "leads": res.data
    }


# -----------------------------
# Update lead status
# -----------------------------
def update_lead_status(lead_id: str, status: str):
    res = supabase.table("leads").update({"status": status}).eq("id", lead_id).execute()

    return {
        "status": "success",
        "updated": res.data
    }