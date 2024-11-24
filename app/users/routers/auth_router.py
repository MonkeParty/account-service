from fastapi import APIRouter, Response

from app.users.schemas import SUserRegister, SUserLogin, SUserRefresh
from app.users.services.auth_service import sign_up, log_in, refresh_access_token, log_out

router = APIRouter(prefix='/api/auth', tags=['Auth'])

@router.post('/sign_up')
async def register(user_data: SUserRegister) -> dict:
    response_body = await sign_up(user_data)
    return response_body

@router.post('/login')
async def login(response: Response, user_data: SUserLogin) -> dict:
    response_body = await log_in(response=response, auth_data=user_data)
    return response_body

@router.post('/refresh')
async def refresh(response: Response, user_data: SUserRefresh) -> dict:
    return await refresh_access_token(response=response, user_data=user_data)

@router.post('/logout', status_code=204)
def logout(response: Response):
    log_out(response=response)