from typing import cast

from flask import Blueprint, jsonify, request
from flask_jwt_extended.utils import get_current_user

from src.core.measure import add_measure
from src.core.schemas import measures_schema, spot_schema, spots_schema
from src.core.spot import add_spot, delete_spot, get_spot, list_spots
from src.core.user.user import User
from src.core.validations.spots_validation import AddSpotForm
from src.web.wrappers.auth_wrapper import need_permission

spots_bp = Blueprint("spots_bp", __name__, url_prefix="/api/spots")


@spots_bp.get("/get/<int:spot_id>")
def get(spot_id: int):
    spot = get_spot(spot_id)

    if not spot:
        return jsonify(message="Punto no encontrado"), 404

    return jsonify(spot_schema.dump(spot))


@spots_bp.get("/list")
def list():
    title = request.args.get("title")

    spots = list_spots(1, title)

    return jsonify(spots_schema.dump(spots))


@spots_bp.get("/list/<int:page>")
def list_page(page: int):
    if page < 1:
        return jsonify(message="La paginación empieza por 1"), 400

    title = request.args.get("title")

    spots = list_spots(page, title)

    return jsonify(spots_schema.dump(spots))


@spots_bp.get("/measures/<int:spot_id>")
def measures(spot_id: int):
    spot = get_spot(spot_id)

    if not spot:
        return jsonify(message="Punto no encontrado"), 404

    return jsonify(measures_schema.dump(spot.measures))


@spots_bp.post("/add")
@need_permission("spots.add")
def add():
    form = cast(AddSpotForm, AddSpotForm.from_json(request.json))  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportAny]
    if not form.validate_on_submit():  # pyright: ignore[reportUnknownMemberType]
        return jsonify(message=form.errors), 400

    user = cast(User, get_current_user())

    # Esto es horrible pero es culpa de Python..
    spot = add_spot(
        form.title.data,  # pyright: ignore[reportArgumentType]
        form.latitude.data,  # pyright: ignore[reportArgumentType]
        form.longitude.data,  # pyright: ignore[reportArgumentType]
    )

    if not spot:
        return jsonify(message="Ya existe un punto con ese título"), 400

    measure = add_measure(
        spot.id,
        form.items_per_m2.data,  # pyright: ignore[reportArgumentType]
        form.weight.data,  # pyright: ignore[reportArgumentType]
        form.area.data,  # pyright: ignore[reportArgumentType]
        form.pet.data,  # pyright: ignore[reportArgumentType]
        form.pead.data,  # pyright: ignore[reportArgumentType]
        form.pebd.data,  # pyright: ignore[reportArgumentType]
        form.pvc.data,  # pyright: ignore[reportArgumentType]
        form.pp.data,  # pyright: ignore[reportArgumentType]
        form.ps.data,  # pyright: ignore[reportArgumentType]
        form.pa.data,  # pyright: ignore[reportArgumentType]
        form.other.data,  # pyright: ignore[reportArgumentType]
        form.ihr_plata.data,  # pyright: ignore[reportArgumentType]
        form.ibirp.data,  # pyright: ignore[reportArgumentType]
        user,
    )

    if not measure:
        return jsonify(message="Error al crear la medición del punto"), 500

    return jsonify(spot_schema.dump(spot))


@spots_bp.delete("/delete/<int:spot_id>")
@need_permission("spots.delete")
def delete(spot_id: int):
    result = delete_spot(spot_id)

    if not result:
        return jsonify(message="Punto no encontrado"), 404

    return jsonify(message="Punto eliminado correctamente")
