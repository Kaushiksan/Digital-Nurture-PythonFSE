# Hands-On 7 – FastAPI Dependency Injection, CRUD & OpenAPI Documentation

## Objective

Build a complete Course Management API using FastAPI with asynchronous CRUD operations, dependency injection, background tasks, and OpenAPI documentation.

## Topics Covered

- FastAPI Dependency Injection
- Async SQLAlchemy
- CRUD Operations
- Response Models
- HTTP Status Codes
- HTTPException
- Background Tasks
- JOIN Queries
- OpenAPI Documentation
- Swagger UI
- API Tags

## Project Structure

```text
HandsOn7/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Run Application

```bash
uvicorn main:app --reload
```

## Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

The API endpoints are grouped using the following OpenAPI tags:

- Courses
- Students
- Enrollments
- General

## Course Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/courses/ | Create course |
| GET | /api/courses/ | List courses |
| GET | /api/courses/{id} | Get course |
| PUT | /api/courses/{id} | Update course |
| DELETE | /api/courses/{id} | Delete course |
| GET | /api/courses/{id}/students/ | Get enrolled students |

## Student Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/students/ | Create student |
| GET | /api/students/ | List students |
| GET | /api/students/{id} | Get student |
| PUT | /api/students/{id} | Update student |
| DELETE | /api/students/{id} | Delete student |

## Enrollment Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/enrollments/ | Create enrollment |
| GET | /api/enrollments/ | List enrollments |
| GET | /api/enrollments/{id} | Get enrollment |
| PUT | /api/enrollments/{id} | Update enrollment |
| DELETE | /api/enrollments/{id} | Delete enrollment |

## HTTP Status Codes

- 200 OK – Successful GET and PUT
- 201 Created – Resource created successfully
- 204 No Content – Resource deleted successfully
- 404 Not Found – Resource does not exist
- 422 Unprocessable Entity – Request validation failed

## Background Tasks

After creating an enrollment, a confirmation task is added using FastAPI `BackgroundTasks`.

```python
background_tasks.add_task(
    send_confirmation_email,
    student.email
)
```

The API returns the HTTP response before the background task executes.

The server console displays:

```text
Sending confirmation to student@example.com
```

## Dependency Injection

FastAPI's `Depends()` is used to inject the asynchronous database session.

```python
db: AsyncSession = Depends(get_db)
```

## Error Handling

Missing resources raise `HTTPException`.

```python
raise HTTPException(
    status_code=404,
    detail="Course not found"
)
```

FastAPI automatically converts the exception into a JSON error response.

## OpenAPI Customisation

The FastAPI application contains custom metadata:

- Title
- Description
- Version
- Contact information

Endpoints are grouped using tags.

The course creation endpoint also includes a custom summary and response description.

## Expected Outcome

- Full Course CRUD works.
- Full Student CRUD works.
- Full Enrollment CRUD works.
- POST returns HTTP 201.
- DELETE returns HTTP 204.
- Invalid IDs return HTTP 404.
- Course students are retrieved using a JOIN query.
- Enrollment confirmation runs as a background task.
- Swagger UI groups endpoints by tags.
- OpenAPI metadata is customised.

## Status

Completed
