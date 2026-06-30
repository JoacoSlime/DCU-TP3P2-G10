from typing import final

from flask_wtf import FlaskForm  # pyright: ignore[reportMissingTypeStubs]
from wtforms import DecimalField, IntegerField, StringField, validators


@final
class AddSpotForm(FlaskForm):
    title = StringField(None, [validators.InputRequired(), validators.Length(3)])

    latitude = DecimalField(None, [validators.InputRequired()])
    longitude = DecimalField(None, [validators.InputRequired()])

    items_per_m2 = DecimalField(
        None, [validators.InputRequired(), validators.NumberRange(0)]
    )
    weight = DecimalField(None, [validators.InputRequired(), validators.NumberRange(0)])
    area = DecimalField(None, [validators.InputRequired(), validators.NumberRange(0)])

    pet = IntegerField(None, [validators.InputRequired(), validators.NumberRange(0)])
    pead = IntegerField(None, [validators.InputRequired(), validators.NumberRange(0)])
    pebd = IntegerField(None, [validators.InputRequired(), validators.NumberRange(0)])
    pvc = IntegerField(None, [validators.InputRequired(), validators.NumberRange(0)])
    pp = IntegerField(None, [validators.InputRequired(), validators.NumberRange(0)])
    ps = IntegerField(None, [validators.InputRequired(), validators.NumberRange(0)])
    pa = IntegerField(None, [validators.InputRequired(), validators.NumberRange(0)])
    other = IntegerField(None, [validators.InputRequired(), validators.NumberRange(0)])

    ihr_plata = DecimalField(
        None, [validators.InputRequired(), validators.NumberRange(0)]
    )
    ibirp = DecimalField(None, [validators.InputRequired(), validators.NumberRange(0)])
