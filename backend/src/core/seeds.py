from src.core import (
    role,
    user,
)


def run():
    """
    Seeds the database with some initial data.
    """
    role.seed_roles()  # Also seeds permissions
    user.seed_admin()
