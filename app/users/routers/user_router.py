from fastapi import APIRouter, Request, Response

from app.users.schemas import SUserUpdateCommonInfo, SUserUpdatePassword, SUserUpdateEmail
from app.users.services.user_service import get_current_user, update_current_user_common_info, \
    update_current_user_password, update_current_user_email, delete_current_user

router = APIRouter(prefix='/api/users/current', tags=['Current User'])

@router.get('', status_code=200)
async def current_user_get(request: Request) -> dict:
    response = await get_current_user(request)
    return response

@router.patch('/update/common', status_code=204)
async def current_user_update_common_info(request: Request, user_data: SUserUpdateCommonInfo):
    await update_current_user_common_info(request, user_data)

@router.patch('/update/password', status_code=204)
async def current_user_update_password(request: Request, user_data: SUserUpdatePassword):
    await update_current_user_password(request, user_data)

@router.patch('/update/email', status_code=204)
async def current_user_update_email(request: Request, response: Response, user_data: SUserUpdateEmail):
    await update_current_user_email(request, response, user_data)

@router.delete('',status_code=204)
async def current_user_delete(request: Request, response: Response):
    await delete_current_user(request, response)