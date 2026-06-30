from typing import final

from flask_wtf import FlaskForm  # pyright: ignore[reportMissingTypeStubs]
from wtforms import DecimalField, IntegerField, StringField, validators


@final
class AddSpotForm(FlaskForm):
    title = StringField(None, [validators.Length(3)])

    latitude = DecimalField(None, [validators.DataRequired()])
    longitude = DecimalField(None, [validators.DataRequired()])

    items_per_m2 = DecimalField(None, [validators.NumberRange(0)])
    weight = DecimalField(None, [validators.NumberRange(0)])
    area = DecimalField(None, [validators.NumberRange(0)])

    pet = IntegerField(None, [validators.NumberRange(0)])
    pead = IntegerField(None, [validators.NumberRange(0)])
    pebd = IntegerField(None, [validators.NumberRange(0)])
    pvc = IntegerField(None, [validators.NumberRange(0)])
    pp = IntegerField(None, [validators.NumberRange(0)])
    ps = IntegerField(None, [validators.NumberRange(0)])
    pa = IntegerField(None, [validators.NumberRange(0)])
    other = IntegerField(None, [validators.NumberRange(0)])

    ihr_plata = DecimalField(None, [validators.NumberRange(0)])
    ibirp = DecimalField(None, [validators.NumberRange(0)])
