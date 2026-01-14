import uuid
from datetime import datetime
from utils.vector_client import supabase
from services.rep_service import track_rep_referral

# -----------------------------
# Validate referral code
# -----------------------------
def validate_referral_code(code: str):
    res = supabase.table("reps").select("*").eq("referral_code", code).execute()
    return res.data[0] if res.data else None

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

    # Log referral event
    referral = {
        "id": str(uuid.uuid4()),
        "rep_id": rep_id,
        "referral_code": code,
        "business_id": business_id,
        "lead_id": lead_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    supabase.table("referrals").insert(referral).execute()

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
    res = supabase.table("referrals").select("*").eq("rep_id", rep_id).execute()
    return {
        "status": "success",
        "referrals": res.data
    }

# -----------------------------
# Get referrals for a business
# -----------------------------
def get_referrals_for_business(business_id: str):
    res = supabase.table("referrals").select("*").eq("business_id", business_id).execute()
    return {
        "status": "success",
        "referrals": res.data
    }