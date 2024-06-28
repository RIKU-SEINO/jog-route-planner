from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_app.models.users import User

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
    if current_user.is_authenticated:
        profile_image = None
    else:
        profile_image = None
    public_profile_image = None
    if public_profile_image is not None:
        return render_template("profile.html", user=user, public_profile_image=public_profile_image, profile_image=profile_image)
    else:
        return redirect(url_for("error.index"))