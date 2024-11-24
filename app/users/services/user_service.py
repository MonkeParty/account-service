from fastapi import Request, Response

from app.exceptions import IncorrectEmailOrPasswordException
from app.users.dao import UserDAO
from app.users.security import get_access_claims, verify_password, get_password_hash
from app.users.schemas import SUserUpdateCommonInfo, SUserUpdatePassword, SUserUpdateEmail


async def get_current_user(request: Request) -> dict:
    access_claims = await get_access_claims(request)
    email = access_claims['sub']
    user = await UserDAO.find_by_email(email)

    return {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'middle_name': user.middle_name,
        'birth_date': user.birth_date
    }

async def update_current_user_common_info(request: Request, user_data: SUserUpdateCommonInfo):
    access_claims = await get_access_claims(request)
    user_data_dict = user_data.model_dump()
    email = access_claims['sub']

    values = {
        'first_name': user_data_dict['first_name'],
        'last_name': user_data_dict['last_name'],
        'middle_name': user_data_dict['middle_name'],
        'birth_date': user_data_dict['birth_date']
    }

    filter_by = {'email': email}

    await UserDAO.update(
        filter_by,
        **values
    )

async def update_current_user_password(request: Request, user_data: SUserUpdatePassword):
    access_claims = await get_access_claims(request)
    email = access_claims['sub']
    user_data_dict = user_data.model_dump()
    old_password = user_data_dict['old_password']
    new_password = user_data_dict['new_password']

    user = await UserDAO.find_by_email(email=email)

    if verify_password(plain_password=old_password, hashed_password=user.password):
        new_hashed_password = get_password_hash(new_password)

        values = {'password': new_hashed_password}
        filter_by = {'email': email}

        await UserDAO.update(
            filter_by,
            **values
        )
    else:
        raise IncorrectEmailOrPasswordException

async def update_current_user_email(request: Request, response: Response, user_data: SUserUpdateEmail):
    access_claims = await get_access_claims(request)
    email = access_claims['sub']
    user_data_dict = user_data.model_dump()
    new_email = user_data_dict['new_email']
    password = user_data_dict['password']

    user = await UserDAO.find_by_email(email=email)

    filter_by = {'email': email}
    values = {'email': new_email}

    if verify_password(plain_password=password, hashed_password=user.password):
        await UserDAO.update(
            filter_by,
            **values
        )
        response.delete_cookie(key='auth_token')
    else:
        raise IncorrectEmailOrPasswordException

async def delete_current_user(request: Request, response: Response):
    access_claims = await get_access_claims(request)
    email = access_claims['sub']
    filter_by = {'email': email}
    await UserDAO.delete(**filter_by)
    response.delete_cookie(key='auth_token')