from flask_app import db
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, request
from flask_login import login_required, current_user
from flask_app.models.facilities import Facility
from flask_app.models.courses import Course
from flask_app.models.address import Prefecture, City
from flask_app.forms.course_forms import CreateCourseForm, SearchCourseForm

courses = Blueprint(
    'courses',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/courses'
)

@courses.route('/get_cities', methods=['POST'])
def get_cities():
    prefecture_id = request.json.get('prefecture_id')

    if prefecture_id is None:
        return jsonify({'error': 'No prefecture_id provided'}), 400

    # prefecture_idに一致する市区町村をデータベースからクエリします
    cities = City.query.filter_by(prefecture_id=prefecture_id).all()
    
    # 市区町村のリストをJSON形式で返します
    city_list = [{'id': city.id, 'name': city.name} for city in cities]
    return jsonify(city_list)

@courses.route("/", methods=["GET","POST"])
def course_list():
    form = SearchCourseForm()
    query = Course.query
    if request.method == "POST":
        freeword = form.freeword.data
        prefecture = form.prefecture.data
        distance_min = form.distance_min.data
        distance_max = form.distance_max.data
        facilities = form.facilities.data

        if freeword:
            query = query.filter((Course.title.ilike(f'%{freeword}%')) | (Course.description.ilike(f'%{freeword}%')))
        if prefecture:
            query = query.filter_by(prefecture_id=prefecture.id)

        if distance_min:
            query = query.filter(Course.distance >= float(distance_min))
        
        if distance_max:
            query = query.filter(Course.distance <= float(distance_max))
        
        if facilities:
            facility_ids = [facility.id for facility in facilities]
            for facility_id in facility_ids:
                query = query.filter(Course.facilities.any(Facility.id == facility_id))

        courses = query.filter_by(is_public=True).all()
        
        return render_template("course_list.html", form=form, courses=courses)

    courses = query.filter_by(is_public=True).all()
    return render_template("course_list.html", form=form, courses=courses)

@courses.route("/<course_id>", methods=["GET"])
def course_detail(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course:
        if course.is_public or (current_user.is_authenticated and current_user.id == course.user_id):
            return render_template("course_detail.html", course=course)
        else:
            return "このコースは非公開です"
    else:
        return "このコースは存在しません。"


@courses.route("/new", methods=["GET", "POST"])
def new():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    form = CreateCourseForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        route = form.route_latlng.data
        distance = form.distance.data
        prefecture = form.prefecture.data
        city_id = form.city.data
        facilities = form.facilities.data

        new_course = Course(title=title, 
                            description=description,
                            route=route,
                            distance=distance,
                            prefecture_id=prefecture.id,
                            city_id=city_id,
                            user_id=current_user.id,
                            facilities=[]
                        )
        
        # タグづけされた施設を関連付ける
        for facility in facilities:
            new_course.facilities.append(facility)

        db.session.add(new_course)
        db.session.commit()

        return render_template("course_detail.html",course=new_course)

    return render_template("course_new.html", form=form)

    


    