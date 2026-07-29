import secrets
from datetime import timedelta
from os import environ
from typing import final

from dotenv import load_dotenv

_ = load_dotenv()


class Config:
    """Base configuration."""


    def __init__(self) -> None:
        self.JWT_SECRET_KEY: str = secrets.token_hex(32)
        self.JWT_TOKEN_LOCATION: list[str] = ["headers"]
        self.JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=1)
        self.JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=30)
        self.SQLALCHEMY_ECHO: bool = True
        self.SMTP_HOST: str = environ.get("SMTP_HOST") or (_ for _ in ()).throw(
            ValueError("SMTP_HOST environment variable must be set")
        )
        self.SMTP_PORT: int = int(
            environ.get("SMTP_PORT")
            or (_ for _ in ()).throw(
                ValueError("SMTP_PORT environment variable must be set")
            )
        )
        self.SMTP_LOGIN: str = environ.get("SMTP_LOGIN") or (_ for _ in ()).throw(
            ValueError("SMTP_LOGIN environment variable must be set")
        )
        self.SMTP_PASSWORD: str = environ.get("SMTP_PASSWORD") or (_ for _ in ()).throw(
            ValueError("SMTP_PASSWORD environment variable must be set")
        )
        self.SECRET_KEY: str = secrets.token_hex()
        self.WTF_CSRF_ENABLED: bool = False


@final
class ProductionConfig(Config):
    """Production environment configuration."""

    def __init__(self) -> None:
        super().__init__()
        self.SQLALCHEMY_ENGINES = {"default": environ.get("DATABASE_URL")}
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": 10,
            "pool_recycle": 60,
            "pool_pre_ping": True,
        }
        self.JWT_SECRET_KEY = environ.get("JWT_SECRET") or (_ for _ in ()).throw(
            ValueError("JWT_SECRET environment variable must be set")
        )
        self.SQLALCHEMY_ECHO = False
        self.SECRET_KEY: str = environ.get("FLASK_SECRET_KEY") or (_ for _ in ()).throw(
            ValueError("FLASK_SECRET_KEY environment variable must be set")
        )


@final
class DevelopmentConfig(Config):
    """Development environment configuration."""

    def __init__(self) -> None:
        super().__init__()
        self.SQLALCHEMY_ENGINES = {"default": "sqlite:///default.sqlite"}


config: dict[str, Config] = {
    "production": ProductionConfig(),
    "development": DevelopmentConfig(),
}
