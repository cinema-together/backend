import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from services.room_service import RoomService, get_room_service
from services.user_service import get_user_service, UserService
from settings import get_settings

router = APIRouter()


@router.post("/create", description='Создание комнаты')
async def crate_room(request: Request,
                     room_service: RoomService = Depends(get_room_service),
                     user_service: UserService = Depends(get_user_service),
                     settings=Depends(get_settings)):
    user = await user_service.get_user(request)
    room_id = str(uuid.uuid4())
    user = {
        'id': user['id'],
        'login': user['login'],
    }
    data = {
        "users": [user, ],
        "admin": user['id'],
    }
    await room_service.create_or_update_room(room_id, data)
    join_url = f'{settings.project_protocol}{settings.project_host}:{settings.project_port}/api/v1/room/join/{room_id}'
    return JSONResponse(status_code=HTTPStatus.CREATED,
                        content={
                            'room_id': room_id,
                            'join_url': join_url,
                        })


@router.get("/join/{room_id}")
async def join_to_room(request: Request,
                       room_id: str,
                       room_service: RoomService = Depends(get_room_service),
                       user_service: UserService = Depends(get_user_service),
                       ):
    user = await user_service.get_user(request)
    room = await room_service.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Вы перешли по неверной ссылке или комната не существует")

    room_users = room.get('users')
    for room_user in room_users:
        if room_user['id'] != user['id']:
            continue
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                            detail="Вы уже находитесь в этой комнате")

    new_user_data = {
        'id': user['id'],
        'login': user['login'],
    }
    room_users.append(new_user_data)
    room['users'] = room_users
    await room_service.create_or_update_room(room_id, room)
    return JSONResponse(status_code=HTTPStatus.CREATED, content=new_user_data)


@router.post("/disconnect/{room_id}")
async def disconnect(request: Request,
                     room_id: str,
                     room_service: RoomService = Depends(get_room_service),
                     user_service: UserService = Depends(get_user_service),
                     ):
    user = await user_service.get_user(request)
    user_id = user['id']
    room = await room_service.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Комната не существует")

    # Хз, если админ закрыл комнату, то удалить ее
    if room['admin'] == user_id:
        await room_service.del_room(room_id)
        return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content={
            "message": "Комната удалена"
        })

    room_users = room['users']
    for room_user in room_users:
        if user_id == room_user['id']:
            room_users.remove(user)
            room['users'] = room_users
            await room_service.create_or_update_room(room_id, room)
            return JSONResponse(status_code=HTTPStatus.NO_CONTENT,
                                content={
                                    'message': f'Пользователь {user["login"]} удален'
                                })

    raise HTTPException(HTTPStatus.NOT_FOUND,
                        detail="Вы не находитесь в этой комнате")
