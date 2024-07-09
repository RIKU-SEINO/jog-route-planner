from flask_app import db
from flask_app.config import Config
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_app.models.users import User
from flask_app.models.courses import Course
from flask_app.forms.auth_forms import EditUserForm
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

profile = Blueprint(
    'profile',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/user',
)

@profile.route("/<userid>", methods=["GET","POST"])
def index(userid):
    user = User.query.filter_by(id=userid).first()
    if user:
        form = EditUserForm()
        if current_user.is_authenticated and str(current_user.id) == str(userid):
            courses = Course.query.filter_by(user_id=userid).all()
            if request.method == "POST":
                filename = secure_filename(form.profile_image.data.filename)
                if allowed_file(filename):
                    form.profile_image.data.save(os.path.join(Config.USER_PROFILE_IMAGE_UPLOAD_FOLDER, filename))
                    user.profile_image = filename
                    db.session.commit()

                    flash("プロフィール画像を変更しました。", "success")
                    return redirect(url_for('profile.index', userid=current_user.id))
                else:
                    flash("jpg, jpeg, png以外のファイルは対応しておりません。", "failure")
                    return redirect(url_for('profile.index', userid=current_user.id))

        else:
            courses = Course.query.filter_by(user_id=user.id, is_public=True).all()
        return render_template("user.html", user=user, courses=courses, form=form)
    else:
        return render_template("404.html")
    
@profile.route("/<user_id>/edit", methods=["GET","POST"])
def settings(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user and (current_user.is_authenticated and str(current_user.id) == str(user_id)):
        form = EditUserForm(obj=user)
        if request.method == "POST":
            user.username = form.username.data
            previous_email = user.email
            user.email = form.email.data
            user.password = form.password.data
            user.bio = form.bio.data
            if form.address.data:
                user.address = form.address.data.name
            else:
                user.address = "設定なし"
            if user.is_duplicated_email() and user.email != previous_email:
                flash("そのメールアドレスはすでにご登録いただいております。", "failure")
                return redirect(url_for('profile.settings', user_id=current_user.id))
            
            db.session.commit()
            flash("プロフィールの変更が完了しました。","success")
            return redirect(url_for('profile.index', userid=current_user.id))
        
        return render_template('user_edit.html',form=form)
    else:
        return render_template("404.html")