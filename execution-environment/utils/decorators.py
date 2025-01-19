import functools
import time
from typing import Callable, Any
from .logger import setup_logger

logger = setup_logger(__name__)

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator for failed operations."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s")
                        time.sleep(wait_time)
            raise last_exception
        return wrapper
    return decorator

def timing(func: Callable) -> Callable:
    """Measure and log function execution time."""
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        logger.debug(f"{func.__name__} took {end_time - start_time:.2f}s to execute")
        return result
    return wrapper
