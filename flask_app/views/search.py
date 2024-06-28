from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_app.models.facilities import Facility
from flask_app.models.courses import Course
from flask_app.models.address import Prefecture, City

route_search = Blueprint(
    'route_search',
    __name__,
    static_folder='./static/',
    template_folder='templates',
    url_prefix='/courses'
)

@route_search.route("/", methods=["GET","POST"])
def course_list():
    if current_user.is_authenticated:
        profile_image = None
    else:
        profile_image = None
    return render_template("course_list.html", profile_image=profile_image)

@route_search.route("/<course_id>", methods=["GET","POST"])
def course_detail(course_id):
    if current_user.is_authenticated:
        profile_image = None
    else:
        profile_image = None
    return render_template("course_detail.html", profile_image=profile_image)