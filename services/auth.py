from functools import lru_cache

from authlib.integrations.starlette_client import OAuth
from fastapi import Depends

from settings import BaseSettings, get_settings


@lru_cache()
def get_auth_service(settings: BaseSettings = Depends(get_settings)):
    """Возвращает клиент для аутентификации и авторизации."""
    oauth = OAuth()
    oauth.register(
        'auth0',
        client_id=settings.auth0_client_id,
        client_secret=settings.auth0_client_secret,
        api_base_url=settings.auth0_domain,
        server_metadata_url=f'https://{settings.auth0_domain}/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )
    return oauth.auth0
