from abc import ABC, abstractmethod
from typing import Any, Optional
import json

class BaseMemory(ABC):
    """Base class for agent memory systems."""
    
    @abstractmethod
    async def store(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Store data in memory."""
        pass
    
    @abstractmethod
    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve data from memory."""
        pass
    
    @abstractmethod
    async def forget(self, key: str) -> bool:
        """Remove data from memory."""
        pass

class InMemoryStorage(BaseMemory):
    """Simple in-memory storage implementation."""
    
    def __init__(self):
        self._storage = {}
    
    async def store(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        self._storage[key] = value
        return True
    
    async def retrieve(self, key: str) -> Optional[Any]:
        return self._storage.get(key)
    
    async def forget(self, key: str) -> bool:
        if key in self._storage:
            del self._storage[key]
            return True
        return False
