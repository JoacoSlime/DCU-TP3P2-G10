# pyright: reportImportCycles=false
from datetime import datetime
from decimal import Decimal
from typing import override

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Numeric
from sqlalchemy.util.typing import final

from src.core.db import Model
from src.core.spot.spot import Spot
from src.core.user.user import User


@final
class Measure(Model):
    __tablename__ = "measures"
    __table_args__ = (  # pyright: ignore[reportAny]
        CheckConstraint(
            "pet >= 0 and pead >= 0 and pebd >= 0 and pvc >= 0 and pp >= 0 and ps >= 0 and pa >= 0 and other >= 0",
            name="measures_nonnegative_counts_chk",
        ),
        CheckConstraint(
            "items_per_m2 >= 0 and weight >= 0 and area > 0",
            name="measures_nonnegative_base_chk",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    items_per_m2: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=4))
    weight: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=4))
    area: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=4))

    pet: Mapped[int] = mapped_column(default=0)
    pead: Mapped[int] = mapped_column(default=0)
    pebd: Mapped[int] = mapped_column(default=0)
    pvc: Mapped[int] = mapped_column(default=0)
    pp: Mapped[int] = mapped_column(default=0)
    ps: Mapped[int] = mapped_column(default=0)
    pa: Mapped[int] = mapped_column(default=0)
    other: Mapped[int] = mapped_column(default=0)

    ihr_plata: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=4))
    ibirp: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=4))

    # Relationships
    spot_id: Mapped[int] = mapped_column(ForeignKey(Spot.id), index=True)
    collaborator_id: Mapped[int] = mapped_column(ForeignKey(User.id))

    spot: Mapped[Spot] = relationship(back_populates="measures", foreign_keys=[spot_id])
    collaborator: Mapped[User] = relationship(
        back_populates="measures", foreign_keys=[collaborator_id]
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    @override
    def __repr__(self) -> str:
        return f"< Measure #{self.id} ({self.spot_id}, {self.collaborator_id}) :  (item x m^2: {self.items_per_m2}, weight: {self.weight}, area: {self.area}) [pet: {self.items_per_m2}, pead: {self.items_per_m2}, pebd: {self.items_per_m2}, pvc: {self.items_per_m2}, pp: {self.items_per_m2}, ps: {self.items_per_m2}, pa: {self.items_per_m2}, other: {self.items_per_m2} | ihr_plata: {self.ihr_plata}, ibirp: {self.ibirp}]>"
