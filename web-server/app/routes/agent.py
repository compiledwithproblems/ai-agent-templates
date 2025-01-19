from fastapi import APIRouter, HTTPException
from ..models.requests import AgentRequest, AgentResponse
from ..services.agent_service import get_agent_service

router = APIRouter()

@router.post("/query", response_model=AgentResponse)
async def query_agent(request: AgentRequest):
    try:
        agent_service = get_agent_service()
        response = await agent_service.send_request(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 