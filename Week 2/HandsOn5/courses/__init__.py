from flask import Blueprint


courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)


from . import routes
