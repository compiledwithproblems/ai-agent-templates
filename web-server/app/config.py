from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Agent API"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Redis Configuration
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Agent Service Configuration
    AGENT_SERVICE_HOST: str = "agent-execution"
    AGENT_SERVICE_PORT: int = 5000
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 