import secrets
from datetime import timedelta
from os import environ
from typing import final

from dotenv import load_dotenv

_ = load_dotenv()


class Config(object):
    """Base configuration."""

    JWT_SECRET_KEY: str = secrets.token_hex(32)
    JWT_TOKEN_LOCATION: list[str] = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=30)
    SQLALCHEMY_ECHO: bool = True
    SMTP_HOST: str = environ.get("SMTP_HOST") or (_ for _ in ()).throw(
        ValueError("SMTP_HOST environment variable must be set")
    )
    SMTP_PORT: int = int(
        environ.get("SMTP_PORT")
        or (_ for _ in ()).throw(
            ValueError("SMTP_PORT environment variable must be set")
        )
    )
    SMTP_LOGIN: str = environ.get("SMTP_LOGIN") or (_ for _ in ()).throw(
        ValueError("SMTP_LOGIN environment variable must be set")
    )
    SMTP_PASSWORD: str = environ.get("SMTP_PASSWORD") or (_ for _ in ()).throw(
        ValueError("SMTP_PASSWORD environment variable must be set")
    )
    SECRET_KEY: str = secrets.token_hex()
    WTF_CSRF_ENABLED: bool = False


@final
class ProductionConfig(Config):
    """Production environment configuration."""

    SQLALCHEMY_ENGINES = {"default": environ.get("DATABASE_URL")}
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }
    JWT_SECRET_KEY = environ.get("JWT_SECRET") or (_ for _ in ()).throw(
        ValueError("JWT_SECRET environment variable must be set")
    )
    SQLALCHEMY_ECHO = False
    SECRET_KEY: str = environ.get("FLASK_SECRET_KEY") or (_ for _ in ()).throw(
        ValueError("FLASK_SECRET_KEY environment variable must be set")
    )


@final
class DevelopmentConfig(Config):
    """Development environment configuration."""

    SQLALCHEMY_ENGINES = {"default": "sqlite:///default.sqlite"}


config: dict[str, Config] = {
    "production": ProductionConfig(),
    "development": DevelopmentConfig(),
}
