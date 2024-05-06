from flask_app.app import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = "data_models_courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    distance = db.Column(db.Float(8,2), nullable=False)
    start_point_name = db.Column(db.String(50), nullable=False)
    end_point_name = db.Column(db.String(50), nullable=False)
    route_data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('data_models_users.id'), nullable=False)
    prefecture_id = db.Column(db.Integer, db.ForeignKey('data_models_prefectures.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    course_images = db.relationship('CourseImage', backref='course', uselist=False)

class CourseImage(db.Model):
    __tablename__ = "data_models_course_images"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('data_models_courses.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class CourseBookmark(db.Model):
    __tablename__ = "data_models_course_bookmarks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('data_models_users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('data_models_courses.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Prefectures(db.Model):
    __tablename__ = "data_models_prefectures"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    courses = db.relationship('Course', backref='prefecture', lazy=True)

class CourseTag(db.Model):
    __tablename__ = "data_models_courses_tags"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('data_models_courses.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('data_models_tags.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Tag(db.Model):
    __tablename__ = "data_models_tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)