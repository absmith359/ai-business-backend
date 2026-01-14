from utils.vector_client import supabase
from models.business import Business
import uuid

# STEP 1 — Create business
def create_business(data: dict):
    business = Business(
        id=str(uuid.uuid4()),
        name=data["name"],
        owner_name=data["owner_name"],
        email=data["email"],
        phone=data.get("phone"),

        # AI defaults
        custom_prompt="You are the AI assistant for this business. Be helpful, accurate, and friendly.",
        greeting="Hi! How can I help you today?",

        # Branding defaults
        primary_color="#4F46E5",
        secondary_color="#6366F1",
        logo_url="https://placehold.co/100x100?text=Logo",

        # Widget defaults
        widget_position="bottom-right",
        welcome_message="Welcome! Ask me anything.",
        show_typing_indicator=True,
        enable_lead_capture=True
    )

    response = supabase.table("businesses").insert(business.dict()).execute()

    return {
        "status": "success",
        "business": response.data[0]
    }


# STEP 2 — Add knowledge (Supabase Vector)
from utils.vector_client import store_business_knowledge

def add_business_knowledge(business_id: str, data: dict):
    documents = data.get("documents", [])

    if not documents:
        return {"status": "error", "message": "No documents provided"}

    for doc in documents:
        text = doc.get("text")
        if not text:
            continue

        store_business_knowledge(business_id, text)

    return {"status": "success", "message": "Knowledge uploaded successfully"}



def get_business_info(business_id: str):
    response = supabase.table("businesses").select("*").eq("id", business_id).execute()

    if not response.data:
        return {"status": "error", "message": "Business not found"}

    business = response.data[0]

    return {
        "status": "success",
        "business": business
    }

from datetime import datetime, timedelta

def get_business_analytics(business_id: str):
    # Total chats
    chats = supabase.table("chats").select("id", "created_at").eq("business_id", business_id).execute().data
    total_chats = len(chats)

    # Total leads
    leads = supabase.table("leads").select("id").eq("business_id", business_id).execute().data
    total_leads = len(leads)

    # Total referrals
    referrals = supabase.table("referrals").select("id").eq("business_id", business_id).execute().data
    total_referrals = len(referrals)

    # Last 7 days chat activity
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_chats = [
        c for c in chats
        if c.get("created_at") and datetime.fromisoformat(c["created_at"].replace("Z", "")) >= seven_days_ago
    ]

    # Last chat timestamp
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

from fastapi import APIRouter
from services.business_service import create_business, add_business_knowledge, get_business_info, get_business_analytics

router = APIRouter(prefix="/business", tags=["Business"])

@router.post("/create")
def create_business_route(data: dict):
    return create_business(data)

@router.post("/{business_id}/knowledge")
def upload_knowledge(business_id: str, data: dict):
    return add_business_knowledge(business_id, data)

@router.patch("/{business_id}/settings")
def update_settings(business_id: str, data: dict):
    from utils.vector_client import supabase

    response = supabase.table("businesses").update(data).eq("id", business_id).execute()

    return {
        "status": "success",
        "updated": response.data
    }

@router.get("/{business_id}")
def get_business(business_id: str):
    return get_business_info(business_id)

@router.get("/{business_id}/analytics")
def analytics(business_id: str):
    return get_business_analytics(business_id)

def update_business_settings(business_id: str, data: dict):
    response = supabase.table("businesses").update(data).eq("id", business_id).execute()

    return {
        "status": "success",
        "updated": response.data
    }