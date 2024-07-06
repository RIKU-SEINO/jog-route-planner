from flask_app.models import *

class Prefecture(db.Model):
    __tablename__ = "data_models_prefectures"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cities = db.relationship('City', backref='prefecture', lazy=True)
    course = db.relationship('Course', backref="prefecture", lazy=True)

class City(db.Model):
    __tablename__ = "data_models_cities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    prefecture_id = db.Column(db.Integer, db.ForeignKey('data_models_prefectures.id'), nullable=False)
    course = db.relationship('Course', backref="city", lazy=True)