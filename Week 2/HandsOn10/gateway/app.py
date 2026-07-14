from flask import (
    Flask,
    request,
    Response,
    jsonify
)

import requests


# ==========================================
# API GATEWAY
# ==========================================

app = Flask(__name__)


COURSE_SERVICE_URL = (
    "http://127.0.0.1:5001"
)

STUDENT_SERVICE_URL = (
    "http://127.0.0.1:5002"
)


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.route(
    "/",
    methods=["GET"]
)
def root():

    return jsonify({
        "service": "API Gateway",
        "port": 5000
    })


# ==========================================
# FORWARD REQUEST
# ==========================================

def forward_request(
    service_url,
    path
):

    target_url = (
        f"{service_url}/{path}"
    )

    try:

        service_response = requests.request(
            method=request.method,
            url=target_url,
            params=request.args,
            json=request.get_json(
                silent=True
            ),
            headers={
                key: value
                for key, value
                in request.headers
                if key.lower()
                not in [
                    "host",
                    "content-length"
                ]
            },
            timeout=5
        )

    except requests.exceptions.ConnectionError:

        return jsonify({
            "error": (
                "Requested service is unavailable"
            )
        }), 503

    except requests.exceptions.Timeout:

        return jsonify({
            "error": (
                "Requested service timed out"
            )
        }), 503

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection"
    ]

    response_headers = [
        (name, value)
        for name, value
        in service_response.headers.items()
        if name.lower()
        not in excluded_headers
    ]

    return Response(
        service_response.content,
        status=service_response.status_code,
        headers=response_headers
    )


# ==========================================
# COURSE SERVICE ROUTING
# ==========================================

@app.route(
    "/api/courses/",
    defaults={
        "path": "api/courses/"
    },
    methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]
)
@app.route(
    "/api/courses/<path:subpath>",
    methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]
)
def course_gateway(
    subpath=None,
    path=None
):

    if path is None:

        path = (
            f"api/courses/{subpath}"
        )

    return forward_request(
        COURSE_SERVICE_URL,
        path
    )


# ==========================================
# STUDENT SERVICE ROUTING
# ==========================================

@app.route(
    "/api/students/",
    defaults={
        "path": "api/students/"
    },
    methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]
)
@app.route(
    "/api/students/<path:subpath>",
    methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
    ]
)
def student_gateway(
    subpath=None,
    path=None
):

    if path is None:

        path = (
            f"api/students/{subpath}"
        )

    return forward_request(
        STUDENT_SERVICE_URL,
        path
    )


# ==========================================
# RUN API GATEWAY
# ==========================================

if __name__ == "__main__":

    app.run(
        port=5000,
        debug=True
    )
