from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

profile = Blueprint(
    'profile',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/profile',
)

@profile.route("/<userid>", methods=["GET","POST"])
def index(userid):
    return render_template("profile.html", userid=userid)