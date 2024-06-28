from dotenv import load_dotenv
import secrets
import os

load_dotenv()

class Config:
    DEBUG = os.getenv("FLASK_DEBUG", default=False)
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    WTF_CSRF_SECRET_KEY = secrets.token_hex(16)
    TEMPLATES_AUTO_RELOAD = True