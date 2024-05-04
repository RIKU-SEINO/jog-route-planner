from flask_app.config import Config
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import secrets

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = ""

def create_app():

    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)

    from flask_app.welcome import views as welcome_views
    from flask_app.route_map import views as map_views
    from flask_app.route_search import views as route_search_views
    from flask_app.auth import views as auth_views
    from flask_app.home import views as home_views
    from flask_app.profile import views as profile_views
    from flask_app.error import views as error_views
    
    app.register_blueprint(welcome_views.welcome, url_prefix='/')
    app.register_blueprint(map_views.route_map, url_prefix='/map')
    app.register_blueprint(route_search_views.route_search, url_prefix='/courses')
    app.register_blueprint(auth_views.auth, url_prefix='/auth')
    app.register_blueprint(home_views.home, url_prefix='/home')
    app.register_blueprint(profile_views.profile, url_prefix='/profile')
    app.register_blueprint(error_views.error, url_prefix='/error')

    @app.errorhandler(404)
    def page_not_found(error):
        return redirect(url_for('error.index'), code=302)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
