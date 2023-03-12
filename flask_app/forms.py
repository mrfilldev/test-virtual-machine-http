from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, RadioField, FloatField, FieldList
from wtforms.validators import DataRequired, Email


class CarwashForm(FlaskForm):
    name = StringField("Название: ", validators=[DataRequired()])
    # id = StringField("id: ", validators=[DataRequired()])
    # enable = BooleanField("enable: ", validators=[DataRequired()])
    Address = StringField("Адрес: ", validators=[DataRequired()])
    Location = StringField("Местоположение: ", validators=[DataRequired()])
    Type = RadioField('Type', choices=[('SelfServiceFixPrice', 'SelfServiceFixPrice'),
                                                       ('SelfService', 'SelfService'),
                                                       ('Manual', 'Manual'),
                                                       ('Portal', 'Portal'),
                                                       ('Tunnel', 'Tunnel'),
                                                       ('Dry', 'Dry')
                                                       ])
    StepCost = FloatField("stepCost: ", validators=[DataRequired()])
    LimitMinCost = FloatField("limitMinCost: ", validators=[DataRequired()])
    Price = FloatField("Цена: ", validators=[DataRequired()])
    # Boxes = StringField("stepCost: ", validators=[DataRequired()])
    Submit = SubmitField("Создать")
