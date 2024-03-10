from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask_app.app import db
from flask_app.auth.models import User
from flask_app.auth.forms import SignUpForm, LoginForm
from flask_login import login_user, logout_user

auth = Blueprint(
    'auth',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/auth',
)

@auth.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next_ = request.args.get('next')
            if next_ is None or not next_.startswith("/"):
                next_ = url_for("profile.index")
            return redirect(next_)
        else:
            flash("メールアドレスまたはパスワードが違います。")
    return render_template("login.html", form=form)

@auth.route("/signup", methods=["GET","POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )

        if user.is_duplicated_email():
            flash("そのメールアドレスはすでにご登録いただいております。")
            return redirect(url_for('auth.signup'))

        db.session.add(user)
        db.session.commit()

        login_user(user)
        next_ = request.args.get('next')
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("profile.index")
        return redirect(next_)
    
    else:
        return render_template("signup.html", form=form)

