from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://jcampillay:BTC.100K.jc@[::1]:5443/portafolio"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    admin_username: str = "admin"
    admin_password: str = "admin123"
    gemini_api_key: str = ""
    DB_SCHEMA: str | None = None

    # Pydantic leerá el archivo .env en local de manera automática
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()