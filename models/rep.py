from pydantic import BaseModel

class Rep(BaseModel):
    id: str | None = None
    business_id: str
    name: str
    phone: str
    email: str | None = None
    created_at: str | None = None