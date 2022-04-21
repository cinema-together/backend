from functools import lru_cache

from aioredis import Redis

redis: Redis = None


@lru_cache()
async def get_redis() -> Redis:
    """Возвращает redis."""
    return redis
