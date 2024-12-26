from fastapi import APIRouter, Request

from app.users.services.manager_service import make_manager_from_user_as_admin, get_all_users_as_admin_or_manager, \
    get_user_by_id_as_admin_or_manager

router = APIRouter(prefix='/api/users', tags=['Manager/Admin'])

@router.get('', status_code=200)
async def get_all(request: Request):
    return await get_all_users_as_admin_or_manager(request=request)

@router.get('/{user_id}', status_code=200)
async def get_user_by_id(request: Request, user_id: int):
    return await get_user_by_id_as_admin_or_manager(request=request, user_id=user_id)

@router.patch('/{user_id}/manager', status_code=204)
async def make_manager_from_user(request: Request, user_id: int):
    await make_manager_from_user_as_admin(request=request, user_id=user_id)
