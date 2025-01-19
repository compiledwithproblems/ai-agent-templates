from fastapi import APIRouter
from ..services.agent_service import get_agent_service

router = APIRouter()

@router.get("/health")
async def health_check():
    agent_service = get_agent_service()
    agent_health = await agent_service.check_health()
    return {
        "status": "healthy" if agent_health else "degraded",
        "agent_service": agent_health
    } 