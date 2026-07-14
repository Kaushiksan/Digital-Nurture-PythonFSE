from flask import jsonify, request

from extensions import db
from . import courses_bp
from .models import Course, Student, Enrollment


# ==========================================
# GET ALL COURSES
# ==========================================

@courses_bp.route("/", methods=["GET"])
def get_courses():

    courses = Course.query.all()

    return jsonify([
        course.to_dict()
        for course in courses
    ]), 200


# ==========================================
# CREATE COURSE
# ==========================================

@courses_bp.route("/", methods=["POST"])
def create_course():

    data = request.get_json()

    if data is None:

        return jsonify({
            "error": "Request body must be JSON"
        }), 400

    required_fields = [
        "name",
        "code",
        "credits",
        "department_id"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:

        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    existing_course = Course.query.filter_by(
        code=data["code"]
    ).first()

    if existing_course:

        return jsonify({
            "error": "Course code already exists"
        }), 400

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"],
        department_id=data["department_id"]
    )

    db.session.add(course)

    db.session.commit()

    return jsonify(
        course.to_dict()
    ), 201


# ==========================================
# GET COURSE BY ID
# ==========================================

@courses_bp.route(
    "/<int:course_id>/",
    methods=["GET"]
)
def get_course(course_id):

    course = Course.query.get_or_404(course_id)

    return jsonify(
        course.to_dict()
    ), 200


# ==========================================
# UPDATE COURSE
# ==========================================

@courses_bp.route(
    "/<int:course_id>/",
    methods=["PUT"]
)
def update_course(course_id):

    course = Course.query.get_or_404(course_id)

    data = request.get_json()

    if data is None:

        return jsonify({
            "error": "Request body must be JSON"
        }), 400

    course.name = data.get(
        "name",
        course.name
    )

    course.code = data.get(
        "code",
        course.code
    )

    course.credits = data.get(
        "credits",
        course.credits
    )

    course.department_id = data.get(
        "department_id",
        course.department_id
    )

    db.session.commit()

    return jsonify(
        course.to_dict()
    ), 200


# ==========================================
# DELETE COURSE
# ==========================================

@courses_bp.route(
    "/<int:course_id>/",
    methods=["DELETE"]
)
def delete_course(course_id):

    course = Course.query.get_or_404(course_id)

    db.session.delete(course)

    db.session.commit()

    return "", 204


# ==========================================
# GET STUDENTS ENROLLED IN COURSE
# ==========================================

@courses_bp.route(
    "/<int:course_id>/students/",
    methods=["GET"]
)
def get_course_students(course_id):

    Course.query.get_or_404(course_id)

    students = (
        db.session.query(Student)
        .join(
            Enrollment,
            Student.id == Enrollment.student_id
        )
        .filter(
            Enrollment.course_id == course_id
        )
        .all()
    )

    return jsonify([
        student.to_dict()
        for student in students
    ]), 200
