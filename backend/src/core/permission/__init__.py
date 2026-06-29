from sqlalchemy import insert, select

from src.core.db import db

from .permission import Permission


def list_permissions():
    """
    List all permissions.
    """
    permissions = db.session.execute(select(Permission)).scalars().all()

    return permissions


def create_permission(name: str) -> Permission:
    """
    Create a new permission
    """
    name = name.lower()
    permission = Permission(name=name)

    db.session.add(permission)
    db.session.commit()

    return permission


def get_permission_by_name(name: str) -> Permission | None:
    """
    Returns a Permission given the name if it exists.
    """
    name = name.lower()
    permission = db.session.execute(
        select(Permission).where(Permission.name == name)
    ).scalar_one_or_none()

    return permission


### Development functions ###


def seed_permisions():
    """
    Seeds permissions.
    """
    permissions = [
        "collaborators.add",
        "collaborators.remove",
        "collaborators.list",
        "measures.add",
        "measures.remove",
        "spots.add",
        "spots.remove",
    ]
    for permission in permissions:
        _ = db.session.execute(insert(Permission).values(name=permission))

    db.session.commit()
