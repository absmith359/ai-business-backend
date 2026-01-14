import uuid
import os
import requests
from datetime import datetime
from services.rep_service import track_rep_referral

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# -----------------------------
# Validate referral code
# -----------------------------
def validate_referral_code(code: str):
    url = f"{SUPABASE_URL}/rest/v1/reps?referral_code=eq.{code}"
    res = requests.get(url, headers=headers).json()
    return res[0] if res else None


# -----------------------------
# Track referral event
# -----------------------------
def track_referral(data: dict):
    code = data["referral_code"]
    rep = validate_referral_code(code)

    if not rep:
        return {"status": "error", "message": "Invalid referral code"}

    rep_id = rep["id"]
    business_id = data.get("business_id")
    lead_id = data.get("lead_id")

    referral = {
        "id": str(uuid.uuid4()),
        "rep_id": rep_id,
        "referral_code": code,
        "business_id": business_id,
        "lead_id": lead_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Insert referral
    url = f"{SUPABASE_URL}/rest/v1/referrals"
    response = requests.post(url, json=referral, headers=headers)

    if response.status_code >= 300:
        return {"status": "error", "message": "Failed to log referral"}

    # Update rep stats
    track_rep_referral(rep_id, business_id, lead_id)

    return {
        "status": "success",
        "referral": referral
    }


# -----------------------------
# Get referrals for a rep
# -----------------------------
def get_referrals_for_rep(rep_id: str):
    url = f"{SUPABASE_URL}/rest/v1/referrals?rep_id=eq.{rep_id}"
    res = requests.get(url, headers=headers).json()

    return {
        "status": "success",
        "referrals": res
    }


# -----------------------------
# Get referrals for a business
# -----------------------------
def get_referrals_for_business(business_id: str):
    url = f"{SUPABASE_URL}/rest/v1/referrals?business_id=eq.{business_id}"
    res = requests.get(url, headers=headers).json()

    return {
        "status": "success",
        "referrals": res
    }