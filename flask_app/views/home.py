from flask import Blueprint, render_template, request
from flask_login import current_user
from flask_app.forms.course_forms import SearchCourseForm

home = Blueprint(
    'home',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/',
)

@home.route("/", methods=["GET","POST"])
def index():
    form = SearchCourseForm()
    return render_template("home.html", form=form)