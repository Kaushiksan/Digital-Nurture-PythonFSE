"""
Hands-On 2
Django ORM CRUD Operations
"""

from courses.models import Course, Student, Enrollment

# -----------------------------
# CREATE
# -----------------------------

course = Course.objects.create(
    course_name="Python Programming",
    course_code="CS101",
    credits=4
)

student = Student.objects.create(
    first_name="Arjun",
    last_name="Mehta",
    email="arjun@gmail.com",
    enrollment_year=2022
)

Enrollment.objects.create(
    student=student,
    course=course,
    grade="A"
)

print("Records Created Successfully.")

# -----------------------------
# READ
# -----------------------------

print("\nCourses")
for c in Course.objects.all():
    print(c.course_name)

print("\nStudents")
for s in Student.objects.all():
    print(s.first_name, s.last_name)

# -----------------------------
# UPDATE
# -----------------------------

student.first_name = "Arjun Kumar"
student.save()

print("\nStudent Updated Successfully.")

# -----------------------------
# DELETE
# -----------------------------

course.delete()

print("\nCourse Deleted Successfully.")
