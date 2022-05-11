import aioredis
from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.urls import api_router
from db import redis
from settings import BaseSettings, get_settings

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
    redis.redis = aioredis.from_url(current_settings.redis_dsn, encoding='utf8', decode_responses=True)


@app.on_event('shutdown')
async def shutdown():
    """Запускается при сворачивании приложения."""
    await redis.redis.close()


@app.get('/health')
def health(current_settings: BaseSettings = Depends(get_settings)):
    """Эндпоинт проверки работоспособности сервиса."""
    return {
        'environment': current_settings.environment,
        'testing': current_settings.testing,
    }


app.include_router(api_router)
