from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь с таким email уже существует')

UserNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                      detail='Пользователя с таким email не существует')

IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Неверная почта или пароль')

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='Токен истёк')

TokenNotFoundException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Access токен отсутствует в cookies/header')

InvalidTokenException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Некорректный JWT-токен')

InvalidRefreshTokenException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail='Некорректный Refresh-токен')

NoSubInTokenException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Отсутствует subject в JWT-токене')

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                   detail='Недостаточно прав доступа')