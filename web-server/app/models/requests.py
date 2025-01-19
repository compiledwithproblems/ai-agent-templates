from pydantic import BaseModel
from typing import Optional, Any, Dict

class AgentRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    response: Any
    status: str
    error: Optional[str] = None 