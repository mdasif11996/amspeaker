import time
import logging
from config.settings import config

logger = logging.getLogger(__name__)


class CacheManager:
    """Simple in-memory cache for production performance"""
    
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
    
    def get(self, key):
        """Get cached value if not expired"""
        if key in self.cache:
            timestamp = self.timestamps[key]
            if time.time() - timestamp < config.cache_ttl:
                logger.info(f"Cache hit for key: {key}")
                return self.cache[key]
        return None
    
    def set(self, key, value):
        """Cache a value with current timestamp"""
        self.cache[key] = value
        self.timestamps[key] = time.time()
        logger.info(f"Cache set for key: {key}")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.timestamps.clear()
        logger.info("Cache cleared")
