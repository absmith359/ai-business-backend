import uuid
import os
import requests
from datetime import datetime
from typing import Optional
from models.lead import Lead
from services.referral_service import validate_referral_code, track_referral
from services.rep_service import get_rep

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

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

    rep_id: Optional[str] = data.get("rep_id")
    referral_code: Optional[str] = data.get("referral_code")

    # Validate referral code
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

    url = f"{SUPABASE_URL}/rest/v1/leads"
    response = requests.post(url, json=lead.dict(), headers=headers)

    if response.status_code >= 300:
        return {"status": "error", "message": "Failed to create lead"}

    # Track referral
    if referral_code:
        track_referral({
            "referral_code": referral_code,
            "business_id": data["business_id"],
            "lead_id": lead_id
        })

    return {
        "status": "success",
        "lead": response.json()[0]
    }


# -----------------------------
# List leads for a business
# -----------------------------
def list_leads(business_id: str):
    url = f"{SUPABASE_URL}/rest/v1/leads?business_id=eq.{business_id}&order=created_at.desc"
    res = requests.get(url, headers=headers).json()

    return {
        "status": "success",
        "leads": res
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
    url = f"{SUPABASE_URL}/rest/v1/leads?business_id=eq.{business_id}"

    if status:
        url += f"&status=eq.{status}"
    if min_score is not None:
        url += f"&score=gte.{min_score}"
    if max_score is not None:
        url += f"&score=lte.{max_score}"

    url += "&order=created_at.desc"

    res = requests.get(url, headers=headers).json()

    return {
        "status": "success",
        "leads": res
    }


# -----------------------------
# Update lead status
# -----------------------------
def update_lead_status(lead_id: str, status: str):
    url = f"{SUPABASE_URL}/rest/v1/leads?id=eq.{lead_id}"
    res = requests.patch(url, json={"status": status}, headers=headers)

    return {
        "status": "success",
        "updated": res.json()
    }