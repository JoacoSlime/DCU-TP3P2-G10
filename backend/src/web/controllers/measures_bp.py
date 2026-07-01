from typing import cast

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_current_user

from src.core.measure import add_measure, delete_measure, get_measure, list_measures
from src.core.schemas import measure_schema, measures_schema
from src.core.user.user import User
from src.core.validations.measures_validation import AddMeasureForm
from src.web.wrappers.auth_wrapper import need_permission

measures_bp = Blueprint("measures_bp", __name__, url_prefix="/api/measures")


@measures_bp.get("/get/<int:measure_id>")
def get(measure_id: int):
    measure = get_measure(measure_id)

    if not measure:
        return jsonify(message="Medición no encontrada"), 404

    return jsonify(measure_schema.dump(measure))


@measures_bp.get("/list")
def list():
    measures = list_measures(1)

    return jsonify(measures_schema.dump(measures))


@measures_bp.get("/list/<int:page>")
def list_page(page: int):
    if page < 1:
        return jsonify(message="La paginación empieza por 1"), 400

    measures = list_measures(page)

    return jsonify(measures_schema.dump(measures))


@measures_bp.post("/add")
@need_permission("measures.add")
def add():
    form = cast(AddMeasureForm, AddMeasureForm.from_json(request.json))  # pyright: ignore[reportAny, reportUnknownMemberType, reportAttributeAccessIssue]
    if not form.validate_on_submit():  # pyright: ignore[reportUnknownMemberType]
        return jsonify(message=form.errors), 400

    user = cast(User, get_current_user())

    # Esto es horrible pero es culpa de Python...
    measure = add_measure(
        form.spot_id.data,  # pyright: ignore[reportArgumentType]
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
        return jsonify(message="No se encontró un punto con ese id"), 404

    return jsonify(measure_schema.dump(measure))


@measures_bp.delete("/delete/<int:measure_id>")
@need_permission("measures.remove")
def delete(measure_id: int):
    result = delete_measure(measure_id)

    if not result:
        return jsonify(message="Medición no encontrada"), 404

    return jsonify(message="Medición eliminada correctamente")
