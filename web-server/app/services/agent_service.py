import redis.asyncio as redis
import json
from ..config import settings
from ..models.requests import AgentRequest, AgentResponse
from tenacity import retry, stop_after_attempt, wait_exponential

class AgentService:
    _instance = None

    def __init__(self):
        self.redis = None
        self.connected = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def connect(self):
        if not self.connected:
            self.redis = await redis.from_url(
                f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
            )
            self.connected = True

    async def disconnect(self):
        if self.redis:
            await self.redis.close()
            self.connected = False

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def send_request(self, request: AgentRequest) -> AgentResponse:
        if not self.connected:
            await self.connect()

        try:
            request_id = await self.redis.incr('request_counter')
            
            request_data = {
                'id': request_id,
                'query': request.query,
                'context': request.context
            }
            
            await self.redis.rpush('agent_requests', json.dumps(request_data))
            
            response_data = await self.redis.blpop(
                f'agent_responses:{request_id}',
                timeout=30
            )
            
            if response_data:
                response = json.loads(response_data[1])
                return AgentResponse(
                    response=response.get('response'),
                    status='success'
                )
            else:
                return AgentResponse(
                    response=None,
                    status='error',
                    error='Request timeout'
                )
                
        except Exception as e:
            return AgentResponse(
                response=None,
                status='error',
                error=str(e)
            )

    async def check_health(self) -> bool:
        try:
            if not self.connected:
                await self.connect()
            await self.redis.ping()
            return True
        except Exception:
            return False

def get_agent_service() -> AgentService:
    return AgentService.get_instance() 