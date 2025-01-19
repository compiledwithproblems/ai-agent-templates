from typing import Any, Callable, Dict, List
from functools import wraps
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class Tool:
    """Base class for agent tools/skills."""
    
    def __init__(self, func: Callable, name: str, description: str):
        self.func = func
        self.name = name
        self.description = description
    
    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        logger.debug(f"Executing tool: {self.name}")
        try:
            return await self.func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {str(e)}")
            raise

def register_tool(name: str, description: str = ""):
    """Decorator to register a function as an agent tool."""
    def decorator(func: Callable) -> Tool:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await func(*args, **kwargs)
        return Tool(wrapper, name, description)
    return decorator
