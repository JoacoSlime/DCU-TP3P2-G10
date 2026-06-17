from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    get_current_user,
    verify_jwt_in_request,  # pyright: ignore[reportUnknownVariableType]
)

from src.core.user.user import User


def need_permission(permission: str):  # pyright: ignore[reportUnknownParameterType]
    def wrapper(fn):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        @wraps(fn)  # pyright: ignore[reportUnknownArgumentType]
        def decorator(*args, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
            _ = verify_jwt_in_request()  # pyright: ignore[reportUnknownVariableType]
            user: User = get_current_user()  # pyright: ignore[reportAny]
            if user.has_permission(permission):
                return fn(*args, **kwargs)  # pyright: ignore[reportUnknownVariableType]
            else:
                return jsonify(
                    status="fail",
                    message=f"Se requiere el permiso {permission} para realizar esta acción.",
                ), 403

        return decorator  # pyright: ignore[reportUnknownVariableType]

    return wrapper  # pyright: ignore[reportUnknownVariableType]
