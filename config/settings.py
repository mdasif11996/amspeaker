import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class AppConfig:
    """Centralized configuration management for production"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.cache_ttl = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour default
        self.max_history_items = int(os.getenv("MAX_HISTORY_ITEMS", "100"))
        self.enable_analytics = os.getenv("ENABLE_ANALYTICS", "true").lower() == "true"
        self.app_version = "2.0.0"
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.api_base_url = "https://api.groq.com/openai/v1"
        self.model_name = "llama-3.3-70b-versatile"
    
    def validate(self):
        """Validate configuration"""
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required")
        return True


config = AppConfig()
