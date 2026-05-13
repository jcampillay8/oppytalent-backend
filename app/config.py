from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://portafolio:portafolio_secret@[::1]:5443/portafolio"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    admin_username: str = "admin"
    admin_password: str = "admin123"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
