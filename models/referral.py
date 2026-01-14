from pydantic import BaseModel

class Referral(BaseModel):
    id: str | None = None
    rep_id: str
    business_id: str
    lead_id: str | None = None
    created_at: str | None = None