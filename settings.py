from functools import lru_cache

from pydantic import BaseSettings as PydanticBaseSettings, RedisDsn, Field


class BaseSettings(PydanticBaseSettings):
    """Базовый конфиг для приложения."""

    project_protocol: str = Field('http://', env='PROJECT_PROTOCOL')
    project_host: str = Field('0.0.0.0', env='PROJECT_HOST')
    project_port: int = Field(8000, env="PROJECT_PORT")
    sentry_dsn: str = Field('', env='SENTRY_DSN')
    environment: str = Field('development', env='APP_ENV')
    testing: bool = False
    redis_dsn: RedisDsn
    auth0_domain: str = Field('', env='AUTH0_DOMAIN')
    auth0_client_id: str = Field('', env='AUTH0_CLIENT_ID')
    auth0_client_secret: str = Field('', env='AUTH0_CLIENT_SECRET')
    jwt_secret: str = Field('', env='JWT_SECRET_KEY')
    jwt_alg: str = Field('HS256', env='JWT_ALG')

    def __hash__(self):
        """Добавляет возможность хеширования для использования lru_cache."""
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config(object):
        env_file = 'config/.env'


@lru_cache()
def get_settings() -> BaseSettings:
    """Возвращает конфигурацию приложения."""
    return BaseSettings()
