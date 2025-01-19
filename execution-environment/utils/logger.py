import logging
from ..config.settings import Settings

def setup_logger(name: str) -> logging.Logger:
    """Setup and return a logger instance."""
    settings = Settings()
    
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
        logger.addHandler(handler)
    
    return logger
