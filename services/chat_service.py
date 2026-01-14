import uuid
import os
import requests
from models.chat import Chat
from utils.vector_client import search_business_knowledge
from utils.ai_client import generate_ai_response

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ---------------------------------------------------------
# GENERATE RESPONSE
# ---------------------------------------------------------
def generate_response(business_id: str, session_id: str, user_message: str):
    # 1. Retrieve relevant knowledge using vector search
    results = search_business_knowledge(business_id, user_message)

    # 2. Build context
    context = "\n".join([row["content"] for row in results])

    # 3. Generate AI response
    ai_response = generate_ai_response(context, user_message)

    # 4. Save chat history
    save_chat_message(
        business_id=business_id,
        session_id=session_id,
        user_message=user_message,
        ai_response=ai_response
    )

    return ai_response


# ---------------------------------------------------------
# SAVE CHAT MESSAGE (REST)
# ---------------------------------------------------------
def save_chat_message(business_id: str, session_id: str, user_message: str, ai_response: str):
    chat = Chat(
        id=str(uuid.uuid4()),
        business_id=business_id,
        session_id=session_id,
        user_message=user_message,
        ai_response=ai_response,
        created_at=None
    )

    url = f"{SUPABASE_URL}/rest/v1/chats"
    response = requests.post(url, json=chat.dict(), headers=headers)

    if response.status_code >= 300:
        print("Error saving chat:", response.text)

    return response.json()