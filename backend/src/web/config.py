import secrets
from os import environ
from typing import final

from dotenv import load_dotenv

_ = load_dotenv()


class Config(object):
    """Base configuration."""

    JWT_SECRET_KEY: str = secrets.token_hex(32)
    JWT_TOKEN_LOCATION: list[str] = ["headers"]
    SQLALCHEMY_ECHO: bool = True
    RESEND_KEY: str = environ.get("RESEND_KEY") or (_ for _ in ()).throw(
        ValueError("RESEND_KEY environment variable must be set")
    )
    SECRET_KEY: str = secrets.token_hex()


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
