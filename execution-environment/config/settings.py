from pydantic import BaseSettings
from typing import Optional, Dict, List

class Settings(BaseSettings):
    # Agent Configuration
    AGENT_NAME: str = "DefaultAgent"
    AGENT_DESCRIPTION: str = "A flexible AI agent template"
    MODEL_NAME: str = "gpt-4"  # Default model
    
    # API Configuration
    API_KEYS: Dict[str, str] = {}
    MAX_RETRIES: int = 3
    TIMEOUT: int = 30
    
    # Memory Configuration
    MEMORY_TYPE: str = "in_memory"  # Options: in_memory, redis, postgres
    MEMORY_CONNECTION: Optional[str] = None
    MEMORY_TTL: int = 3600  # Time to live in seconds
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
