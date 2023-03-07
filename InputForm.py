from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class InputForm(FlaskForm):
    formula = StringField('Атом', validators=[DataRequired()])
    isotope_mass = StringField('Масса изотопа (если изотоп)')
    submit = SubmitField('Расчитать')
