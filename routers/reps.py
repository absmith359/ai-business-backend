from fastapi import APIRouter
from services.rep_service import create_rep, get_rep, get_rep_stats, get_rep_leaderboard

router = APIRouter(prefix="/reps", tags=["Reps"])

@router.post("/create")
def create_rep_route(payload: dict):
    return create_rep(payload)

@router.get("/{rep_id}")
def get_rep_route(rep_id: str):
    return get_rep(rep_id)

@router.get("/{rep_id}/stats")
def get_rep_stats_route(rep_id: str):
    return get_rep_stats(rep_id)

@router.get("/leaderboard")
def leaderboard_route():
    return get_rep_leaderboard()