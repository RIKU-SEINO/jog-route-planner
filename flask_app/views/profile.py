from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_app.models.users import User
from flask_app.models.courses import Course

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