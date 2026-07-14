from flask import (
    Flask,
    jsonify,
    request
)

from flask_sqlalchemy import SQLAlchemy

import requests


# ==========================================
# STUDENT SERVICE
# ==========================================

app = Flask(__name__)


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///students.db"

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False


db = SQLAlchemy(app)


COURSE_SERVICE_URL = (
    "http://127.0.0.1:5001"
)


# ==========================================
# STUDENT MODEL
# ==========================================

class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )


    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


# ==========================================
# ENROLLMENT MODEL
# ==========================================

class Enrollment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        nullable=False
    )


    def to_dict(self):

        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id
        }


# ==========================================
# CREATE DATABASE
# ==========================================

with app.app_context():

    db.create_all()


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.route(
    "/",
    methods=["GET"]
)
def root():

    return jsonify({
        "service": "Student Service",
        "port": 5002
    })


# ==========================================
# GET ALL STUDENTS
# ==========================================

@app.route(
    "/api/students/",
    methods=["GET"]
)
def get_students():

    students = Student.query.all()

    return jsonify([
        student.to_dict()
        for student in students
    ]), 200


# ==========================================
# CREATE STUDENT
# ==========================================

@app.route(
    "/api/students/",
    methods=["POST"]
)
def create_student():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "JSON body is required"
        }), 400

    student = Student(
        name=data["name"],
        email=data["email"]
    )

    db.session.add(student)

    db.session.commit()

    return jsonify(
        student.to_dict()
    ), 201


# ==========================================
# ENROLL STUDENT
# ==========================================

@app.route(
    "/api/students/<int:student_id>/enroll",
    methods=["POST"]
)
def enroll_student(student_id):

    student = db.session.get(
        Student,
        student_id
    )

    if student is None:

        return jsonify({
            "error": "Student not found"
        }), 404

    data = request.get_json()

    if not data or "course_id" not in data:

        return jsonify({
            "error": "course_id is required"
        }), 400

    course_id = data["course_id"]

    try:

        course_response = requests.get(
            f"{COURSE_SERVICE_URL}"
            f"/api/courses/{course_id}/",
            timeout=5
        )

    except requests.exceptions.ConnectionError:

        return jsonify({
            "error": (
                "Course Service is unavailable"
            )
        }), 503

    except requests.exceptions.Timeout:

        return jsonify({
            "error": (
                "Course Service request timed out"
            )
        }), 503

    if course_response.status_code == 404:

        return jsonify({
            "error": "Course not found"
        }), 404

    if course_response.status_code != 200:

        return jsonify({
            "error": (
                "Unable to verify course"
            )
        }), 503

    existing_enrollment = (
        Enrollment.query.filter_by(
            student_id=student_id,
            course_id=course_id
        ).first()
    )

    if existing_enrollment:

        return jsonify({
            "error": (
                "Student already enrolled"
            )
        }), 409

    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id
    )

    db.session.add(enrollment)

    db.session.commit()

    return jsonify({
        "message": (
            "Student enrolled successfully"
        ),
        "student": student.to_dict(),
        "course": course_response.json(),
        "enrollment": enrollment.to_dict()
    }), 201


# ==========================================
# RUN STUDENT SERVICE
# ==========================================

if __name__ == "__main__":

    app.run(
        port=5002,
        debug=True
    )
