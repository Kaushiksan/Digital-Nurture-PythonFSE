from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    BackgroundTasks
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import (
    engine,
    Base,
    get_db
)

from models import (
    Course,
    Student,
    Enrollment
)

from schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Course Management API",
    description="FastAPI Course Management System",
    version="1.0",
    contact={
        "name": "Course Management Team",
        "email": "admin@college.edu"
    }
)


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

@app.on_event("startup")
async def create_tables():

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )


# ==========================================
# BACKGROUND TASK
# ==========================================

def send_confirmation_email(student_email: str):

    print(
        f"Sending confirmation to {student_email}"
    )


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get(
    "/",
    tags=["General"]
)
async def root():

    return {
        "message": "Course Management API running"
    }


# ==========================================
# COURSE CRUD
# ==========================================


# CREATE COURSE

@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
    response_description="Course created successfully"
)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db)
):

    new_course = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id
    )

    db.add(new_course)

    await db.commit()

    await db.refresh(new_course)

    return new_course


# GET ALL COURSES

@app.get(
    "/api/courses/",
    response_model=list[CourseResponse],
    tags=["Courses"]
)
async def get_courses(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course)
    )

    return result.scalars().all()


# GET COURSE BY ID

@app.get(
    "/api/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if course is None:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


# UPDATE COURSE

@app.put(
    "/api/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if course is None:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    update_data = course_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(
            course,
            field,
            value
        )

    await db.commit()

    await db.refresh(course)

    return course


# DELETE COURSE

@app.delete(
    "/api/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"]
)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if course is None:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    await db.delete(course)

    await db.commit()

    return None


# GET STUDENTS ENROLLED IN COURSE

@app.get(
    "/api/courses/{course_id}/students/",
    response_model=list[StudentResponse],
    tags=["Courses"]
)
async def get_course_students(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    course_result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = course_result.scalar_one_or_none()

    if course is None:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    result = await db.execute(
        select(Student)
        .join(
            Enrollment,
            Student.id == Enrollment.student_id
        )
        .where(
            Enrollment.course_id == course_id
        )
    )

    return result.scalars().all()


# ==========================================
# STUDENT CRUD
# ==========================================


# CREATE STUDENT

@app.post(
    "/api/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"]
)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):

    new_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        department_id=student.department_id,
        enrollment_year=student.enrollment_year
    )

    db.add(new_student)

    await db.commit()

    await db.refresh(new_student)

    return new_student


# GET ALL STUDENTS

@app.get(
    "/api/students/",
    response_model=list[StudentResponse],
    tags=["Students"]
)
async def get_students(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student)
    )

    return result.scalars().all()


# GET STUDENT BY ID

@app.get(
    "/api/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"]
)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(
            Student.id == student_id
        )
    )

    student = result.scalar_one_or_none()

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# UPDATE STUDENT

@app.put(
    "/api/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"]
)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(
            Student.id == student_id
        )
    )

    student = result.scalar_one_or_none()

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(
            student,
            field,
            value
        )

    await db.commit()

    await db.refresh(student)

    return student


# DELETE STUDENT

@app.delete(
    "/api/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"]
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(
            Student.id == student_id
        )
    )

    student = result.scalar_one_or_none()

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    await db.delete(student)

    await db.commit()

    return None


# ==========================================
# ENROLLMENT CRUD
# ==========================================


# CREATE ENROLLMENT

@app.post(
    "/api/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"]
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):

    student_result = await db.execute(
        select(Student).where(
            Student.id == enrollment.student_id
        )
    )

    student = student_result.scalar_one_or_none()

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    course_result = await db.execute(
        select(Course).where(
            Course.id == enrollment.course_id
        )
    )

    course = course_result.scalar_one_or_none()

    if course is None:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrollment_date=enrollment.enrollment_date,
        grade=enrollment.grade
    )

    db.add(new_enrollment)

    await db.commit()

    await db.refresh(new_enrollment)

    background_tasks.add_task(
        send_confirmation_email,
        student.email
    )

    return new_enrollment


# GET ALL ENROLLMENTS

@app.get(
    "/api/enrollments/",
    response_model=list[EnrollmentResponse],
    tags=["Enrollments"]
)
async def get_enrollments(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment)
    )

    return result.scalars().all()


# GET ENROLLMENT BY ID

@app.get(
    "/api/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    tags=["Enrollments"]
)
async def get_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:

        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return enrollment


# UPDATE ENROLLMENT

@app.put(
    "/api/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    tags=["Enrollments"]
)
async def update_enrollment(
    enrollment_id: int,
    enrollment_data: EnrollmentUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:

        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    update_data = enrollment_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(
            enrollment,
            field,
            value
        )

    await db.commit()

    await db.refresh(enrollment)

    return enrollment


# DELETE ENROLLMENT

@app.delete(
    "/api/enrollments/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"]
)
async def delete_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:

        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    await db.delete(enrollment)

    await db.commit()

    return None
