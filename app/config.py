from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # En MAYÚSCULAS. Si Railway o el .env no las encuentran, usarán tu config local por defecto.
    DATABASE_URL: str = "postgresql+asyncpg://jcampillay:BTC.100K.jc@[::1]:5443/portafolio"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    GEMINI_API_KEY: str = ""
    DB_SCHEMA: str | None = None

    # Pydantic leerá el archivo .env en local de manera automática
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()