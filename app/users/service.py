from fastapi import Response, Request

from app.exceptions import UserAlreadyExistsException, UserNotFoundException, IncorrectEmailOrPasswordException
from app.users.dao import UserDAO
from app.users.schemas import SUserRegister, SUserLogin
from app.users.security import get_password_hash, verify_password, create_access_token, create_refresh_token, \
    get_access_claims
from app.config import settings


async def sign_up(user_data: SUserRegister) -> dict:
    user = await UserDAO.find_by_email(email=user_data.email)

    if user:
        raise UserAlreadyExistsException

    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_dict['password'])

    if (user_data.email == settings.ADMIN_USERNAME) and (user_data.password == settings.ADMIN_PASSWORD):
        user_dict['is_admin'] = True

    await UserDAO.add(**user_dict)
    return user_dict

async def log_in(response: Response, auth_data: SUserLogin) -> dict:
    user = await UserDAO.find_by_email(email=auth_data.email)

    if not user:
        raise IncorrectEmailOrPasswordException

    if verify_password(plain_password=auth_data.password, hashed_password=user.password):
        claims = {
            "sub": user.email,
            "is_admin": user.is_admin,
            "is_manager": user.is_manager
        }

        access_token = create_access_token(data=claims)
        refresh_token = create_refresh_token(data=claims)

        """
        Here need to put refresh_token into cache
        """

        response.set_cookie(key='auth_token', value=access_token, httponly=True)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    raise IncorrectEmailOrPasswordException

async def secured_method(request: Request):
    claims = await get_access_claims(request)
    return claims