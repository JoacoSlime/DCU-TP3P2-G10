from flask.app import Flask
from flask_jwt_extended import JWTManager

from src.core.user import get_user
from src.core.user.user import User

jwt = JWTManager()


def init_app(app: Flask):
    jwt.init_app(app)

    @jwt.user_identity_loader  # pyright: ignore[reportUnknownMemberType]
    def user_identity_lookup(user: User):  # pyright: ignore[reportUnusedFunction]
        return str(user.id)

    @jwt.user_lookup_loader  # pyright: ignore[reportUnknownMemberType]
    def user_lookup_callback(_jwt_header, jwt_data):  # pyright: ignore[reportUnusedFunction, reportUnknownParameterType, reportMissingParameterType]
        identity = int(jwt_data["sub"])  # pyright: ignore[reportUnknownArgumentType]
        return get_user(identity)
