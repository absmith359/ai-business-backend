from pydantic import BaseModel

class Chat(BaseModel):
    id: str | None = None
    business_id: str
    user_message: str
    ai_response: str | None = None
    rep_id: str | None = None
    created_at: str | None = None