# ==========================================================
# HANDS-ON 6
# N+1 Problem using SQLAlchemy
# ==========================================================

import time

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload

from models import (
    engine,
    Student
)

# ----------------------------------------------------------
# Create Session
# ----------------------------------------------------------

Session = sessionmaker(bind=engine)
session = Session()

# ==========================================================
# N+1 PROBLEM
# ==========================================================

print("\n========== N+1 QUERY ==========\n")

start = time.time()

students = session.query(Student).all()

for student in students:
    print(
        student.first_name,
        "->",
        student.department.dept_name
    )

end = time.time()

print("\nExecution Time :", end - start)

# ==========================================================
# OPTIMIZED USING joinedload()
# ==========================================================

print("\n========== USING JOINEDLOAD ==========\n")

start = time.time()

students = (
    session.query(Student)
    .options(joinedload(Student.department))
    .all()
)

for student in students:
    print(
        student.first_name,
        "->",
        student.department.dept_name
    )

end = time.time()

print("\nExecution Time :", end - start)

# ==========================================================
# EXPLANATION
# ==========================================================

print("""

N+1 Query Problem

Without joinedload()

1 Query loads Students

For every student,
another query loads Department.

Total Queries

1 + N

Optimized Solution

joinedload()

Only ONE JOIN query executes.

Advantages

✔ Faster
✔ Fewer Database Calls
✔ Better ORM Performance

""")

session.close()

print("\nSession Closed.")
