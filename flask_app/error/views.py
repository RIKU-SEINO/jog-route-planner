from flask import Blueprint, render_template, abort

error = Blueprint(
    'error',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/error'
)

@error.route("/404", methods=["GET","POST"])
def index():
    return render_template("404.html")