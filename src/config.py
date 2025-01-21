from pydantic import SecretStr
from pydantic_settings import BaseSettings


class _AppConfig(BaseSettings):
    BOT_TOKEN: SecretStr
    WEBAPP_URL: str

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    SMTP_HOST: str
    SMTP_PORT: int
    IMAP_HOST: str
    IMAP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    TG_CHAT_ID: int

    class Config:
        # env_file = "../.env"
        env_file = ".env"
        env_file_encoding = "utf-8"


AppConfig = _AppConfig()
