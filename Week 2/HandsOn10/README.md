# Hands-On 10 – Microservices Architecture

## Objective

Decompose the Course Management monolith into independent microservices and implement inter-service communication and an API Gateway.

## Topics Covered

- Monolith vs Microservices
- Service Decomposition
- Bounded Contexts
- Database per Service
- Inter-Service Communication
- Synchronous HTTP Communication
- API Gateway Pattern
- Service Failure Handling
- Message Queues

## Project Structure

```text
HandsOn10/
├── README.md
├── requirements.txt
├── course_service/
│   └── app.py
├── student_service/
│   └── app.py
└── gateway/
    └── app.py
```

## Microservice Decomposition

| Service Name | Responsibility | Endpoints it Owns | Database it Owns |
| --- | --- | --- | --- |
| Course Service | Course and department management | /api/courses/* | courses.db |
| Student Service | Student and enrollment management | /api/students/* | students.db |
| Auth Service | Registration, login and token validation | /api/auth/* | auth.db |
| Notification Service | Email and enrollment confirmations | Internal notification events | notification data |

For this hands-on exercise, Course Service and Student Service are implemented as separate Flask applications.

Auth Service and Notification Service are identified as natural service boundaries but are not separately implemented.

## Microservices Principle

Each microservice owns its own data.

Course Service owns:

```text
courses.db
```

Student Service owns:

```text
students.db
```

Student Service must not directly query the Course Service database.

To verify a course, Student Service communicates with Course Service using an HTTP request.

## Course Service

Course Service runs on:

```text
http://127.0.0.1:5001
```

### Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /api/courses/ | List courses |
| GET | /api/courses/{id}/ | Get course |
| POST | /api/courses/ | Create course |

### Sample Course

```json
{
    "name": "Python Programming",
    "code": "CS101",
    "credits": 4
}
```

## Student Service

Student Service runs on:

```text
http://127.0.0.1:5002
```

### Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /api/students/ | List students |
| POST | /api/students/ | Create student |
| POST | /api/students/{id}/enroll | Enroll student |

### Sample Student

```json
{
    "name": "Arjun Mehta",
    "email": "arjun@college.edu"
}
```

## Inter-Service Communication

The Student Service enrollment endpoint needs to verify that the requested course exists.

Student Service sends an HTTP GET request to Course Service.

```python
course_response = requests.get(
    f"{COURSE_SERVICE_URL}/api/courses/{course_id}/"
)
```

The communication flow is:

```text
Student Service
       |
       | HTTP GET
       v
Course Service
       |
       | Course verification
       v
Student Service
```

Student Service does not directly access `courses.db`.

## Service Failure Handling

If Course Service is unavailable, Student Service catches the connection error.

The API returns:

```text
503 Service Unavailable
```

Example response:

```json
{
    "error": "Course Service is unavailable"
}
```

This demonstrates a disadvantage of synchronous inter-service communication.

## API Gateway

The API Gateway runs on:

```text
http://127.0.0.1:5000
```

Clients communicate with the gateway instead of directly communicating with individual services.

The gateway routes:

```text
/api/courses/*  -> Course Service
/api/students/* -> Student Service
```

Architecture:

```text
                 Client
                    |
                    v
              API Gateway
               Port 5000
               /        \
              /          \
             v            v
     Course Service   Student Service
        Port 5001        Port 5002
             |                |
             v                v
        courses.db       students.db
```

## Running the Application

Open three terminals.

### Terminal 1 – Course Service

```bash
cd course_service
python app.py
```

Course Service runs on port 5001.

### Terminal 2 – Student Service

```bash
cd student_service
python app.py
```

Student Service runs on port 5002.

### Terminal 3 – API Gateway

```bash
cd gateway
python app.py
```

API Gateway runs on port 5000.

## Testing Through API Gateway

### Create Course

Send:

```text
POST /api/courses/
```

Request body:

```json
{
    "name": "Python Programming",
    "code": "CS101",
    "credits": 4
}
```

### Create Student

Send:

```text
POST /api/students/
```

Request body:

```json
{
    "name": "Arjun Mehta",
    "email": "arjun@college.edu"
}
```

### Enroll Student

Send:

```text
POST /api/students/1/enroll
```

Request body:

```json
{
    "course_id": 1
}
```

The complete communication flow is:

```text
Client
  |
  v
API Gateway
  |
  v
Student Service
  |
  | GET /api/courses/1/
  v
Course Service
  |
  v
Student Service
  |
  v
API Gateway
  |
  v
Client
```

## Synchronous vs Asynchronous Communication

### Synchronous HTTP Communication

In synchronous communication, one service directly calls another service and waits for a response.

Advantages:

- Simple to implement
- Immediate response
- Easy to understand
- Suitable when the caller needs the result immediately

Disadvantages:

- Services become tightly coupled
- Service failure affects dependent services
- Network latency increases response time
- Multiple service calls can create cascading failures

The enrollment endpoint uses synchronous HTTP because Student Service must immediately verify whether the course exists.

### Asynchronous Message Queue Communication

In asynchronous communication, a service sends a message to a message broker.

The receiving service processes the message later.

Message queue technologies include:

- RabbitMQ
- Kafka

Advantages:

- Services are loosely coupled
- Better failure isolation
- Improved scalability
- Messages can be processed later
- Suitable for background processing

Disadvantages:

- Increased system complexity
- Eventual consistency
- Harder debugging
- Requires message broker infrastructure

## When to Use RabbitMQ or Kafka

A message queue can be used for:

- Sending enrollment confirmation emails
- Notifications
- Audit logging
- Analytics events
- Background report generation

For example:

```text
Student Service
       |
       | Enrollment Created Event
       v
   Message Queue
       |
       v
Notification Service
       |
       v
Send Confirmation Email
```

Student Service does not need to wait for the email to be sent.

## API Gateway Pattern

An API Gateway provides a single entry point for clients.

A production API Gateway may handle:

- Request routing
- Authentication
- Authorization
- Rate limiting
- SSL termination
- Logging
- Monitoring

The gateway in this exercise demonstrates only request routing and basic service failure handling.

## Expected Outcome

- Course Service runs independently on port 5001.
- Student Service runs independently on port 5002.
- API Gateway runs independently on port 5000.
- Course Service owns its own SQLite database.
- Student Service owns its own SQLite database.
- Services do not share databases.
- Student Service calls Course Service using HTTP.
- Invalid courses return HTTP 404.
- Course Service failure returns HTTP 503.
- Gateway routes course requests to Course Service.
- Gateway routes student requests to Student Service.
- Student enrollment works through the API Gateway.

## Status

Completed
