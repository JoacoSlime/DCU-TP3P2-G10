# pyright: reportImportCycles=false
from datetime import datetime
from typing import TYPE_CHECKING, override

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy.util.typing import final

from src.core.db import Model
from src.core.role.role import roles_permissions

if TYPE_CHECKING:
    from src.core.role.role import Role


@final
class Permission(Model):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    roles: Mapped[list["Role"]] = relationship(
        back_populates="permissions", secondary=roles_permissions
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    @override
    def __repr__(self) -> str:
        return f"< Permission #{self.id} : {self.name}>"
