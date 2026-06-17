from typing import final

from flask_wtf import FlaskForm  # pyright: ignore[reportMissingTypeStubs]
from wtforms import (
    EmailField,
    PasswordField,
    StringField,
    ValidationError,
    validators,
)


@final
class AddUserForm(FlaskForm):
    email = EmailField(None, [validators.InputRequired()])


@final
class ChangeEmailForm(FlaskForm):
    email = EmailField(None, [validators.InputRequired()])


@final
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(None, [validators.InputRequired()])
    new_password = PasswordField(None, [validators.InputRequired()])


@final
class CreatePasswordForm(FlaskForm):
    token = StringField(None, [validators.InputRequired(), validators.Length(1)])
    name = StringField(None, [validators.InputRequired(), validators.Length(1)])
    surname = StringField(None, [validators.InputRequired(), validators.Length(1)])
    password = PasswordField(None, [validators.InputRequired()])

    def validate_password(self, _form: CreatePasswordForm, field: PasswordField):
        assert field.data is not None

        if len(field.data) < 8:
            raise ValidationError(
                "La nueva contraseña debe tener al menos 8 caracteres"
            )

        if not any(ch.isupper() for ch in field.data):
            raise ValidationError(
                "La contraseña debe contener al menos una letra mayúscula"
            )

        if not any(ch.islower() for ch in field.data):
            raise ValidationError(
                "La contraseña debe contener al menos una letra minúscula"
            )

        if not any(ch.isdigit() for ch in field.data):
            raise ValidationError("La contraseña debe contener al menos un número")
