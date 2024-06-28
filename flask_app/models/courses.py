from flask_app.models import *

course_facility = db.Table('course_facility',
    db.Column('course_id', db.Integer, db.ForeignKey('data_models_courses.id'), primary_key=True),
    db.Column('facility_id', db.Integer, db.ForeignKey('data_models_facilities.id'), primary_key=True)
)

class Course(db.Model):
    __tablename__ = "data_models_courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True, nullable=False)
    description = db.Column(db.String(200), index=True)
    route = db.Column(db.String, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    prefecture_id = db.Column(db.Integer, db.ForeignKey('data_models_prefectures.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('data_models_cities.id'), nullable=True)
    facilities = db.relationship('Facility', secondary=course_facility, lazy='subquery',
                                 backref=db.backref('courses', lazy=True))
