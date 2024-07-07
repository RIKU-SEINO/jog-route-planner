from flask_app.forms import *


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

class EditUserForm(SignUpForm):
    username = StringField(
        "変更後のユーザー名",
        validators=[
            DataRequired("ユーザー名は必須です。"),
            Length(1, 30, "30文字以内で入力してください。")
        ],
    )
    email = StringField(
        "変更後のメールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。")
        ],
    )
    password = PasswordField(
        "変更後のパスワード",
        validators=[
            DataRequired("パスワードは必須です。"),

        ],
    )
    bio = TextAreaField(
        "あなたの紹介文",
        validators=[
            Length(0, 100, "100文字以内で入力してください。")
        ]
    )
    address =  QuerySelectField(
        "お住まいの地域",
        query_factory=prefecture_query,
        get_label='name',
    )
    profile_image = FileField(
        'プロフィール画像',
        validators=[
            Length(max=255, message='ファイル名は255文字以下で入力してください。'),
            FileAllowed(['jpg', 'jpeg', 'png'], "jpgn jpeg, pngのみサポートしております。")
        ]
        
    )
    submit = SubmitField("更新")

