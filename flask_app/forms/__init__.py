from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, FileField, ValidationError
from wtforms.validators import DataRequired, Email, Length
import re