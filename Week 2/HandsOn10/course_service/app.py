from flask import (
    Flask,
    jsonify,
    request
)

from flask_sqlalchemy import SQLAlchemy


# ==========================================
# COURSE SERVICE
# ==========================================

app = Flask(__name__)


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///courses.db"

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False


db = SQLAlchemy(app)


# ==========================================
# COURSE MODEL
# ==========================================

class Course(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    credits = db.Column(
        db.Integer,
        nullable=False
    )


    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "credits": self.credits
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
        "service": "Course Service",
        "port": 5001
    })


# ==========================================
# GET ALL COURSES
# ==========================================

@app.route(
    "/api/courses/",
    methods=["GET"]
)
def get_courses():

    courses = Course.query.all()

    return jsonify([
        course.to_dict()
        for course in courses
    ]), 200


# ==========================================
# GET COURSE BY ID
# ==========================================

@app.route(
    "/api/courses/<int:course_id>/",
    methods=["GET"]
)
def get_course(course_id):

    course = db.session.get(
        Course,
        course_id
    )

    if course is None:

        return jsonify({
            "error": "Course not found"
        }), 404

    return jsonify(
        course.to_dict()
    ), 200


# ==========================================
# CREATE COURSE
# ==========================================

@app.route(
    "/api/courses/",
    methods=["POST"]
)
def create_course():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "JSON body is required"
        }), 400

    required_fields = [
        "name",
        "code",
        "credits"
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
        }), 409

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"]
    )

    db.session.add(course)

    db.session.commit()

    return jsonify(
        course.to_dict()
    ), 201


# ==========================================
# RUN COURSE SERVICE
# ==========================================

if __name__ == "__main__":

    app.run(
        port=5001,
        debug=True
    )
