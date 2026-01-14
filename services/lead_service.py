import os
import requests
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# ---------------------------------------------------------
# SIMPLE LEAD SCORING
# ---------------------------------------------------------
def score_lead(message: str):
    if not message:
        return "low"

    msg = message.lower()

    high_keywords = ["urgent", "asap", "quote", "call me", "interested", "buy", "pricing"]
    medium_keywords = ["info", "details", "learn more"]

    if any(k in msg for k in high_keywords):
        return "high"
    if any(k in msg for k in medium_keywords):
        return "medium"

    return "low"


# ---------------------------------------------------------
# CREATE LEAD
# ---------------------------------------------------------
def create_lead(business_id: str, data: dict):
    data["business_id"] = business_id
    data["score"] = score_lead(data.get("message", ""))

    url = f"{SUPABASE_URL}/rest/v1/leads"
    response = requests.post(url, json=data, headers=headers)

    if response.status_code >= 300:
        print("Error inserting lead:", response.text)
        raise Exception("Failed to insert lead")

    return {
        "status": "success",
        "lead": response.json()
    }


# ---------------------------------------------------------
# LIST LEADS
# ---------------------------------------------------------
def list_leads(business_id: str):
    url = f"{SUPABASE_URL}/rest/v1/leads?business_id=eq.{business_id}&order=created_at.desc"
    response = requests.get(url, headers=headers)

    if response.status_code >= 300:
        print("Error fetching leads:", response.text)
        raise Exception("Failed to fetch leads")

    return response.json()


# ---------------------------------------------------------
# FILTER LEADS
# ---------------------------------------------------------
def filter_leads(business_id: str, score: str):
    url = f"{SUPABASE_URL}/rest/v1/leads?business_id=eq.{business_id}&score=eq.{score}"
    response = requests.get(url, headers=headers)

    if response.status_code >= 300:
        print("Error filtering leads:", response.text)
        raise Exception("Failed to filter leads")

    return response.json()