from typing import Any, List, Optional
from abc import ABC, abstractmethod
import asyncio
from ..config.settings import Settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.memory = None  # Initialize in subclass
        self.tools = []     # Available tools/skills
        self._initialize()
    
    def _initialize(self):
        """Initialize agent components."""
        logger.info(f"Initializing agent: {self.settings.AGENT_NAME}")
        self._setup_memory()
        self._load_tools()
    
    @abstractmethod
    def _setup_memory(self):
        """Setup agent memory system."""
        pass
    
    @abstractmethod
    def _load_tools(self):
        """Load available tools/skills."""
        pass
    
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """Process input and return response."""
        pass
    
    async def think(self, context: Any) -> List[str]:
        """Strategic thinking before action."""
        pass
    
    async def act(self, thoughts: List[str], context: Any) -> Any:
        """Execute actions based on thoughts."""
        pass
    
    async def reflect(self, action_result: Any, context: Any) -> None:
        """Learn from actions and results."""
        pass
