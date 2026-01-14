from fastapi import APIRouter
from services.business_service import create_business, add_business_knowledge

router = APIRouter(prefix="/business", tags=["business"])

@router.post("/create")
def create_business_route(payload: dict):
    return create_business(payload)

@router.post("/{business_id}/knowledge")
def upload_knowledge_route(business_id: str, payload: dict):
    return add_business_knowledge(business_id, payload)

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