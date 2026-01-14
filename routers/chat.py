from fastapi import APIRouter
from services.chat_service import generate_response

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
def chat_endpoint(payload: dict):
    business_id = payload["business_id"]
    session_id = payload.get("session_id", "default")
    message = payload["message"]

    ai_response = generate_response(business_id, session_id, message)

    return {"response": ai_response}