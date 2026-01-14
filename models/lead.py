from pydantic import BaseModel
from typing import Optional

class Lead(BaseModel):
    id: str
    business_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    message: Optional[str] = None

    # Associations
    rep_id: Optional[str] = None
    referral_code: Optional[str] = None

    # Lead management
    status: str = "new"           # new, contacted, qualified, lost, won
    score: int = 0

    created_at: str