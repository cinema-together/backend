import aioredis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.urls import api_router
from db import redis
from settings import get_settings

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
    current_settings = get_settings()
    redis.redis = await aioredis.create_redis_pool(current_settings.redis_dsn, minsize=10, maxsize=20)


@app.on_event('shutdown')
async def shutdown():
    """Запускается при сворачивании приложения."""
    redis.redis.close()


app.include_router(api_router, prefix='/api/v1')
