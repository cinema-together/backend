import logging

import jwt
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    UnauthenticatedUser,
    BaseUser,
)

from settings import get_settings

logger = logging.getLogger(__name__)
security = HTTPBearer()


class CustomUser(BaseUser):  # noqa
    def __init__(self, id: str, login: str) -> None:
        self.id = id
        self.login = login

    @property
    def is_authenticated(self) -> bool:
        return True

    def as_dict(self):
        return self.__dict__


class CustomAuthBackend(AuthenticationBackend):

    async def authenticate(self, request):
        settings = get_settings()
        authorization: str = request.headers.get('Authorization')
        scheme, credentials = get_authorization_scheme_param(authorization)
        if scheme.lower() != 'bearer':
            return AuthCredentials(), UnauthenticatedUser()

        if not credentials:
            return AuthCredentials(), UnauthenticatedUser()

        # Checks the validity of the JWT token, if token is invalid returns UnauthenticatedUser object
        try:
            jwt_decoded = jwt.decode(credentials, settings.jwt_secret, algorithms=[settings.jwt_alg])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return AuthCredentials(), UnauthenticatedUser()

        # In case if token is valid returns an object of the authorized user
        try:
            auth_user = CustomUser(
                id=jwt_decoded['sub'],
                login=jwt_decoded['login'],
            )
        except KeyError:
            logger.error(f'Bad signature for user: {jwt_decoded}')
            return AuthCredentials(), UnauthenticatedUser()

        return AuthCredentials(['authenticated']), auth_user
