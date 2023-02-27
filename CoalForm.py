from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CoalForm(FlaskForm):
    text = TextAreaField('Текст забивочки', validators=[DataRequired()])
    submit = SubmitField('Раскумарить')
