# ==========================================================
# HANDS-ON 6
# CRUD Operations using SQLAlchemy ORM
# ==========================================================

from datetime import date

from sqlalchemy.orm import sessionmaker

from models import (
    engine,
    Department,
    Student,
    Course,
    Enrollment,
    Professor
)

# ----------------------------------------------------------
# Create Session
# ----------------------------------------------------------

Session = sessionmaker(bind=engine)
session = Session()

# ==========================================================
# INSERT SAMPLE DATA
# ==========================================================

# -------------------------
# Department
# -------------------------

cs = Department(
    dept_name="Computer Science",
    hod_name="Dr. Ramesh Kumar",
    budget=850000
)

ece = Department(
    dept_name="Electronics",
    hod_name="Dr. Priya Nair",
    budget=650000
)

session.add_all([cs, ece])
session.commit()

# -------------------------
# Courses
# -------------------------

course1 = Course(
    course_name="Database Management Systems",
    course_code="CS102",
    credits=4,
    department=cs
)

course2 = Course(
    course_name="Data Structures",
    course_code="CS101",
    credits=4,
    department=cs
)

session.add_all([course1, course2])
session.commit()

# -------------------------
# Professor
# -------------------------

prof = Professor(
    prof_name="Dr. Anand",
    email="anand@college.edu",
    salary=95000,
    department=cs
)

session.add(prof)
session.commit()

# -------------------------
# Student
# -------------------------

student = Student(
    first_name="Arjun",
    last_name="Mehta",
    email="arjun@college.edu",
    date_of_birth=date(2003,4,12),
    enrollment_year=2022,
    department=cs
)

session.add(student)
session.commit()

# -------------------------
# Enrollment
# -------------------------

enroll = Enrollment(
    student=student,
    course=course1,
    enrollment_date=date.today(),
    grade="A"
)

session.add(enroll)
session.commit()

print("\nSample Data Inserted Successfully.")

# ==========================================================
# READ OPERATIONS
# ==========================================================

print("\n========== ALL STUDENTS ==========\n")

students = session.query(Student).all()

for s in students:
    print(
        s.student_id,
        s.first_name,
        s.last_name,
        s.department.dept_name
    )

# ==========================================================
# FILTER QUERY
# ==========================================================

print("\n========== STUDENTS (2022) ==========\n")

students2022 = (
    session.query(Student)
    .filter(Student.enrollment_year == 2022)
    .all()
)

for s in students2022:
    print(s.first_name)

# ==========================================================
# UPDATE
# ==========================================================

student = (
    session.query(Student)
    .filter_by(email="arjun@college.edu")
    .first()
)

if student:

    student.first_name = "Arjun Kumar"

    session.commit()

    print("\nStudent Updated Successfully.")

# ==========================================================
# DELETE
# ==========================================================

course = (
    session.query(Course)
    .filter_by(course_code="CS101")
    .first()
)

if course:

    session.delete(course)

    session.commit()

    print("\nCourse Deleted Successfully.")

# ==========================================================
# VERIFY
# ==========================================================

print("\n========== COURSES ==========\n")

courses = session.query(Course).all()

for c in courses:

    print(
        c.course_code,
        c.course_name
    )

# ==========================================================
# TOTAL COUNTS
# ==========================================================

print("\n========== SUMMARY ==========\n")

print("Departments :",
      session.query(Department).count())

print("Students :",
      session.query(Student).count())

print("Courses :",
      session.query(Course).count())

print("Professors :",
      session.query(Professor).count())

print("Enrollments :",
      session.query(Enrollment).count())

# ==========================================================
# CLOSE SESSION
# ==========================================================

session.close()

print("\nSession Closed.")
