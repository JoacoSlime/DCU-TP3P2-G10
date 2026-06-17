from typing import final

from flask_wtf import FlaskForm  # pyright: ignore[reportMissingTypeStubs]
from wtforms import DecimalField, IntegerField, validators


@final
class AddMeasureForm(FlaskForm):
    spot_id = IntegerField(None, [validators.DataRequired(), validators.NumberRange(0)])

    items_per_m2 = DecimalField(
        None, [validators.DataRequired(), validators.NumberRange(0)]
    )
    weight = DecimalField(None, [validators.DataRequired(), validators.NumberRange(0)])
    area = DecimalField(None, [validators.DataRequired(), validators.NumberRange(0)])

    pet = IntegerField(None, [validators.DataRequired(), validators.NumberRange(0)])
    pead = IntegerField(None, [validators.DataRequired(), validators.NumberRange(0)])
    pebd = IntegerField(None, [validators.DataRequired(), validators.NumberRange(0)])
    pvc = IntegerField(None, [validators.DataRequired(), validators.NumberRange(0)])
    pp = IntegerField(None, [validators.DataRequired(), validators.NumberRange(0)])
    ps = IntegerField(None, [validators.DataRequired(), validators.NumberRange(0)])
    pa = IntegerField(None, [validators.DataRequired(), validators.NumberRange(0)])
    other = IntegerField(None, [validators.DataRequired(), validators.NumberRange(0)])

    ihr_plata = DecimalField(
        None, [validators.DataRequired(), validators.NumberRange(0)]
    )
    ibirp = DecimalField(None, [validators.DataRequired(), validators.NumberRange(0)])
