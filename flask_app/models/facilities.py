from flask_app.models import *

class Facility(db.Model):
    __tablename__ = "data_models_facilities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)