from sqlalchemy import select, update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import User

class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_by_email(cls, email: str):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(email=email)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_has_sub(cls, id_user: int) -> bool:
        async with async_session_maker() as session:
            query = select(cls.model.has_sub).filter_by(id=id_user)
            result = await session.execute(query)
            has_sub_value = result.scalar_one_or_none()
            return has_sub_value
