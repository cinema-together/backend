import aioredis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.urls import api_router
from api.v1 import room
from db import redis

app = FastAPI(
    title='API «Кино вместе»',
    description='Сервис совместного просмотра видео',
    version='1.0.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    """Запускается при старте приложения."""
    redis.redis = await aioredis.create_redis_pool(('localhost', 6379), minsize=10, maxsize=20)


@app.on_event('shutdown')
async def shutdown():
    """Запускается при сворачивании приложения."""
    await redis.redis.close()


app.include_router(room.router, prefix='/api/v1/room', tags=['room'])


app.include_router(api_router)
