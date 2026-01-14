import uuid
import os
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# -----------------------------
# Generate unique referral code
# -----------------------------
def generate_referral_code(name: str) -> str:
    base = name.replace(" ", "").upper()
    suffix = str(uuid.uuid4())[:6].upper()
    return f"{base}-{suffix}"


# -----------------------------
# Create a new rep
# -----------------------------
def create_rep(data: dict):
    rep_id = str(uuid.uuid4())
    referral_code = generate_referral_code(data["name"])

    rep = {
        "id": rep_id,
        "name": data["name"],
        "email": data.get("email"),
        "phone": data.get("phone"),
        "referral_code": referral_code,
        "total_referrals": 0,
        "total_leads": 0,
        "total_conversions": 0,
        "created_at": datetime.utcnow().isoformat()
    }

    url = f"{SUPABASE_URL}/rest/v1/reps"
    response = requests.post(url, json=rep, headers=headers)

    if response.status_code >= 300:
        raise Exception("Failed to create rep")

    return {
        "status": "success",
        "rep": response.json()[0]
    }


# -----------------------------
# Get rep info
# -----------------------------
def get_rep(rep_id: str):
    url = f"{SUPABASE_URL}/rest/v1/reps?id=eq.{rep_id}"
    res = requests.get(url, headers=headers).json()
    return res[0] if res else None


# -----------------------------
# Get rep stats
# -----------------------------
def get_rep_stats(rep_id: str):
    rep = get_rep(rep_id)
    if not rep:
        return {"error": "Rep not found"}

    return {
        "referrals": rep.get("total_referrals", 0),
        "leads": rep.get("total_leads", 0),
        "conversions": rep.get("total_conversions", 0)
    }


# -----------------------------
# Leaderboard
# -----------------------------
def get_rep_leaderboard():
    url = f"{SUPABASE_URL}/rest/v1/reps?order=total_referrals.desc"
    res = requests.get(url, headers=headers).json()
    return res


# -----------------------------
# Track referral event
# -----------------------------
def track_rep_referral(rep_id: str, business_id: str | None, lead_id: str | None):
    rep = get_rep(rep_id)
    if not rep:
        return {"error": "Rep not found"}

    new_total = (rep.get("total_referrals") or 0) + 1

    # Update rep stats
    url = f"{SUPABASE_URL}/rest/v1/reps?id=eq.{rep_id}"
    requests.patch(url, json={"total_referrals": new_total}, headers=headers)

    # Log referral
    referral = {
        "id": str(uuid.uuid4()),
        "rep_id": rep_id,
        "business_id": business_id,
        "lead_id": lead_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    url = f"{SUPABASE_URL}/rest/v1/referrals"
    requests.post(url, json=referral, headers=headers)

    return {
        "status": "success",
        "referral": referral
    }