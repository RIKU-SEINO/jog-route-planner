from flask import Blueprint, render_template
from flask_login import current_user

home = Blueprint(
    'home',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/',
)

@home.route("/", methods=["GET","POST"])
def index():
    return render_template("home.html")