from fastapi import APIRouter

from api.v1.views import auth, room

api_router = APIRouter()
api_router.include_router(auth.router, prefix='/oauth', tags=['oauth'])
api_router.include_router(room.router, prefix='/rooms', tags=['room'])
