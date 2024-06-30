from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, FileField, TextAreaField, SelectField, FloatField, widgets, ValidationError
from wtforms.validators import DataRequired, Email, Length, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_app.models.address import Prefecture
from flask_app.models.facilities import Facility
import re