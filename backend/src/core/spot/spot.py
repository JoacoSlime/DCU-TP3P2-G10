# pyright: reportImportCycles=false
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, override

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Numeric, String
from sqlalchemy.util.typing import final

from src.core.db import Model

if TYPE_CHECKING:
    from src.core.measure.measure import Measure


@final
class Spot(Model):
    __tablename__ = "spots"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)

    latitude: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=8))
    longitude: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=8))

    measures: Mapped[list[Measure]] = relationship(
        back_populates="spot", cascade="all, delete-orphan"
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    @override
    def __repr__(self) -> str:
        return f"< Spot #{self.id} : {self.title} ({self.latitude}, {self.longitude})>"
