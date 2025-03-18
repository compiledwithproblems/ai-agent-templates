from typing import Any, List, Dict
from openai import AsyncOpenAI
from .agent import BaseAgent
from .memory import InMemoryStorage
from .tools.code_analysis import analyze_code_structure, suggest_improvements, track_code_changes
from ..config.settings import Settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class OpenAIAgent(BaseAgent):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL_NAME
    
    def _setup_memory(self):
        """Initialize in-memory storage"""
        self.memory = InMemoryStorage()
    
    def _load_tools(self):
        """Load code analysis tools"""
        self.tools = [
            analyze_code_structure,
            suggest_improvements,
            track_code_changes
        ]
    
    async def analyze_code(self, code: str) -> Dict:
        """Analyze code and provide insights with memory of previous analyses"""
        # Get current analysis
        current_analysis = await analyze_code_structure(code)
        
        # Get previous analysis from memory
        previous_analysis = await self.memory.retrieve("previous_code_analysis")
        
        # Track changes if we have previous analysis
        if previous_analysis:
            changes = await track_code_changes(current_analysis, previous_analysis)
            current_analysis["changes"] = changes
        
        # Get improvement suggestions
        suggestions = await suggest_improvements(current_analysis)
        current_analysis["suggestions"] = suggestions
        
        # Store current analysis for future comparison
        await self.memory.store("previous_code_analysis", current_analysis)
        
        return current_analysis
    
    async def process(self, input_data: Any) -> Any:
        """Process input using OpenAI"""
        # Check if input is code analysis request
        if isinstance(input_data, dict) and input_data.get("type") == "code_analysis":
            return await self.analyze_code(input_data["code"])
        
        # Regular conversation processing
        context = await self.memory.retrieve("conversation_history") or []
        context.append({"role": "user", "content": str(input_data)})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=context,
            temperature=0.7
        )
        
        context.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        await self.memory.store("conversation_history", context)
        
        return response.choices[0].message.content
    
    async def think(self, context: Any) -> List[str]:
        """Strategic thinking using OpenAI"""
        if isinstance(context, dict) and "code_analysis" in context:
            # Analyze code-specific context
            thoughts = [
                f"Code has {context['complexity_indicators']['num_functions']} functions",
                f"Found {len(context.get('suggestions', []))} potential improvements",
                "Considering historical changes and patterns"
            ]
            return thoughts
        
        # Regular thinking process
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": f"Given this context, what should be considered? Context: {context}"
            }],
            temperature=0.7
        )
        return [response.choices[0].message.content] 