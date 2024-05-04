from flask import Blueprint, render_template, abort

error = Blueprint(
    'error',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/error'
)

@error.route("/404", methods=["GET"])
def index():
    return render_template("index.html")