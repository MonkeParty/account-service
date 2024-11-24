from fastapi import Response

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, \
    InvalidRefreshTokenException
from app.users.dao import UserDAO
from app.users.schemas import SUserRegister, SUserLogin, SUserRefresh
from app.users.security import get_password_hash, verify_password, create_access_token, create_refresh_token, get_refresh_claims
from app.config import settings
from app.database import refresh_storage


async def sign_up(user_data: SUserRegister) -> dict:
    user = await UserDAO.find_by_email(email=user_data.email)

    if user:
        raise UserAlreadyExistsException

    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_dict['password'])

    if (user_data.email == settings.ADMIN_USERNAME) and (user_data.password == settings.ADMIN_PASSWORD):

        """
        In future here we need to send check-authorities message to kafka auth topic
        """

        user_dict['is_admin'] = True

    new_instance = await UserDAO.add(**user_dict)

    return {
        "email": new_instance.email,
        "first_name": new_instance.first_name,
        "last_name": new_instance.last_name,
        "middle_name": new_instance.middle_name,
        "birth_date": new_instance.birth_date
    }

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

        await refresh_storage.set(user.email, refresh_token)

        response.set_cookie(key='auth_token', value=access_token, httponly=True)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    raise IncorrectEmailOrPasswordException

async def refresh_access_token(response: Response, user_data: SUserRefresh) -> dict:
    refresh_token = user_data.refresh_token

    refresh_claims = await get_refresh_claims(refresh_token)
    refresh_token_from_cache = await refresh_storage.get(refresh_claims['sub'])

    if refresh_token_from_cache:
        refresh_token_from_cache = refresh_token_from_cache.decode('utf-8')

    if (not refresh_token_from_cache) or (refresh_token != refresh_token_from_cache):
        raise InvalidRefreshTokenException

    access_token = create_access_token(data=refresh_claims)

    response.set_cookie(key='auth_token', value=access_token, httponly=True)

    return {
        "access_token": access_token
    }

def log_out(response: Response):
    response.delete_cookie(key='auth_token')