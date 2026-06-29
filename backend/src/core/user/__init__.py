import secrets
from dataclasses import dataclass
from typing import Literal, TypedDict

from sqlalchemy import ColumnElement, insert, select
from werkzeug.security import check_password_hash, generate_password_hash

from src.core.db import db
from src.core.role import get_admin_role, get_collaborator_role
from src.core.role.role import Role
from src.core.user.user import User


def list_users(page: int, email: str | None = None, role: Role | None = None):
    """
    Returns paginated user list.
    Can search by fields: email and role.
    """

    filter: list[ColumnElement[bool]] = []
    if email is not None:
        filter.append(User.email.ilike(f"%{email}%"))
    if role is not None:
        filter.append(User.role == role)

    paginated_users = (
        db.session.execute(
            select(User).filter(*filter).limit(25).offset((page - 1) * 25)
        )
        .scalars()
        .all()
    )

    return paginated_users


@dataclass
class UserResult(TypedDict):
    id: int
    email: str


def add_user(email: str) -> tuple[User, str] | None:
    """
    Creates a new using with a random password and generation token, returning the user and the generation token.
    Returns `None` if email is not unique.
    """

    password_hash = generate_password_hash(secrets.token_urlsafe(16))

    token = secrets.token_urlsafe(16)

    token_hash = generate_password_hash(token)

    user = db.session.execute(
        insert(User)
        .values(email=email, password=password_hash, generation_token=token_hash)
        .returning(User)
    ).scalar_one_or_none()

    if user:
        db.session.commit()

    return (user, token) if user else None


def complete_register(
    token: str, name: str, surname: str, password: str
) -> User | None:
    """
    Completes the registration of the user with the associated token.
    Returns `None` if a user with such token doesn't exist.
    """

    user = db.session.execute(
        select(User).where(User.generation_token == token)
    ).scalar_one_or_none()

    if user:
        collaborator_role = get_collaborator_role()
        password_hash = generate_password_hash(password)

        user.password = password_hash
        user.name = name
        user.surname = surname
        user.role = collaborator_role
        user.generation_token = None

        db.session.commit()

    return user


@dataclass
class PasswordChangeResult(TypedDict):
    success: bool
    reason: Literal["user_not_found", "incorrect_password", "success"]


def change_user_password(
    id: int, old_password: str, new_password: str
) -> PasswordChangeResult:
    """
    Updates user password if the old_password coincides with current password.
    """

    user = db.session.execute(select(User).where(User.id == id)).scalar_one_or_none()

    if not user:
        return PasswordChangeResult(success=False, reason="user_not_found")

    if not check_password_hash(user.password, old_password):
        return PasswordChangeResult(success=False, reason="incorrect_password")

    user.password = generate_password_hash(new_password)
    db.session.commit()

    return PasswordChangeResult(success=True, reason="success")


def change_user_email(id: int, email: str) -> User | None:
    """
    Updates the user email based on the user id.
    Returns `None` if user with such id doesn't exists.
    """

    user = db.session.execute(select(User).where(User.id == id)).scalar_one_or_none()

    if user:
        user.email = email
        db.session.commit()

    return user


def delete_user(id: int) -> bool:
    """
    Deletes the user with the given id.
    Returns `False` if user doesn't exist.
    """

    user = db.session.execute(select(User).where(User.id == id)).scalar_one_or_none()

    if not user:
        return False

    db.session.delete(user)
    db.session.commit()

    return True


def get_user(id: int) -> User | None:
    """
    Returns user with given id if it exists.
    """
    user = db.session.execute(select(User).where(User.id == id)).scalar_one_or_none()

    return user


def get_user_by_email(email: str) -> User | None:
    """
    Returns user with given email if it exists.
    """
    user = db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    return user


def check_auth(email: str, password: str) -> User | None:
    """
    Returns user if given email and password match.
    """
    email = email.lower()
    user = get_user_by_email(email)

    if not user:
        return None

    if not check_password_hash(user.password, password):
        return None

    return user


### Development functions ###


def seed_admin():
    """
    Development function.
    Seeds an admin account.
    """
    user = get_user_by_email("admin@admin.com")

    if not user:
        result = add_user("admin@admin.com")
        if not result:
            return
        (user, _) = result

    admin_role = get_admin_role()
    password_hash = generate_password_hash("admin")

    user.generation_token = None
    user.password = password_hash
    user.role = admin_role
    user.name = "Admin"
    user.surname = "Admin"
    db.session.commit()
