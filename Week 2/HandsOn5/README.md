# Hands-On 5 – Flask with SQLAlchemy ORM & Database Integration

## Objective

Integrate Flask-SQLAlchemy with the Course Management API and perform database operations using the SQLAlchemy ORM.

## Topics Covered

- Flask-SQLAlchemy
- SQLAlchemy ORM
- Database Models
- Model Relationships
- Flask-Migrate
- Database Migrations
- ORM CRUD Operations
- JSON Serialization
- JOIN Queries

## Project Structure

```text
HandsOn5/
├── app.py
├── commands.txt
├── config.py
├── extensions.py
├── requirements.txt
├── README.md
└── courses/
    ├── __init__.py
    ├── models.py
    └── routes.py
```

## Models

The application contains the following SQLAlchemy models:

### Department

Stores department information.

Fields:

- id
- name
- head_of_dept
- budget

### Course

Stores course information.

Fields:

- id
- name
- code
- credits
- department_id

### Student

Stores student information.

Fields:

- id
- first_name
- last_name
- email
- department_id
- enrollment_year

### Enrollment

Stores student course enrollment information.

Fields:

- id
- student_id
- course_id
- enrollment_date
- grade

A unique constraint prevents the same student from enrolling in the same course more than once.

## Relationships

- A Department can have many Courses.
- A Department can have many Students.
- A Course can have many Enrollments.
- A Student can have many Enrollments.
- Enrollment connects Students and Courses.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Database Migration

Initialize Flask-Migrate:

```bash
flask --app app.py db init
```

Create the initial migration:

```bash
flask --app app.py db migrate -m "initial schema"
```

Apply the migration:

```bash
flask --app app.py db upgrade
```

## Run Application

```bash
flask --app app.py run
```

The application runs at:

`http://127.0.0.1:5000`

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /api/courses/ | List all courses |
| POST | /api/courses/ | Create a course |
| GET | /api/courses/{id}/ | Retrieve a course |
| PUT | /api/courses/{id}/ | Update a course |
| DELETE | /api/courses/{id}/ | Delete a course |
| GET | /api/courses/{id}/students/ | List students enrolled in a course |

## Sample Course JSON

```json
{
    "name": "Database Management Systems",
    "code": "CS102",
    "credits": 4,
    "department_id": 1
}
```

## ORM Operations

SQLAlchemy ORM is used to perform database operations.

Example:

```python
courses = Course.query.all()
```

Create and save a course:

```python
course = Course(
    name="Python Programming",
    code="CS101",
    credits=4,
    department_id=1
)

db.session.add(course)
db.session.commit()
```

## JSON Serialization

Each model contains a `to_dict()` method.

Example:

```python
def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "code": self.code,
        "credits": self.credits
    }
```

The method converts SQLAlchemy model objects into dictionaries that can be returned as JSON responses.

## Expected Outcome

- Flask-SQLAlchemy configured successfully.
- Database models created.
- Model relationships implemented.
- Flask-Migrate configured.
- Database migrations applied.
- CRUD endpoints use database queries.
- Course data is stored in the database.
- Students enrolled in a course are retrieved using a JOIN query.

## Status

Completed
