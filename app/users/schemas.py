import re
from datetime import date
from fastapi import HTTPException, status

from pydantic import BaseModel, EmailStr, Field, field_validator

class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 символов")
    first_name: str = Field(..., min_length=2, max_length=50, description="Имя от 2 до 50 символов")
    middle_name: str = Field(..., min_length=2, max_length=50, description="Фамилия от 2 до 50 символов")
    last_name: str = Field(..., min_length=2, max_length=50, description="Отчество от 2 до 50 символов")
    birth_date: date = Field(..., description="Дата рождения")

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        if not re.match(r'^[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Некорректный формат электронного адреса"
            )
        return value

    @field_validator("birth_date")
    def validate_birth_date(cls, value: date) -> date:
        if not value < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Дата рождения должна быть в прошлом"
            )
        return value

class SUserLogin(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        if not re.match(r'^[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Некорректный формат электронного адреса"
            )
        return value