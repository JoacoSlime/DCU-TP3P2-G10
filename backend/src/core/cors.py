from typing import Unpack

from flask.app import Flask
from flask_cors import CORS
from flask_cors.core import CorsOptionsInput

cors = CORS()


def init_app(app: Flask, **kwargs: Unpack[CorsOptionsInput]):
    cors.init_app(app, **kwargs)
