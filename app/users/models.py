from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, str_unique_not_null, int_pk, str_nullable, str_not_null, date_not_null

class User(Base):
    id: Mapped[int_pk]
    email: Mapped[str_unique_not_null]
    password: Mapped[str_not_null]
    first_name: Mapped[str_nullable]
    middle_name: Mapped[str_nullable]
    last_name: Mapped[str_nullable]
    birth_date: Mapped[date_not_null]

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_manager : Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"