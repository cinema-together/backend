import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from services.room_service import RoomService, get_room_service

router = APIRouter()


@router.post("/", description='Создание комнаты')
async def crate_room(request: Request, room_service: RoomService = Depends(get_room_service)):
    user = request.user
    if not user.is_authenticated:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    room_id = str(uuid.uuid4())
    data = {
        "users": [user.as_dict(), ],
        "admin": user.id,
    }
    await room_service.create_or_update_room(room_id, data)
    return JSONResponse(status_code=HTTPStatus.CREATED,
                        content={
                            'room_id': room_id,
                            'join_url': request.url_for('join_to_room', room_id=room_id),
                        })


@router.patch("/{room_id}", description='Присоединение к комнате')
async def join_to_room(request: Request,
                       room_id: str,
                       room_service: RoomService = Depends(get_room_service),
                       ):
    user = request.user
    if not user.is_authenticated:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    room = await room_service.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Вы перешли по неверной ссылке или комната не существует")

    room_users = room.get('users')
    for room_user in room_users:
        if room_user['id'] != user.id:
            continue
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                            detail="Вы уже находитесь в этой комнате")

    room_users.append(user.as_dict())
    room['users'] = room_users
    await room_service.create_or_update_room(room_id, room)
    return JSONResponse(status_code=HTTPStatus.CREATED, content={'message': f'{user.login} добавлен в комнату'})


@router.delete("/{room_id}", description='Выход из комнаты')
async def disconnect(request: Request,
                     room_id: str,
                     room_service: RoomService = Depends(get_room_service),
                     ):
    user = request.user
    if not user.is_authenticated:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    room = await room_service.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Комната не существует")

    # Хз, если админ закрыл комнату, то удалить ее
    if room['admin'] == user.id:
        await room_service.del_room(room_id)
        return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content={
            "message": "Комната удалена"
        })

    room_users = room['users']
    for idx, room_user in enumerate(room_users):
        if user.id == room_user['id']:
            room_users.pop(idx)
            room['users'] = room_users
            await room_service.create_or_update_room(room_id, room)
            return JSONResponse(status_code=HTTPStatus.NO_CONTENT,
                                content={
                                    'message': f'Пользователь {user.login} удален',
                                })

    raise HTTPException(HTTPStatus.NOT_FOUND, detail="Вы не находитесь в этой комнате")
