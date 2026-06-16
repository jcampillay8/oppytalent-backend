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
    
    # Auth & Env
    ENVIRONMENT: str = "development"
    API_URL: str = "http://localhost:8000/api"
    WEBSITE_URL: str = "http://localhost:5173"
    JWT_ACCESS_SECRET_KEY: str = "super-secret-access"
    JWT_REFRESH_SECRET_KEY: str = "super-secret-refresh"
    ENCRYPTION_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Encryption (Fernet key for API keys)
    ENCRYPTION_KEY: str | None = None
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Cloudflare R2 Integration (Premium Storage)
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = ""
    R2_PUBLIC_URL: str = ""
    
    # Google OAuth (Free Tier Drive Uploads)
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"
    
    # Email
    EMAIL_PROVIDER: str = "smtp"
    MAIL_USERNAME: str = "dummy_user"
    MAIL_PASSWORD: str = "dummy_password"
    MAIL_FROM: str = "no-reply@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.example.com"
    MAIL_FROM_NAME: str = "OppyTalent"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    SUPPORT_EMAIL: str = "support@example.com"
    RESEND_API_KEY: str | None = None

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # Pydantic leerá el archivo .env en local de manera automática
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()