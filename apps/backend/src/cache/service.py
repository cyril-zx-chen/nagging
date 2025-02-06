import json
from typing import Optional
import hashlib

from redis import Redis
from pydantic import BaseModel

class CacheConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    ttl: int = 3600  # 1 hour default TTL

class CacheService:
    def __init__(self, config: CacheConfig = CacheConfig()):
        self.redis = Redis(
            host=config.host,
            port=config.port,
            decode_responses=True,
        )
        self.ttl = config.ttl

    def _generate_key(self, text: str, **kwargs) -> str:
        """Generate a cache key from text and additional parameters."""
        # Sort kwargs to ensure consistent key generation
        kwargs_str = json.dumps(dict(sorted(kwargs.items())))
        key_string = f"{text}:{kwargs_str}"
        return hashlib.md5(key_string.encode()).hexdigest()

    async def get(self, text: str, **kwargs) -> Optional[str]:
        """Get cached suggestion."""
        key = self._generate_key(text, **kwargs)
        return self.redis.get(key)

    async def set(self, text: str, suggestion: str, **kwargs) -> None:
        """Cache a suggestion."""
        key = self._generate_key(text, **kwargs)
        self.redis.setex(key, self.ttl, suggestion)

    async def delete(self, text: str, **kwargs) -> None:
        """Delete a cached suggestion."""
        key = self._generate_key(text, **kwargs)
        self.redis.delete(key) 