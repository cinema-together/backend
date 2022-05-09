from functools import lru_cache
from typing import Optional

from aioredis import Redis

redis: Optional[Redis] = None


@lru_cache()
def get_redis() -> Redis:
    """Возвращает redis."""
    return redis
