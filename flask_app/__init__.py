from flask_app.config import Config
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import secrets

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "views.auth"
login_manager.login_message = ""

def create_app():

    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)
    app.config.from_object(Config)

    @app.errorhandler(400)
    def error_400(error):
        return render_template('400.html')
    
    @app.errorhandler(404)
    def error_404(error):
        return render_template('404.html')

    @app.errorhandler(500)
    def error_500(error):
        return render_template('500.html')
    
    @app.errorhandler(502)
    def error_502(error):
        return render_template('502.html')

    @app.errorhandler(503)
    def error_503(error):
        return render_template('503.html')
    
    

    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)

    from flask_app.views import home as home_bp
    from flask_app.views import auth as auth_bp
    from flask_app.views import map as map_bp
    from flask_app.views import course as course_bp
    from flask_app.views import profile as profile_bp
    
    app.register_blueprint(home_bp.home, url_prefix='/')
    app.register_blueprint(auth_bp.auth, url_prefix='/auth')
    app.register_blueprint(map_bp.route_map, url_prefix='/map')
    app.register_blueprint(course_bp.courses, url_prefix='/courses')
    app.register_blueprint(profile_bp.profile, url_prefix='/user')

    return app