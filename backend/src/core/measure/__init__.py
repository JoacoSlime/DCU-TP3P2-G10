from decimal import Decimal

from sqlalchemy import ColumnElement, insert, select

from src.core.db import db
from src.core.measure.measure import Measure
from src.core.spot.spot import Spot
from src.core.user.user import User


def add_measure(
    spot_id: int,
    items_per_m2: Decimal,
    weight: Decimal,
    area: Decimal,
    pet: int,
    pead: int,
    pebd: int,
    pvc: int,
    pp: int,
    ps: int,
    pa: int,
    other: int,
    ihr_plata: Decimal,
    ibirp: Decimal,
    collaborator: User,
) -> Measure | None:
    """
    Creates a measure.
    Returns `None` if a spot with the given id doesn't exist.
    """
    spot = db.session.execute(
        select(Spot).where(Spot.id == spot_id)
    ).scalar_one_or_none()

    if not spot:
        return None

    measure = db.session.execute(
        insert(Measure)
        .values(
            items_per_m2=items_per_m2,
            weight=weight,
            area=area,
            pet=pet,
            pead=pead,
            pebd=pebd,
            pvc=pvc,
            pp=pp,
            ps=ps,
            pa=pa,
            other=other,
            ihr_plata=ihr_plata,
            ibirp=ibirp,
        )
        .returning(Measure)
    ).scalar_one()
    measure.spot = spot
    measure.collaborator = collaborator
    db.session.commit()

    return measure


def delete_measure(id: int) -> bool:
    """
    Deletes the measures with the given id.
    Returns `False` if measure doesn't exist.
    """

    measure = db.session.execute(
        select(Measure).where(Measure.id == id)
    ).scalar_one_or_none()

    if not measure:
        return False

    db.session.delete(measure)
    db.session.commit()

    return True


def list_measures(page: int):
    """
    Returns paginated measures list.
    """

    paginated_measures = (
        db.session.execute(select(Measure).limit(25).offset((page - 1) * 25))
        .scalars()
        .all()
    )

    return paginated_measures


def get_measure(id: int) -> Measure | None:
    """
    Returns user with given id if it exists.
    """
    measure = db.session.execute(
        select(Measure).where(Measure.id == id)
    ).scalar_one_or_none()

    return measure
