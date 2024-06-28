from flask import Blueprint, render_template, request, redirect, session, url_for, flash
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
    if current_user.is_authenticated:
        profile_image = None
    else:
        profile_image = None
    return render_template("home.html", profile_image=profile_image)