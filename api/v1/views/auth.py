from fastapi import APIRouter, Depends
from starlette.requests import Request

from services.auth import OAuth, get_auth_service

router = APIRouter()


@router.get('/login')
async def login(request: Request, oauth: OAuth = Depends(get_auth_service)):
    """Переход на страницу аутентификации."""
    redirect_uri = request.url_for('callback')
    return await oauth.authorize_redirect(request, redirect_uri)


@router.get('/logout')
def logout():
    """Удаление сессии."""
    pass


@router.get('/callback')
async def callback(request: Request, oauth: OAuth = Depends(get_auth_service)):
    """Получение токена от провайдера."""
    token = await oauth.authorize_access_token(request)
    user = token['userinfo']
    return dict(user)
