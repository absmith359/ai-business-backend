from utils.vector_client import search_business_knowledge
from utils.ai_client import generate_ai_response
from utils.vector_client import supabase
from models.chat import Chat
import uuid

def generate_response(business_id: str, session_id: str, user_message: str):
    # 1. Retrieve relevant knowledge using Supabase Vector
    results = search_business_knowledge(business_id, user_message)

    # 2. Build context from retrieved chunks
    context = "\n".join([row["content"] for row in results])

    # 3. Generate AI response using your AI client
    ai_response = generate_ai_response(context, user_message)

    # 4. Save chat history
    save_chat_message(
        business_id=business_id,
        session_id=session_id,
        user_message=user_message,
        ai_response=ai_response
    )

    return ai_response


def save_chat_message(business_id: str, session_id: str, user_message: str, ai_response: str):
    chat = Chat(
        id=str(uuid.uuid4()),
        business_id=business_id,
        user_message=user_message,
        ai_response=ai_response,
        created_at=None
    )

    supabase.table("chats").insert(chat.dict()).execute()