from http import HTTPStatus
from typing import Dict

import aiohttp
from fastapi import HTTPException, Depends

from settings import BaseSettings, get_settings


class UserService:
    def __init__(self, settings):
        self.user_url = settings.get_user_url

    async def get_user(self, request) -> Dict:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=self.user_url, headers=request.headers)
            status_code = response.status
            if status_code != HTTPStatus.OK:
                raise HTTPException(status_code=status_code)

        user_data = await response.json()
        return user_data


def get_user_service(settings: BaseSettings = Depends(get_settings)) -> UserService:
    return UserService(settings)
