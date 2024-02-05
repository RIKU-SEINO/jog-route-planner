from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    return app