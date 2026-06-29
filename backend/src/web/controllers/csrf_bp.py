from flask import Blueprint, jsonify
from flask_wtf.csrf import (  # pyright: ignore[reportMissingTypeStubs]
    generate_csrf,  # pyright: ignore[reportUnknownVariableType]
)

csrf_bp = Blueprint("csrf_bp", __name__, url_prefix="/api/csrf")


@csrf_bp.route("/get", methods=["GET"])
def get_csrf():
    return jsonify(csrf_token=generate_csrf())
