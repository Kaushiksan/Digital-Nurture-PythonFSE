# Hands-On 1 – QA Concepts, Functional Testing & Defect Lifecycle

## Name
Kaushik A

---

# Task 1: Map Testing Types to a Real System

## 1. Test Cases for Different Testing Levels

### Unit Testing
**Scenario:** Verify that the `create_course()` function validates required fields before saving a course.

**Test Type:** Functional Testing

---

### Integration Testing
**Scenario:** Verify that the `POST /api/courses/` endpoint successfully stores a new course in the database.

**Test Type:** Functional Testing

---

### System Testing
**Scenario:** Verify the complete flow:
1. Send a POST request.
2. Store course in the database.
3. Retrieve it using GET.
4. Verify the returned data.

**Test Type:** Functional Testing

---

### User Acceptance Testing (UAT)
**Scenario:** A college administrator creates a new course and verifies that students can view and enroll in it.

**Test Type:** Functional Testing

---

## 2. Functional vs Non-Functional Testing

### Functional Testing
Checks whether the application performs the required functions correctly.

**Example**
Verify that the POST `/api/courses/` endpoint successfully creates a course.

### Non-Functional Testing
Checks how well the system performs.

**Example**
Measure API response time under 500 concurrent requests.

---

## 3. Black-Box vs White-Box Testing

| Black-Box Testing | White-Box Testing |
|-------------------|-------------------|
| No knowledge of source code | Knowledge of source code required |
| Focuses on inputs and outputs | Focuses on internal logic |
| Usually performed by QA testers | Usually performed by developers |
| Validates functionality | Validates code quality and coverage |

---

## 4. Formal Test Cases

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|--------------|-------------|---------------|------------|-----------------|---------------|-----------|
| TC001 | Create a new course with valid data | API server running | Send valid POST request | Course created successfully (201 Created) | | |
| TC002 | Create course with missing name | API server running | Send POST request without course name | Validation error (400 Bad Request) | | |
| TC003 | Create duplicate course code | Existing course present | Send POST request using duplicate course code | Duplicate entry error | | |

---

# Task 2: Defect Lifecycle & Severity Classification

## 5. Defect Lifecycle

```
New
 ↓
Assigned
 ↓
Open
 ↓
Fixed
 ↓
Retest
 ↓
Verified
 ↓
Closed
```

### Rejected
Bug is invalid or cannot be reproduced.

### Deferred
Bug is postponed to a future release.

---

## 6. Severity & Priority Classification

### a) POST /api/courses/ returns 500 Internal Server Error

**Severity:** Critical

**Priority:** P1

**Reason:** Core functionality is completely broken.

---

### b) Course names longer than 150 characters are silently truncated

**Severity:** Medium

**Priority:** P2

**Reason:** Data integrity issue but system still functions.

---

### c) Swagger documentation contains a typo

**Severity:** Low

**Priority:** P4

**Reason:** Cosmetic issue with no functional impact.

---

### d) Login occasionally returns 401 for valid users

**Severity:** High

**Priority:** P1

**Reason:** Intermittent authentication failures affect usability.

---

## 7. Defect Report

**Defect ID:** BUG-001

**Title:** POST /api/courses/ returns HTTP 500 Internal Server Error

**Environment:** Windows 11, Chrome Latest

**Build Version:** v1.0.0

**Severity:** Critical

**Priority:** P1

### Steps to Reproduce

1. Open Swagger UI.
2. Navigate to POST `/api/courses/`.
3. Enter valid course details.
4. Click Execute.

### Expected Result

Course should be created successfully with HTTP 201.

### Actual Result

HTTP 500 Internal Server Error is returned.

### Attachments

Screenshot of 500 Internal Server Error.

---

## 8. Severity vs Priority

### Severity
Measures the impact of the defect on the application.

### Priority
Measures how urgently the defect should be fixed.

### Example

A typo on the CEO's dashboard:

- Severity: Low
- Priority: High

Reason:
Although functionality is unaffected, the issue is highly visible and should be corrected immediately.

---

# Conclusion

This hands-on covered:

- QA testing levels
- Functional and Non-Functional testing
- Black-Box vs White-Box testing
- Formal test case writing
- Defect lifecycle
- Severity and Priority
- Professional defect reporting

**Status:** Completed
