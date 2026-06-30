from typing import cast

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,  # pyright: ignore[reportUnknownVariableType]
    current_user,  # pyright: ignore[reportAny]
)
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import (
    jwt_required,  # pyright: ignore[reportUnknownVariableType]
)

from src.core.schemas import user_schema
from src.core.user import check_auth
from src.core.validations.auth_validation import LoginForm

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


@auth_bp.route("/me", methods=["GET"])  # pyright: ignore[reportAny]
@jwt_required()  # pyright: ignore[reportAny]
def me():
    return jsonify(user_schema.dump(current_user))


@auth_bp.route("/login", methods=["POST"])
def login():
    form = cast(LoginForm, LoginForm.from_json(request.json))  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportAny]
    if not form.validate_on_submit():  # pyright: ignore[reportUnknownMemberType]
        return jsonify(message=form.errors), 400

    user = check_auth(form.email.data, form.password.data)  # pyright: ignore[reportArgumentType]

    if not user:
        return jsonify(message="El email o contraseña son incorrectos"), 400

    # Checkea que no se inicie un usuario sin finalizar su registro
    if user.generation_token:
        return jsonify(message="Debe finalizar su registro primero"), 400

    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    response = jsonify(access_token=access_token, refresh_token=refresh_token)

    return response


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@auth_bp.route("/refresh", methods=["POST"])  # pyright: ignore[reportAny]
@jwt_required(refresh=True)  # pyright: ignore[reportAny]
def refresh():
    identity = get_jwt_identity()  # pyright: ignore[reportAny]
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@auth_bp.route("/logout", methods=["GET"])  # pyright: ignore[reportAny]
@jwt_required()  # pyright: ignore[reportAny]
def logout():
    response = jsonify(message="Sesión cerrada con éxito")

    return response
