from pydantic import SecretStr
from pydantic_settings import BaseSettings


class _AppConfig(BaseSettings):
    BOT_TOKEN: SecretStr
    WEBAPP_URL: str

    APP_HOST: str = "localhost"
    APP_PORT: int = 8000

    SMTP_HOST: str
    SMTP_PORT: int
    IMAP_HOST: str
    IMAP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    class Config:
        # env_file = "../.env"
        env_file = ".env"
        env_file_encoding = "utf-8"


AppConfig = _AppConfig()
