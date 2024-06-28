from instance.config import Config
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

    from flask_app.views import index as index_bp
    from flask_app.views import auth as auth_bp
    from flask_app.views import map as map_bp
    from flask_app.views import search as search_bp
    from flask_app.views import user as user_bp
    
    app.register_blueprint(index_bp.index, url_prefix='/')
    app.register_blueprint(auth_bp.auth, url_prefix='/auth')
    app.register_blueprint(auth_bp.auth, url_prefix='/auth')

    return app