import uuid
import os
import requests
from datetime import datetime, timedelta
from models.business import Business
from utils.vector_client import store_business_knowledge, search_business_knowledge

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ---------------------------------------------------------
# CREATE BUSINESS
# ---------------------------------------------------------
def create_business(data: dict):
    business = Business(
        id=str(uuid.uuid4()),
        name=data["name"],
        owner_name=data["owner_name"],
        email=data["email"],
        phone=data.get("phone"),
        custom_prompt="You are the AI assistant for this business. Be helpful, accurate, and friendly.",
        greeting="Hi! How can I help you today?",
        primary_color="#4F46E5",
        secondary_color="#6366F1",
        logo_url="https://placehold.co/100x100?text=Logo",
        widget_position="bottom-right",
        welcome_message="Welcome! Ask me anything.",
        show_typing_indicator=True,
        enable_lead_capture=True
    )

    url = f"{SUPABASE_URL}/rest/v1/businesses"
    response = requests.post(url, json=business.dict(), headers=headers)

    return {
        "status": "success",
        "business": response.json()[0]
    }


# ---------------------------------------------------------
# ADD KNOWLEDGE
# ---------------------------------------------------------
def add_business_knowledge(business_id: str, data: dict):
    documents = data.get("documents", [])

    if not documents:
        return {"status": "error", "message": "No documents provided"}

    for doc in documents:
        text = doc.get("text")
        if text:
            store_business_knowledge(business_id, text)

    return {"status": "success", "message": "Knowledge uploaded successfully"}


# ---------------------------------------------------------
# GET BUSINESS INFO
# ---------------------------------------------------------
def get_business_info(business_id: str):
    url = f"{SUPABASE_URL}/rest/v1/businesses?id=eq.{business_id}"
    response = requests.get(url, headers=headers)

    data = response.json()
    if not data:
        return {"status": "error", "message": "Business not found"}

    return {"status": "success", "business": data[0]}


# ---------------------------------------------------------
# ANALYTICS
# ---------------------------------------------------------
def get_business_analytics(business_id: str):
    def fetch(table):
        url = f"{SUPABASE_URL}/rest/v1/{table}?business_id=eq.{business_id}"
        return requests.get(url, headers=headers).json()

    chats = fetch("chats")
    leads = fetch("leads")
    referrals = fetch("referrals")

    total_chats = len(chats)
    total_leads = len(leads)
    total_referrals = len(referrals)

    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_chats = [
        c for c in chats
        if c.get("created_at") and datetime.fromisoformat(c["created_at"].replace("Z", "")) >= seven_days_ago
    ]

    last_chat = max(
        (c["created_at"] for c in chats if c.get("created_at")),
        default=None
    )

    return {
        "status": "success",
        "analytics": {
            "total_chats": total_chats,
            "total_leads": total_leads,
            "total_referrals": total_referrals,
            "last_7_days_chats": len(recent_chats),
            "last_chat_at": last_chat
        }
    }


# ---------------------------------------------------------
# UPDATE SETTINGS
# ---------------------------------------------------------
def update_business_settings(business_id: str, data: dict):
    url = f"{SUPABASE_URL}/rest/v1/businesses?id=eq.{business_id}"
    response = requests.patch(url, json=data, headers=headers)

    return {
        "status": "success",
        "updated": response.json()
    }