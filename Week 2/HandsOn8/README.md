# Hands-On 8 – RESTful API Design Best Practices

## Objective

Apply RESTful API design best practices to the Course Management API using FastAPI.

## Topics Covered

- RESTful Resource Naming
- HTTP Methods
- HTTP Status Codes
- API Versioning
- PUT vs PATCH
- Location Header
- Pagination
- Search Filtering
- Standard Error Responses

## Project Structure

```text
HandsOn8/
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

## API Versioning

All course endpoints use versioned URLs.

```text
/api/v1/courses/
```

Using API versioning allows future versions of the API to be introduced without immediately breaking existing clients.

## RESTful Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/v1/courses/ | Create a course |
| GET | /api/v1/courses/ | List courses |
| GET | /api/v1/courses/{id} | Retrieve a course |
| PUT | /api/v1/courses/{id} | Replace a course |
| PATCH | /api/v1/courses/{id} | Partially update a course |
| DELETE | /api/v1/courses/{id} | Delete a course |

## POST Request

Example:

```json
{
    "name": "Python Programming",
    "code": "CS101",
    "credits": 4,
    "department_id": 1
}
```

A successful POST request returns:

```text
201 Created
```

The response also contains a `Location` header.

Example:

```text
Location: /api/v1/courses/1
```

## PUT vs PATCH

### PUT

PUT performs a complete replacement of the resource.

All course fields are required.

Example:

```json
{
    "name": "Advanced Python",
    "code": "CS101",
    "credits": 5,
    "department_id": 1
}
```

### PATCH

PATCH performs a partial update.

Only the fields that need to be changed are sent.

Example:

```json
{
    "credits": 5
}
```

## Pagination

The course list endpoint supports `page` and `page_size`.

Example:

```text
GET /api/v1/courses/?page=1&page_size=2
```

The response uses the following pagination format:

```json
{
    "count": 5,
    "next": "/api/v1/courses/?page=2&page_size=2",
    "previous": null,
    "results": []
}
```

## Search

Courses can be searched by course name or course code.

Example:

```text
GET /api/v1/courses/?search=python
```

Search can also be combined with pagination.

```text
GET /api/v1/courses/?page=1&page_size=2&search=python
```

## Standard Error Response

API errors use a consistent JSON structure.

Example:

```json
{
    "error": {
        "status": 404,
        "message": "Course not found",
        "path": "/api/v1/courses/100"
    }
}
```

## HTTP Status Codes

- 200 OK – Successful GET, PUT, and PATCH
- 201 Created – Resource created
- 204 No Content – Resource deleted
- 400 Bad Request – Invalid request
- 404 Not Found – Resource does not exist
- 422 Unprocessable Entity – Validation error

## Expected Outcome

- RESTful plural resource URLs are used.
- API endpoints are versioned using `/api/v1/`.
- POST returns HTTP 201.
- POST returns a Location header.
- PUT performs complete replacement.
- PATCH performs partial updates.
- DELETE returns HTTP 204.
- Pagination supports page and page_size.
- Search filters by course name or code.
- Pagination responses contain count, next, previous, and results.
- API errors use a standard JSON format.

## Status

Completed
