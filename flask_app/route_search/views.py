from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_app.auth.models import ProfileImage

route_search = Blueprint(
    'route_search',
    __name__,
    static_folder='./static/',
    template_folder='templates',
    url_prefix='/courses'
)

@route_search.route("/",methods=["GET","POST"])
def index():
    if current_user.is_authenticated:
        profile_image = ProfileImage.query.filter_by(user_id=current_user.id).first()
    else:
        profile_image = None
    return render_template("index.html", profile_image=profile_image)