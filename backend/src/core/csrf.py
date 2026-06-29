from flask.app import Flask
from flask_wtf.csrf import CSRFProtect  # pyright: ignore[reportMissingTypeStubs]

csrf = CSRFProtect()


def create_app(app: Flask):
    """
    Initializes the csrf protection.
    """
    csrf.init_app(app)  # pyright: ignore[reportUnknownMemberType]
