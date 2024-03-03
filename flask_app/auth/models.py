from flask_app.app import db
from datetime import datetime
from flask_bcrypt import bcrypt

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hashed = db.Column(db.String, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


@property
def password(self):
    raise AttributeError("読み取り不可")

@password.setter
def password(self, password):
    self.password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(self, password):
    return bcrypt.checkpw(password.encode("utf-8"),self.password_hashed.encode("utf-8"))