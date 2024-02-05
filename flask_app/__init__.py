from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    from flask_app.route_map import views as map_views
    
    app.register_blueprint(map_views.route_map, url_prefix='/map')

    return app