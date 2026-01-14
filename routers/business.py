from fastapi import APIRouter
from pydantic import BaseModel
from services.business_service import create_business, add_business_knowledge

router = APIRouter(prefix="/business", tags=["business"])

class BusinessCreateRequest(BaseModel):
    name: str
    owner_name: str
    email: str
    phone: str | None = None

class KnowledgeUploadRequest(BaseModel):
    documents: list[dict]

@router.post("/create")
def create_business_route(payload: BusinessCreateRequest):
    return create_business(payload.dict())

@router.post("/{business_id}/knowledge")
def upload_knowledge_route(business_id: str, payload: KnowledgeUploadRequest):
    return add_business_knowledge(business_id, payload.dict())

@router.patch("/{business_id}/settings")
def update_business_settings_route(business_id: str, payload: dict):
    from services.business_service import update_business_settings
    return update_business_settings(business_id, payload)

@router.get("/{business_id}")
def get_business_info_route(business_id: str):
    from services.business_service import get_business_info
    return get_business_info(business_id)

@router.get("/{business_id}/analytics")
def get_business_analytics_route(business_id: str):
    from services.business_service import get_business_analytics
    return get_business_analytics(business_id)