# Hands-On 6 – FastAPI Path Parameters, Pydantic & Async Endpoints

## Objective

Build an asynchronous Course Management API using FastAPI, Pydantic, and SQLAlchemy.

## Topics Covered

- FastAPI
- Path Parameters
- Query Parameters
- Pydantic Models
- Request Validation
- Response Models
- Async and Await
- SQLAlchemy AsyncSession
- Dependency Injection
- Swagger UI
- OpenAPI Documentation
- Pagination
- Department Filtering

## Project Structure

```text
HandsOn6/
├── main.py
├── schemas.py
├── database.py
├── models.py
├── requirements.txt
└── README.md
```

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run Application

```bash
uvicorn main:app --reload
```

## Root Endpoint

```text
GET /
```

Expected response:

```json
{
    "message": "API running"
}
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | / | Check API status |
| POST | /api/courses/ | Create a course |
| GET | /api/courses/ | List courses |
| GET | /api/courses/{course_id} | Retrieve course by ID |

## Create Course

Endpoint:

```text
POST /api/courses/
```

Sample request:

```json
{
    "name": "Python Programming",
    "code": "CS101",
    "credits": 4,
    "department_id": 1
}
```

FastAPI automatically validates the request body using the `CourseCreate` Pydantic model.

Invalid request data returns HTTP status code `422 Unprocessable Entity`.

## Path Parameters

The following endpoint uses a path parameter:

```text
GET /api/courses/{course_id}
```

Example:

```text
GET /api/courses/1
```

The `course_id` value is automatically validated as an integer by FastAPI.

## Query Parameters

The course list endpoint supports:

- skip
- limit
- department_id

Example:

```text
GET /api/courses/?skip=0&limit=2
```

This returns the first two courses.

Example:

```text
GET /api/courses/?skip=2&limit=2
```

This returns the next two courses.

Filter by department:

```text
GET /api/courses/?department_id=1
```

## Dependency Injection

The database session is injected using FastAPI's `Depends` system.

```python
db: AsyncSession = Depends(get_db)
```

The `get_db()` dependency creates and provides an asynchronous database session.

## Async Database Access

Database operations use SQLAlchemy's asynchronous API.

Example:

```python
result = await db.execute(
    select(Course)
)
```

Database commits are also asynchronous:

```python
await db.commit()
```

## Swagger Documentation

Start the server and open:

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically generates interactive Swagger documentation.

## Expected Outcome

- FastAPI application runs successfully.
- Swagger UI displays the API endpoints.
- Pydantic validates request data.
- Invalid data returns HTTP 422.
- Courses can be created.
- Courses can be retrieved by ID.
- Pagination works using skip and limit.
- Courses can be filtered by department.
- Database operations use async SQLAlchemy.

## Status

Completed
