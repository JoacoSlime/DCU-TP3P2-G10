from typing import final

from flask_wtf import FlaskForm  # pyright: ignore[reportMissingTypeStubs]
from wtforms import EmailField, PasswordField, validators


@final
class LoginForm(FlaskForm):
    email = EmailField(None, [validators.InputRequired(), validators.Email()])
    password = PasswordField(None, [validators.InputRequired()])
