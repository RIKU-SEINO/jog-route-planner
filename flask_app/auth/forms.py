from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length
import re


class SignUpForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired("ユーザー名は必須です。"),
            Length(1, 30, "30文字以内で入力してください。")
        ],
    )
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。")
        ],
    )
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードは必須です。"),

        ],
    )
    submit = SubmitField("新規登録")

    def validate_password(self, password):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$')
        if not pattern.match(password.data):
            raise ValidationError("英大文字・英小文字・数字の全てを1つ以上含む必要があります。")
        

class LoginForm(FlaskForm):
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。")
        ],
    )
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードは必須です。"),

        ],
    )
    submit = SubmitField("ログイン")

    def validate_password(self, password):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$')
        if not pattern.match(password.data):
            raise ValidationError("正しい形式で入力してください。")