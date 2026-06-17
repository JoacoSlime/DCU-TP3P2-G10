# pyright: reportImportCycles=false
from datetime import datetime
from typing import TYPE_CHECKING, override

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy.util.typing import final

from src.core.db import Model
from src.core.role.role import Role

if TYPE_CHECKING:
    from src.core.measure.measure import Measure


@final
class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(256))
    name: Mapped[str | None] = mapped_column(String(50))
    surname: Mapped[str | None] = mapped_column(String(50))
    generation_token: Mapped[str | None] = mapped_column(String(256), unique=True)

    role_id: Mapped[int | None] = mapped_column(ForeignKey(Role.id), nullable=True)
    role: Mapped["Role | None"] = relationship(
        back_populates="users", foreign_keys=[role_id]
    )
    measures: Mapped[list["Measure"]] = relationship(back_populates="collaborator")

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    def has_permission(self, permission: str) -> bool:
        return self.role.has_permission(permission) if self.role else False

    @override
    def __repr__(self) -> str:
        return f"< User #{self.id} ({self.email}) : {self.surname}, {self.name} [{self.role}]"
