from flask_app import db
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_app.models.users import User
from flask_app.models.courses import Course
from flask_app.forms.auth_forms import EditUserForm

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
        if current_user.is_authenticated and str(current_user.id) == str(userid):
            courses = Course.query.filter_by(user_id=userid).all()
        else:
            courses = Course.query.filter_by(user_id=user.id, is_public=True).all()
        return render_template("user.html", user=user, courses=courses)
    else:
        return "ユーザーは存在しません"
    
@profile.route("/<user_id>/edit", methods=["GET","POST"])
def settings(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        if current_user.is_authenticated and str(current_user.id) == str(user_id):
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
                    flash("そのメールアドレスはすでにご登録いただいております。")
                    return redirect(url_for('profile.settings', user_id=current_user.id))
                
                db.session.commit()
                flash("プロフィールの変更が完了しました。","success")
                return redirect(url_for('profile.index', userid=current_user.id))
            
            return render_template('user_edit.html',form=form)
        return "このユーザーの編集権限はありません。"
    else:
        return "ユーザーは存在しません"