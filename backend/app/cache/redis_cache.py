import hashlib
import json
import logging
from typing import Optional, Dict, Any
import redis
from app.config import settings

logger = logging.getLogger("crisis_companion.cache")

class DisasterResponseCache:
    def __init__(self):
        self.redis_client = None
        self._memory_cache: Dict[str, str] = {}
        self.knowledge_version = "v1.0"
        
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=1.5
            )
            self.redis_client.ping()
            logger.info("Connected to Redis server successfully.")
        except Exception as e:
            logger.warning(f"Redis unavailable ({e}). Operating in resilient In-Memory fallback cache mode.")
            self.redis_client = None

    def generate_cache_key(self, question: str, disaster_type: str = "all", language: str = "en") -> str:
        normalized = question.strip().lower()
        raw_key = f"{normalized}:{disaster_type}:{language}:{self.knowledge_version}"
        return f"rag_cache:{hashlib.sha256(raw_key.encode('utf-8')).hexdigest()}"

    def get(self, question: str, disaster_type: str = "all", language: str = "en") -> Optional[Dict[str, Any]]:
        key = self.generate_cache_key(question, disaster_type, language)
        try:
            if self.redis_client:
                data = self.redis_client.get(key)
                if data:
                    logger.debug(f"Redis Cache HIT for key {key}")
                    return json.loads(data)
            elif key in self._memory_cache:
                logger.debug(f"In-Memory Cache HIT for key {key}")
                return json.loads(self._memory_cache[key])
        except Exception as e:
            logger.error(f"Error reading from cache: {e}")
        
        logger.debug(f"Cache MISS for question '{question}'")
        return None

    def set(self, question: str, response_data: Dict[str, Any], disaster_type: str = "all", language: str = "en", ttl: int = None) -> None:
        key = self.generate_cache_key(question, disaster_type, language)
        ttl = ttl or settings.CACHE_TTL_SECONDS
        serialized = json.dumps(response_data)
        
        try:
            if self.redis_client:
                self.redis_client.setex(key, ttl, serialized)
            else:
                self._memory_cache[key] = serialized
        except Exception as e:
            logger.error(f"Error writing to cache: {e}")

    def clear(self) -> bool:
        try:
            if self.redis_client:
                keys = self.redis_client.keys("rag_cache:*")
                if keys:
                    self.redis_client.delete(*keys)
            self._memory_cache.clear()
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False

# Global Singleton
disaster_cache = DisasterResponseCache()
