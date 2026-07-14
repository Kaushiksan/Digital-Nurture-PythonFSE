# Hands-On 9 – Authentication & Security

## Objective

Implement secure authentication for the Course Management API using bcrypt password hashing and JWT access tokens.

## Topics Covered

- Password Hashing
- bcrypt
- JWT Authentication
- OAuth2 Bearer Tokens
- Protected API Routes
- CORS
- HTTP 401 Unauthorized
- HTTP 409 Conflict
- OWASP Security Awareness

## Project Structure

```text
HandsOn9/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── requirements.txt
└── README.md
```

## Installation

Install the required dependencies:

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

## User Registration

Endpoint:

```text
POST /api/v1/auth/register/
```

Sample request:

```json
{
    "email": "student@college.edu",
    "password": "Student@123"
}
```

The password is hashed using bcrypt before it is stored in the database.

Plain-text passwords are never stored.

Registering the same email twice returns:

```text
409 Conflict
```

## User Login

Endpoint:

```text
POST /api/v1/auth/login/
```

Sample request:

```json
{
    "email": "student@college.edu",
    "password": "Student@123"
}
```

Successful login returns:

```json
{
    "access_token": "jwt-token",
    "token_type": "bearer"
}
```

The JWT access token expires after 30 minutes.

## Public Endpoint

The following endpoint can be accessed without authentication:

```text
GET /api/v1/courses/
```

## Protected Endpoints

The following endpoints require a valid Bearer token:

```text
POST /api/v1/courses/
DELETE /api/v1/courses/{course_id}/
```

Without a valid token, the API returns:

```text
401 Unauthorized
```

## JWT Authentication

The JWT token stores the user's email in the `sub` claim.

Example:

```python
{
    "sub": user.email
}
```

JWT payloads are encoded and not encrypted.

Sensitive data such as passwords must never be stored in a JWT payload.

## Password Security

bcrypt is used for password hashing.

bcrypt is intentionally slow and uses a work factor. This makes brute-force password attacks computationally expensive.

MD5 and SHA-256 are designed to be fast and should not be directly used for password storage.

## CORS Configuration

The API allows browser requests from:

```text
http://localhost:3000
```

CORS is configured using FastAPI `CORSMiddleware`.

CORS is enforced by the browser. It is not a replacement for authentication or authorization.

## OAuth2 Authorization Code Flow

In the OAuth2 Authorization Code flow, the user is redirected to an authorization server.

After successful authorization, the client receives an authorization code.

The client exchanges the authorization code for an access token.

The JWT login in this project is simpler. The user sends an email and password directly to the API, and the API generates a JWT access token.

## Expected Outcome

- User registration works.
- Passwords are stored as bcrypt hashes.
- Plain-text passwords are never stored.
- Duplicate registration returns HTTP 409.
- Login returns a JWT access token.
- JWT token expires after 30 minutes.
- Invalid or expired tokens return HTTP 401.
- GET courses works without authentication.
- POST course requires authentication.
- DELETE course requires authentication.
- CORS allows localhost:3000.
- OAuth2 Authorization Code flow is documented.

## Status

Completed
