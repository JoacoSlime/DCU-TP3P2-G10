from dataclasses import dataclass
from typing import Literal, TypedDict

from sqlalchemy import insert, select

from src.core.db import db
from src.core.permission import get_permission_by_name, seed_permisions
from src.core.permission.permission import Permission

from .role import Role


def get_collaborator_role() -> Role:
    """
    Returns the collaborator role.
    """
    return db.session.execute(
        select(Role).where(Role.name == "collaborator")
    ).scalar_one()


def get_admin_role() -> Role:
    """
    Returns the admin role.
    """
    return db.session.execute(
        select(Role).where(Role.name == "administrator")
    ).scalar_one()


def get_role(id: int) -> Role | None:
    """
    Fetchs role with given id.
    Returns `None` if role with such id doesn't exist.
    """
    return db.session.execute(select(Role).where(Role.id == id)).scalar_one_or_none()


def get_role_by_name(name: str) -> Role | None:
    """
    Fetchs role with given name.
    Returns `None` if role with such name doesn't exist.
    """
    name = name.lower()

    return db.session.execute(
        select(Role).where(Role.name == name)
    ).scalar_one_or_none()


def add_role(name: str) -> Role | None:
    """
    Adds a role, returns `None` if it already exists.
    """
    name = name.lower()

    role = db.session.execute(
        insert(Role).values(name=name).returning(Role)
    ).scalar_one_or_none()

    return role


@dataclass
class AssingPermissionResponse(TypedDict):
    success: bool
    reason: Literal["success", "role_not_found", "permission_not_found"]


def assign_permission(role_id: int, permission_id: int):
    """
    Assigns permissions to a role.
    Return `None`
    """

    permission = db.session.execute(
        select(Permission).where(Permission.id == permission_id)
    ).scalar_one_or_none()

    if not permission:
        return AssingPermissionResponse(success=False, reason="permission_not_found")

    role = db.session.execute(
        select(Role).where(Role.id == role_id)
    ).scalar_one_or_none()

    if not role:
        return AssingPermissionResponse(success=False, reason="role_not_found")

    role.permissions.append(permission)
    db.session.commit()


### Development functions ###


def seed_roles():
    """
    Seeds roles.
    """

    # Be sure permissions are seeded
    seed_permisions()

    collaborator_permissions = [
        get_permission_by_name("measures.add"),
        get_permission_by_name("spots.add"),
    ]
    collaborator_permissions = [p for p in collaborator_permissions if p is not None]

    admin_permissions = collaborator_permissions + [
        get_permission_by_name("collaborators.add"),
        get_permission_by_name("collaborators.remove"),
        get_permission_by_name("collaborators.list"),
        get_permission_by_name("measures.remove"),
        get_permission_by_name("spots.remove"),
    ]
    admin_permissions = [p for p in admin_permissions if p is not None]

    collaborator_role = db.session.execute(
        insert(Role).values(name="collaborator").returning(Role)
    ).scalar_one()
    admin_role = db.session.execute(
        insert(Role).values(name="administrator").returning(Role)
    ).scalar_one()

    collaborator_role.permissions = collaborator_permissions
    admin_role.permissions = admin_permissions

    db.session.commit()
