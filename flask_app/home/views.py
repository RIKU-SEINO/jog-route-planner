from flask import Blueprint, render_template, request, redirect, session, url_for, flash

home = Blueprint(
    'home',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/home',
)

@home.route("/", methods=["GET","POST"])
def index():
    return render_template("home.html")