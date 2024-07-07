from flask_app import db
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, request, flash
from sqlalchemy import or_
from flask_login import login_required, current_user
from flask_app.models.facilities import Facility
from flask_app.models.courses import Course
from flask_app.models.address import Prefecture, City
from flask_app.forms.course_forms import CreateCourseForm, SearchCourseForm, EditCourseForm

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
        
    if current_user.is_authenticated:
        courses = query.filter(or_(Course.is_public == True, Course.user_id == current_user.id)).all()
    else:
        courses = query.filter_by(is_public=True).all()
    return render_template("course_list.html", form=form, courses=courses)

@courses.route("/<course_id>", methods=["GET"])
def course_detail(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course:
        if course.is_public or (current_user.is_authenticated and current_user.id == course.user_id):
            course_dict = course_to_dict(course)
            return render_template("course_detail.html", course_dict=course_dict)
        else:
            return "このコースは非公開です。"
    else:
        return "このコースは存在しません。"

@courses.route("/<course_id>/edit", methods=["GET", "POST"])
def edit(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course:
        if current_user.is_authenticated and current_user.id == course.user_id:
            form = EditCourseForm(obj=course)
            course_dict = course_to_dict(course)
            if request.method == "POST":
                course.title = form.title.data
                course.description = form.description.data
                course.distance = form.distance.data
                course.prefecture_id = form.prefecture.data.id
                course.city_id = form.city.data
                course.facilities = [facility for facility in form.facilities.data]
                course.is_public = form.is_public.data

                db.session.commit()

                if form.is_public.data:
                    flash('コースを公開して保存しました。', 'success')
                else:
                    flash('コースを非公開で保存しました。', 'success')
                return redirect(url_for("courses.course_detail", course_id=course_id))

            return render_template("course_edit.html", form=form, course_dict=course_dict)
        else:
            return "このコースの編集権限がありません"
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
        waypoint_indices = form.waypoint_indices.data
        distance = form.distance.data
        prefecture = form.prefecture.data
        city_id = form.city.data
        facilities = form.facilities.data

        new_course = Course(title=title, 
                            description=description,
                            route=route,
                            waypoint_indices=waypoint_indices,
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

        flash('コースを非公開で保存しました。', 'success')
        new_course_dict = course_to_dict(new_course)

        return render_template("course_detail.html",course_dict=new_course_dict)

    return render_template("course_new.html", form=form)

# courseモデルをdictに変換し、jsでjsonに変換することができるようにする
def course_to_dict(course):
    city = course.city
    if city:
        city_name = city.name
        city_id = city.id
    else:
        city_name = ""
        city_id = ""
    return {
        'id': course.id,
        'title':course.title,
        'description': course.description,
        'distance': course.distance,
        'route': course.route,
        'waypoint_indices': course.waypoint_indices,
        'prefecture_id': course.prefecture.id,
        'prefecture_name': course.prefecture.name,
        'city_id': city_id,
        'city_name': city_name,
        'facilities': [{'id': facility.id, 'name': facility.name} for facility in course.facilities],
        'user_id': course.user_id
    }

    


    