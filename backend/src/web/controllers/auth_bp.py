from typing import cast

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,  # pyright: ignore[reportUnknownVariableType]
    current_user,  # pyright: ignore[reportAny]
    set_access_cookies,  # pyright: ignore[reportUnknownVariableType]
    unset_jwt_cookies,
)
from flask_jwt_extended.view_decorators import (
    jwt_required,  # pyright: ignore[reportUnknownVariableType]
)

from src.core.user import check_auth
from src.core.validations.auth_validation import LoginForm

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/me", methods=["GET"])  # pyright: ignore[reportAny]
@jwt_required()  # pyright: ignore[reportAny]
def me():
    return jsonify(
        id=current_user.id,  # pyright: ignore[reportAny]
        email=current_user.email,  # pyright: ignore[reportAny]
        name=current_user.name,  # pyright: ignore[reportAny]
        surname=current_user.surname,  # pyright: ignore[reportAny]
    )


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

    response = jsonify(token=access_token)

    set_access_cookies(response, access_token)

    return response


@auth_bp.route("/logout", methods=["GET"])  # pyright: ignore[reportAny]
@jwt_required()  # pyright: ignore[reportAny]
def logout():
    response = jsonify(message="Sesión cerrada con éxito")

    unset_jwt_cookies(response)

    return response
