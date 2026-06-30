-- ==========================================================
-- HANDS-ON 4
-- Query Optimisation - Indexes, EXPLAIN & Query Plans
-- ==========================================================

USE college_db;

-- ==========================================================
-- TASK 1 : BASELINE PERFORMANCE (NO INDEXES)
-- ==========================================================

-- Query to analyze

EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- ==========================================================
-- COMMENTS
-- ==========================================================

/*
Baseline Observation

- EXPLAIN displays how MySQL executes the query.
- Before adding indexes, MySQL may perform a Full Table Scan.
- Rows examined and access type can be observed.
- Large tables become slower without indexes.
*/

-- ==========================================================
-- TASK 2 : CREATE INDEXES
-- ==========================================================

-------------------------------------------------------------
-- B-Tree Index
-------------------------------------------------------------

CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);

-------------------------------------------------------------
-- Composite UNIQUE Index
-------------------------------------------------------------

CREATE UNIQUE INDEX idx_enrollment_student_course
ON enrollments(student_id, course_id);

-------------------------------------------------------------
-- Course Code Index
-------------------------------------------------------------

CREATE INDEX idx_course_code
ON courses(course_code);

-------------------------------------------------------------
-- MySQL Alternative for Partial Index
-------------------------------------------------------------

/*
The handbook requests a Partial Index:

CREATE INDEX ...
WHERE grade IS NULL

This feature is supported in PostgreSQL.

MySQL does NOT support Partial Indexes.

Hence this step is documented as required.
*/

CREATE INDEX idx_grade_student
ON enrollments(grade, student_id);

-- ==========================================================
-- TASK 3 : VERIFY IMPROVEMENT
-- ==========================================================

EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- ==========================================================
-- COMMENTS
-- ==========================================================

/*

Comparison

Before Indexes

Possible Full Table Scan
Higher rows examined

After Indexes

Possible Index Scan
Reduced rows examined
Better performance

Composite UNIQUE index also prevents duplicate
(student_id, course_id) enrollments.

*/

-- ==========================================================
-- VERIFY INDEXES
-- ==========================================================

SHOW INDEX FROM students;

SHOW INDEX FROM courses;

SHOW INDEX FROM enrollments;

-- ==========================================================
-- VERIFY DUPLICATE PREVENTION
-- ==========================================================

/*

The following statement should fail because of the
UNIQUE Composite Index.

INSERT INTO enrollments
(student_id,course_id,enrollment_date,grade)

VALUES
(1,1,'2024-01-01','A');

*/

-- ==========================================================
-- EXTRA PERFORMANCE TEST
-- ==========================================================

EXPLAIN
SELECT *
FROM students
WHERE enrollment_year = 2022;

EXPLAIN
SELECT *
FROM courses
WHERE course_code='CS101';

EXPLAIN
SELECT *
FROM enrollments
WHERE student_id=1
AND course_id=1;

# ==========================================================
# HANDS-ON 4
# N+1 Query Problem Demonstration
# ==========================================================

import sqlite3
import time

# ----------------------------------------------------------
# Create Connection
# ----------------------------------------------------------

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

# ----------------------------------------------------------
# Create Tables
# ----------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    dept_name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    first_name TEXT,
    department_id INTEGER
)
""")

# ----------------------------------------------------------
# Insert Sample Data
# ----------------------------------------------------------

cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM departments")

departments = [
    (1, "Computer Science"),
    (2, "Electronics"),
    (3, "Mechanical")
]

students = [
    (1, "Arjun", 1),
    (2, "Priya", 1),
    (3, "Rohan", 2),
    (4, "Sneha", 3),
    (5, "Rahul", 1)
]

cursor.executemany(
    "INSERT INTO departments VALUES (?,?)",
    departments
)

cursor.executemany(
    "INSERT INTO students VALUES (?,?,?)",
    students
)

conn.commit()

# ==========================================================
# N+1 QUERY PROBLEM
# ==========================================================

print("\n========== N+1 QUERY ==========\n")

start = time.time()

cursor.execute("SELECT student_id, first_name, department_id FROM students")

students = cursor.fetchall()

for student in students:

    cursor.execute(
        "SELECT dept_name FROM departments WHERE department_id=?",
        (student[2],)
    )

    dept = cursor.fetchone()

    print(
        f"{student[1]} --> {dept[0]}"
    )

end = time.time()

print("\nExecution Time :", end - start)

# ==========================================================
# OPTIMIZED QUERY
# ==========================================================

print("\n========== OPTIMIZED JOIN ==========\n")

start = time.time()

cursor.execute("""

SELECT
students.first_name,
departments.dept_name

FROM students

JOIN departments

ON students.department_id=departments.department_id

""")

rows = cursor.fetchall()

for row in rows:
    print(row[0], "-->", row[1])

end = time.time()

print("\nExecution Time :", end - start)

# ==========================================================
# Explanation
# ==========================================================

print("""

Explanation

N+1 Problem

1 Query retrieves all students.

Then one additional query runs
for every student.

Total Queries

1 + N

This becomes slow when N is large.

Optimized Solution

Use JOIN.

Only ONE query retrieves
students and departments.

Advantages

✔ Faster
✔ Less Database Calls
✔ Better Performance

""")

conn.close()

-- ==========================================================
-- SUMMARY
-- ==========================================================

/*

Topics Covered

1. EXPLAIN
2. Query Plan
3. Full Table Scan
4. B-Tree Index
5. Composite Index
6. UNIQUE Index
7. Query Optimization
8. Index Verification

Expected Outcome

✔ EXPLAIN executed
✔ Indexes created
✔ Query plan compared
✔ Duplicate enrollments prevented
✔ Performance improved

*/

-- ==========================================================
-- END OF HANDS-ON 4 (SQL PART)
-- ==========================================================
