import uuid
from datetime import datetime
from utils.vector_client import supabase

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

    response = supabase.table("reps").insert(rep).execute()

    if response.data:
        return {
            "status": "success",
            "rep": response.data[0]
        }
    else:
        raise Exception("Failed to create rep")

# -----------------------------
# Get rep info
# -----------------------------
def get_rep(rep_id: str):
    res = supabase.table("reps").select("*").eq("id", rep_id).execute()
    return res.data[0] if res.data else None

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
    res = supabase.table("reps").select("*").order("total_referrals", desc=True).execute()
    return res.data

# -----------------------------
# Track referral event
# -----------------------------
def track_rep_referral(rep_id: str, business_id: str | None, lead_id: str | None):
    # increment counters (simple version)
    rep = get_rep(rep_id)
    if not rep:
        return {"error": "Rep not found"}

    new_total = (rep.get("total_referrals") or 0) + 1

    supabase.table("reps").update({
        "total_referrals": new_total
    }).eq("id", rep_id).execute()

    # log referral
    referral = {
        "id": str(uuid.uuid4()),
        "rep_id": rep_id,
        "business_id": business_id,
        "lead_id": lead_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    supabase.table("referrals").insert(referral).execute()

    return {
        "status": "success",
        "referral": referral
    }