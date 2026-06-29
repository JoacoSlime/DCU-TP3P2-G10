from decimal import Decimal

from sqlalchemy import ColumnElement, insert, select

from src.core.db import db
from src.core.spot.spot import Spot
from src.core.user.user import User


def add_spot(title: str, latitude: Decimal, longitude: Decimal) -> Spot | None:
    """
    Creates a spot.
    Returns `None` if a spot with the give title already exists.
    """
    spot = db.session.execute(
        insert(Spot)
        .values(title=title, latitude=latitude, longitude=longitude)
        .returning(Spot)
    ).scalar_one_or_none()

    if spot:
        db.session.commit()

    return spot


def delete_spot(id: int) -> bool:
    """
    Deletes the spot with the given id.
    Returns `False` if spot doesn't exist.
    """

    spot = db.session.execute(select(Spot).where(Spot.id == id)).scalar_one_or_none()

    if not spot:
        return False

    db.session.delete(spot)
    db.session.commit()

    return True


def list_spots(page: int, title: str | None):
    """
    Returns paginated spot list.
    Can search by fields: title.
    """

    filter: list[ColumnElement[bool]] = []
    if title is not None:
        filter.append(Spot.title.ilike(f"%{title}%"))

    paginated_spots = (
        db.session.execute(
            select(Spot).filter(*filter).limit(25).offset((page - 1) * 25)
        )
        .scalars()
        .all()
    )

    return paginated_spots


def get_spot(id: int) -> Spot | None:
    """
    Returns spot with given id if it exists.
    """
    user = db.session.execute(select(Spot).where(Spot.id == id)).scalar_one_or_none()

    return user
