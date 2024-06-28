from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask_app.models.users import User
from flask_app.forms.auth_forms import SignUpForm, LoginForm
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import os
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = os.path.join('flask_app', 'static', 'profile-image')


auth = Blueprint(
    'auth',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/auth',
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("profile.index", userid=current_user.id))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next_ = request.args.get('next')
            if next_ is None or not next_.startswith("/"):
                next_ = url_for("profile.index", userid=user.id)
            return redirect(next_)
        else:
            flash("メールアドレスまたはパスワードが違います。")
    return render_template("login.html", form=form)

@auth.route("/signup", methods=["GET","POST"])
def signup():
    form = SignUpForm()
    if current_user.is_authenticated:
        return redirect(url_for("profile.index", userid=current_user.id))
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        profile_image = request.files['profile_image']
        profile_image_filename = profile_image.filename
        user = User(
            username = username,
            email = email,
            password = password
        )
        if user.is_duplicated_email():
            flash("そのメールアドレスはすでにご登録いただいております。")
            return redirect(url_for('auth.signup'))
        
        db.session.add(user)
        db.session.commit()
        
        if profile_image and allowed_file(profile_image_filename):
            filename = f"{str(uuid.uuid4())}_{secure_filename(profile_image_filename)}"
            profile_image.save(os.path.join(UPLOAD_FOLDER, filename))
            image = ProfileImage(filename=filename, user_id=user.id)
        elif profile_image and not allowed_file(profile_image_filename):
            flash("png, jpg, jpeg以外のファイルはサポートしておりません。")
            return redirect(url_for('auth.signup'))
        else:
            default_image_filename = 'default-user.png'
            image = ProfileImage(filename=default_image_filename, user_id=user.id)

        db.session.add(image)
        db.session.commit()

        login_user(user)
        next_ = request.args.get('next')
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("profile.index", userid=user.id)
        return redirect(next_)
    
    else:
        return render_template("signup.html", form=form)
    
@auth.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for("home.index"))