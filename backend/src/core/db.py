from flask import Flask
from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy_utils import (  # pyright: ignore[reportMissingTypeStubs]
    create_database,  # pyright: ignore[reportUnknownVariableType]
    database_exists,  # pyright: ignore[reportUnknownVariableType]
    drop_database,  # pyright: ignore[reportUnknownVariableType]
)

db: SQLAlchemy = SQLAlchemy()


class Model(DeclarativeBase):
    pass


def init_app(app: Flask):
    """
    Initializes and configures the database.
    """
    db.init_app(app)
    config(app)


def config(app: Flask):
    """
    Configures the database teardown.
    """

    @app.teardown_request
    def close_db_session(exception=None):
        db.session.close()


def reset():
    """
    Reset the database
    """
    print("Reiniciando la base de datos...")
    for engine in db.engines.values():
        if database_exists(engine.url):
            drop_database(engine.url)
        create_database(engine.url)

    Model.metadata.create_all(db.engines["default"])

    print("Base de datos creada")
