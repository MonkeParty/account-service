from fastapi import APIRouter, Response, Request

from app.users.schemas import SUserRegister, SUserLogin
from app.users.service import sign_up, log_in, secured_method

router = APIRouter(prefix='/api/auth', tags=['Auth'])

@router.post('/sign_up')
async def register(user_data: SUserRegister) -> dict:
    response_body = await sign_up(user_data)
    return response_body

@router.post('/login')
async def login(response: Response, user_data: SUserLogin) -> dict:
    response_body = await log_in(response=response, auth_data=user_data)
    return response_body

@router.get('/secured')
async def secured(request: Request) -> dict:
    response = await secured_method(request)
    return response