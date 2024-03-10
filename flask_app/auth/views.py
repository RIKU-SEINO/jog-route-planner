from flask import Blueprint, render_template, request, redirect, session, url_for
from flask_app.app import db
from flask_app.auth.models import User
from flask_app.auth.forms import UserForm

auth = Blueprint(
    'auth',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/auth',
)

@auth.route("/", methods=["GET","POST"])
def index():
    return render_template("login.html")

@auth.route("/signup", methods=["GET","POST"])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.index'))
    

