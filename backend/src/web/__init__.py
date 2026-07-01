from os import environ

import wtforms_json  # pyright: ignore[reportMissingTypeStubs]
from flask import Flask, jsonify

from src.core import cors, db, jwt, mail, seeds
from src.web.controllers.auth_bp import auth_bp
from src.web.controllers.measures_bp import measures_bp
from src.web.controllers.spots_bp import spots_bp
from src.web.controllers.users_bp import users_bp

from .config import config


def create_app(env: str = "production") -> Flask:
    app = Flask(__name__)
    wtforms_json.init()

    app.config.from_object(config[env])

    db.init_app(app)
    jwt.init_app(app)
    mail.init(app)

    # Healtchecker endpoint
    @app.route("/healthcheck")
    def healthcheck():  # pyright: ignore[reportUnusedFunction]
        response = jsonify({"status": "success", "message": "ContaminApp - Grupo10"})
        return response

    # Auth API
    app.register_blueprint(auth_bp)

    # Users API
    app.register_blueprint(users_bp)

    # Spots API
    app.register_blueprint(spots_bp)

    # Measures API
    app.register_blueprint(measures_bp)

    # Start CORS
    origins = [
        "https://localhost",  # Thanks capacitor.
        "http://localhost:5173",
        "http://localhost:8080",
        "http://localhost:5000",
    ]
    public_url = environ.get("URL_BASE_PUBLIC_APP")
    if public_url:
        origins.append(public_url.strip())
    cors.init_app(
        app,
        origins=origins,
        methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Accept", "Content-Type"],
        supports_credentials=True,
    )

    # Commands
    @app.cli.command(name="reset-db")
    def reset_db():  # pyright: ignore[reportUnusedFunction]
        db.reset()

    @app.cli.command(name="seed-db")
    def seeds_db():  # pyright: ignore[reportUnusedFunction]
        seeds.run()

    return app
