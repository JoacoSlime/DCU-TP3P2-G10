from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import cast

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (
    get_current_user,
    jwt_required,  # pyright: ignore[reportUnknownVariableType]
)

from src.core.mail import mail
from src.core.role import get_role_by_name
from src.core.schemas import user_schema, users_schema
from src.core.user import (
    add_user,
    change_user_email,
    change_user_password,
    complete_register,
    delete_user,
    get_user,
    list_users,
)
from src.core.user.user import User
from src.core.validations.users_validation import (
    AddUserForm,
    ChangeEmailForm,
    ChangePasswordForm,
    CreatePasswordForm,
)
from src.web.wrappers.auth_wrapper import need_permission

users_bp = Blueprint("users_bp", __name__, url_prefix="/api/users")


@users_bp.get("/get/<int:user_id>")
def get(user_id: int):
    user = get_user(user_id)

    if not user:
        return jsonify(message="Usuario no encontrado"), 404

    return jsonify(user_schema.dump(user))


@users_bp.get("/list")
@need_permission("collaborators.list")
def list():
    email = request.args.get("email")
    role = request.args.get("role")

    role = None if not role else get_role_by_name(role)

    users = list_users(1, email, role)

    return jsonify(users_schema.dump(users))


@users_bp.get("/list/<int:page>")
@need_permission("collaborators.list")
def list_page(page: int):
    if page < 1:
        return jsonify(message="La paginación empieza por 1"), 400

    email = request.args.get("email")
    role = request.args.get("role")

    role = None if not role else get_role_by_name(role)

    users = list_users(page, email, role)

    return jsonify(users_schema.dump(users))


@users_bp.post("/register")
@need_permission("collaborators.add")
def register():
    form = cast(AddUserForm, AddUserForm.from_json(request.json))  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportAny]
    if not form.validate_on_submit():  # pyright: ignore[reportUnknownMemberType]
        return jsonify(message=form.errors), 400

    user = add_user(form.email.data)  # pyright: ignore[reportArgumentType]

    if not user:
        return jsonify(message="Ya existe un punto con ese título"), 400
    (user, token) = user

    # Envio de mail

    if not form.email.data:
        return jsonify(message="Hubo un error al validar el email"), 500

    sender = "contaminapp@demomailtrap.com"
    receiver = form.email.data
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "Invitación a colaborar en ContaminApp"
    body = f"""\
<h1>Fuiste invitade a ContaminApp</h1>

<p>Para finalizar la creación de tu cuenta, crea tu contraseña <a href="http://contaminapp.joacoslime.zapto.org/finalizar_registro?token={token}">aquí</a></p>

<p>O copia este enlace: http://contaminapp.joacoslime.zapto.org/finalizar_registro?token={token}</p>"""
    message.attach(MIMEText(body, "html"))

    try:
        _ = mail.sendmail(sender, receiver, message.as_string())
    except Exception as e:
        current_app.logger.error(e)
        _ = delete_user(user.id)
        return jsonify(message="Hubo un error al enviar el mail"), 500

    return jsonify(user=user_schema.dump(user))


@users_bp.delete("/delete/<int:user_id>")
@need_permission("collaborators.remove")
def delete(user_id: int):
    result = delete_user(user_id)

    if not result:
        return jsonify(message="Usuario no encontrado"), 404

    return jsonify(message="Usuario eliminado correctamente")


@users_bp.post("/change_email")  # pyright: ignore[reportAny]
@jwt_required()  # pyright: ignore[reportAny]
def change_email():
    form = cast(ChangeEmailForm, ChangeEmailForm.from_json(request.json))  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportAny]
    if not form.validate_on_submit():  # pyright: ignore[reportUnknownMemberType]
        return jsonify(message=form.errors), 400

    user = cast(User, get_current_user())

    result = change_user_email(user.id, form.email.data)  # pyright: ignore[reportArgumentType].

    if not result:
        return jsonify(message="Error al obtener el usuario"), 500

    return jsonify(message="Email actualizado correctamente", email=result.email)


@users_bp.post("/change_password")  # pyright: ignore[reportAny]
@jwt_required()  # pyright: ignore[reportAny]
def change_password():
    form = cast(ChangePasswordForm, ChangePasswordForm.from_json(request.json))  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportAny]
    if not form.validate_on_submit():  # pyright: ignore[reportUnknownMemberType]
        return jsonify(message=form.errors), 400

    user = cast(User, get_current_user())

    result = change_user_password(
        user.id,
        form.old_password.data,  # pyright: ignore[reportArgumentType]
        form.new_password.data,  # pyright: ignore[reportArgumentType]
    )

    if not result["success"]:
        if result["reason"] == "incorrect_password":
            return jsonify(message="La contraseña actual no coincide"), 400
        if result["reason"] == "user_not_found":
            return jsonify(message="Error al obtener el usuario"), 500

    return jsonify(message="Contraseña actualizada correctamente")


@users_bp.post("/create_password")
def create_password():
    form = cast(CreatePasswordForm, CreatePasswordForm.from_json(request.json))  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportAny]
    if not form.validate_on_submit():  # pyright: ignore[reportUnknownMemberType]
        return jsonify(message=form.errors), 400

    user = complete_register(
        form.token.data,  # pyright: ignore[reportArgumentType]
        form.name.data,  # pyright: ignore[reportArgumentType]
        form.surname.data,  # pyright: ignore[reportArgumentType]
        form.password.data,  # pyright: ignore[reportArgumentType]
    )

    if not user:
        return jsonify(
            message="No existe un usuario con ese token o ya fue utilizado"
        ), 400

    return jsonify()
