from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, RadioField, FloatField, FieldList
from wtforms.validators import DataRequired, Email


class CarwashForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    id = StringField("id: ", validators=[DataRequired()])
    enable = BooleanField("enable: ", validators=[DataRequired()])
    address = StringField("address: ", validators=[DataRequired()])
    Location = StringField("Location: ", validators=[DataRequired()])
    Type = RadioField("Name: ", validators=[DataRequired()])
    stepCost = FloatField("stepCost: ", validators=[DataRequired()])
    limitMinCost = FloatField("limitMinCost: ", validators=[DataRequired()])
    Price = FloatField("Price: ", validators=[DataRequired()])
    Boxes = StringField("stepCost: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


