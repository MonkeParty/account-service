from fastapi import Request
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.config import get_auth_config
from app.exceptions import TokenNotFoundException, TokenExpiredException, NoSubInTokenException, UserNotFoundException, \
    InvalidTokenException
from app.users.dao import UserDAO

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({'exp': expire})
    auth_config = get_auth_config()
    access_token = jwt.encode(to_encode, auth_config['access_secret_key'], algorithm=auth_config['algorithm'])
    return access_token

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({'exp': expire})
    auth_config = get_auth_config()
    encoded_jwt = jwt.encode(to_encode, auth_config['refresh_secret_key'], algorithm=auth_config['algorithm'])
    return encoded_jwt

def get_access_token_from_request(request: Request) -> str:
    token_from_cookies = request.cookies.get('auth_token')
    token_from_header = request.headers.get('Authorization')

    if token_from_cookies is not None:
        return token_from_cookies
    else:
        if token_from_header is not None:
            return token_from_header
        raise TokenNotFoundException

async def token_filter(claims: dict):
    expire: str = claims['exp']
    expire_time = datetime.fromtimestamp(int(expire), timezone.utc)

    if (not expire) or (expire_time <= datetime.now(timezone.utc)):
        raise TokenExpiredException

    email: str = claims['sub']
    if not email:
        raise NoSubInTokenException

    user = await UserDAO.find_by_email(email)
    if not user:
        raise UserNotFoundException


async def get_access_claims(request: Request) -> dict:
    token = get_access_token_from_request(request)
    auth_config = get_auth_config()

    try:
        access_claims = jwt.decode(token, auth_config['access_secret_key'], algorithms=auth_config['algorithm'])
    except JWTError:
        raise InvalidTokenException

    await token_filter(access_claims)

    return access_claims

async def get_refresh_claims(token: str) -> dict:
    auth_config = get_auth_config()

    try:
        refresh_claims = jwt.decode(token, auth_config['refresh_secret_key'], algorithms=auth_config['algorithm'])
    except JWTError:
        raise InvalidTokenException

    await token_filter(refresh_claims)

    return refresh_claims

def is_admin(claims: dict) -> bool:
    return claims['is_admin']

def is_manager(claims: dict) -> bool:
    return claims['is_manager']

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
