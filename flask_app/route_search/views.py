from flask import Blueprint, render_template, request, jsonify
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
    return "コース検索画面一覧"