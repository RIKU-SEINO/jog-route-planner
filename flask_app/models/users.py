from flask_app import db, login_manager
from datetime import datetime
from flask_bcrypt import bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "data_models_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hashed = db.Column(db.String, index=True)
    address = db.Column(db.String(50), index=True)
    bio = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    profile_image = db.relationship('ProfileImage', backref='user', uselist=False)
    courses = db.relationship('Course', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError("読み取り不可")

    @password.setter
    def password(self, password):
        self.password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"),self.password_hashed.encode("utf-8"))
    
    def is_duplicated_email(self):
        return User.query.filter_by(email=self.email).first() is not None
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)