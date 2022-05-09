from functools import lru_cache
from os import environ

from pydantic import BaseSettings as PydanticBaseSettings
from pydantic import RedisDsn


class BaseSettings(PydanticBaseSettings):
    """Базовый конфиг для приложения."""

    get_user_url = 'http://localhost:5001/v1/get-user'
    redis_dsn: RedisDsn
    project_protocol: str = 'http://'
    project_host: str = 'localhost'
    project_port: int = 8000
    sentry_dsn: str
    environment: str = environ.get('APP_ENV', 'development')
    testing: bool = False

    class Config(object):
        env_file = 'config/.env'


@lru_cache()
def get_settings() -> BaseSettings:
    """Возвращает конфигурацию приложения."""
    return BaseSettings()
