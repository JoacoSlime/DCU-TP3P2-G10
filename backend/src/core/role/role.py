# pyright: reportImportCycles=false
from datetime import datetime
from typing import TYPE_CHECKING, override

from sqlalchemy import Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.types import String
from sqlalchemy.util.typing import final

from src.core.db import Model

if TYPE_CHECKING:
    from src.core.permission.permission import Permission
    from src.core.user.user import User

roles_permissions = Table(
    "roles_permissions",
    Model.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),  # pyright: ignore[reportUnknownArgumentType]
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),  # pyright: ignore[reportUnknownArgumentType]
)


@final
class Role(Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    permissions: Mapped[list["Permission"]] = relationship(
        back_populates="roles", secondary=roles_permissions
    )
    users: Mapped[list["User"]] = relationship(back_populates="role")

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    def has_permission(self, checking: str) -> bool:
        checking = checking.lower()

        for permission in self.permissions:
            if permission.name == checking:
                return True

        return False

    @override
    def __repr__(self) -> str:
        return f"< Role #{self.id} : {self.name}>"
