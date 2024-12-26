import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    REDIS_PORT: str
    REDIS_HOST: str
    REDIS_DB: str
    REDIS_PASSWORD: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str
    KAFKA_BOOTSTRAP_SERVER: str
    EVENT_BUS_TOPIC_NAME: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

settings = Settings()

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

def get_redis_url():
    return f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"

def get_auth_config():
    return {
        "access_secret_key": settings.ACCESS_SECRET_KEY,
        "refresh_secret_key": settings.REFRESH_SECRET_KEY,
        "algorithm": settings.ALGORITHM
    }