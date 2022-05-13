from functools import lru_cache
from pickle import dumps, loads

from aioredis import Redis
from fastapi import Depends

from db.redis import get_redis


class RoomService:
    """Класс для создания комнат для просмотра фильмов"""

    def __init__(self, storage: Redis):
        self.storage = storage
        self.ROOM_LIVE_TIME = 3600  # 6h

    async def create_or_update_room(self, room_id: str, data: dict) -> None:
        await self.storage.set(room_id, dumps(data), expire=self.ROOM_LIVE_TIME)

    async def del_room(self, room_id: str) -> None:
        await self.storage.delete(room_id)

    async def get_room_by_id(self, room_id: str):
        room = await self.storage.get(room_id)
        if room:
            return loads(room)


@lru_cache()
def get_room_service(storage: Redis = Depends(get_redis)) -> RoomService:
    return RoomService(storage)
