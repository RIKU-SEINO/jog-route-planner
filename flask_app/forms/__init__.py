from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, FileField, TextAreaField, SelectField, FloatField, BooleanField, widgets, ValidationError
from wtforms.validators import DataRequired, Email, Length, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_app.models.address import Prefecture
from flask_app.models.facilities import Facility
import re

def prefecture_query():
    return Prefecture.query

def facility_query():
    return Facility.query