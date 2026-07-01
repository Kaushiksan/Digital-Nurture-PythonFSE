# Hands-On 4 – Django REST Framework (DRF)

## Objective

Build REST APIs using Django REST Framework.

## Files

- serializers.py
- views.py
- urls.py
- requirements.txt

## Topics Covered

- Django REST Framework
- ModelSerializer
- Generic API Views
- CRUD APIs
- URL Routing
- JSON Responses

## Install

```bash
pip install djangorestframework
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "rest_framework",
]
```

## Run

```bash
python manage.py runserver
```

## Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /courses/ | List all courses |
| POST | /courses/ | Create a course |
| GET | /courses/1/ | Retrieve course |
| PUT | /courses/1/ | Update course |
| DELETE | /courses/1/ | Delete course |

## Status

Completed
