from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class CoalForm(FlaskForm):
    text = TextAreaField('Текст забивочки', validators=[DataRequired()])
    freq = IntegerField('Частота (1-10)', validators=[DataRequired()])
    submit = SubmitField('Раскумарить')
