from fastapi import Request

from app.exceptions import ForbiddenException, UserNotFoundException
from app.users.dao import UserDAO
from app.users.security import get_access_claims

async def get_all_users_as_admin_or_manager(request: Request) -> list[dict]:
    current_user = await get_current_user_from_request(request)

    if (not current_user.is_admin) and (not current_user.is_manager):
        raise ForbiddenException

    all_users = await UserDAO.find_all()

    return [{
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'middle_name': user.middle_name,
        'birth_date': user.birth_date
    } for user in all_users]

async def get_user_by_id_as_admin_or_manager(request:Request, user_id: int) -> dict:
    current_user = await get_current_user_from_request(request)

    if (not current_user.is_admin) and (not current_user.is_manager):
        raise ForbiddenException

    user = await UserDAO.find_by_id(data_id=user_id)

    if not user:
        raise UserNotFoundException

    return {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'middle_name': user.middle_name,
        'birth_date': user.birth_date
    }


async def make_manager_from_user_as_admin(request: Request, user_id: int):
    current_user = await get_current_user_from_request(request)

    if not current_user.is_admin:
        raise ForbiddenException

    user = await UserDAO.find_by_id(data_id=user_id)

    if not user:
        raise UserNotFoundException

    filter_by = {'id': user_id}
    values = {'is_manager': True}

    await UserDAO.update(
        filter_by,
        **values
    )

async def get_current_user_from_request(request: Request):
    access_claims = await get_access_claims(request)
    email = access_claims['sub']
    current_user = await UserDAO.find_by_email(email=email)
    return current_user