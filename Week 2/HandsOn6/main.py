from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import (
    engine,
    Base,
    get_db
)

from models import (
    Course,
    Department
)

from schemas import (
    CourseCreate,
    CourseResponse
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Course Management API",
    version="1.0"
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
# ROOT ENDPOINT
# ==========================================

@app.get("/")
async def root():

    return {
        "message": "API running"
    }


# ==========================================
# CREATE COURSE
# ==========================================

@app.post(
    "/api/courses/",
    response_model=CourseResponse
)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db)
):

    existing_course = await db.execute(
        select(Course).where(
            Course.code == course.code
        )
    )

    if existing_course.scalar_one_or_none():

        raise HTTPException(
            status_code=400,
            detail="Course code already exists"
        )

    department_result = await db.execute(
        select(Department).where(
            Department.id == course.department_id
        )
    )

    department = (
        department_result.scalar_one_or_none()
    )

    if department is None:

        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

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


# ==========================================
# GET ALL COURSES
# ==========================================

@app.get(
    "/api/courses/",
    response_model=list[CourseResponse]
)
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):

    query = select(Course)

    if department_id is not None:

        query = query.where(
            Course.department_id == department_id
        )

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)

    courses = result.scalars().all()

    return courses


# ==========================================
# GET COURSE BY ID
# ==========================================

@app.get(
    "/api/courses/{course_id}",
    response_model=CourseResponse
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
