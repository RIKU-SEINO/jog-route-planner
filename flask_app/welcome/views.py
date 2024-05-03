from flask import Blueprint, redirect, url_for

welcome = Blueprint(
    'welcome',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/',
)

@welcome.route("/", methods=["GET","POST"])
def index():
    return redirect(url_for('home.index'))