from fastapi import APIRouter

from app.users.services.sub_service import get_user_sub_info, set_sub_for_user, unsub_user

router = APIRouter(prefix='/api/user', tags=['User subscription'])

@router.get('/check_sub/{id_user}', status_code=200)
async def check_sub(id_user: int):
    return await get_user_sub_info(id_user)

@router.patch('/set_sub/{id_user}', status_code=200)
async def set_sub(id_user: int):
    return await set_sub_for_user(id_user)

@router.patch('/unsub/{id_user}', status_code=200)
async def unsub(id_user: int):
    return await unsub_user(id_user)
