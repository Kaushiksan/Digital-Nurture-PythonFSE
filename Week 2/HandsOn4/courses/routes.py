from flask import jsonify
from flask import request

from . import courses_bp


courses = []


@courses_bp.route("/", methods=["GET"])
def get_courses():

    return jsonify(courses)


@courses_bp.route("/", methods=["POST"])
def create_course():

    data = request.get_json()

    if not data:

        return jsonify(
            {"message": "Invalid JSON"}
        ), 400

    courses.append(data)

    return jsonify(data), 201
