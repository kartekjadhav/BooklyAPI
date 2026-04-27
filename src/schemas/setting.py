from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    DOMAIN: str
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_URL: str = "redis://localhost"
    REDIS_PORT: int = 6379
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool
    ITSDANGEROUS_SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

setting = Setting()