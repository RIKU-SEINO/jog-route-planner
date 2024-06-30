from flask_app.forms import *

def prefecture_query():
    return Prefecture.query

def facility_query():
    return Facility.query

class CreateCourseForm(FlaskForm):
    title = StringField(
        "コースのタイトル",
        validators=[
            DataRequired("コースタイトルは必須です。"),
            Length(1, 50, "50文字以内で入力してください。")
        ],
    )
    description = TextAreaField(
        "コースの説明",
        validators=[
            DataRequired("コースの説明は必須です。"),
            Length(1, 200, "200文字以内で入力してください。")
        ]
    )
    prefecture = QuerySelectField(
        "都道府県",
        query_factory=prefecture_query,
        get_label='name',
        allow_blank=False,
        validators=[DataRequired("都道府県は必須です。")]
    )
    city = SelectField(
        "市区町村",
        choices=[],
        validate_choice=False
    )
    facilities = QuerySelectMultipleField(
        "近くの施設",
        query_factory=facility_query,
        get_label='name',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    submit = SubmitField("投稿する")
