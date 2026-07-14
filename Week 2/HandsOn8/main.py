from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Request,
    Response,
    status
)

from fastapi.responses import JSONResponse

from sqlalchemy import (
    select,
    func,
    or_
)

from sqlalchemy.ext.asyncio import AsyncSession

from database import (
    engine,
    Base,
    get_db
)

from models import Course

from schemas import (
    CourseCreate,
    CourseReplace,
    CoursePatch,
    CourseResponse
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Course Management REST API",
    description="RESTful API Design Best Practices",
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
# STANDARD ERROR RESPONSE
# ==========================================

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "status": exc.status_code,
                "message": exc.detail,
                "path": str(request.url.path)
            }
        }
    )


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
async def root():

    return {
        "message": "Course Management REST API"
    }


# ==========================================
# CREATE COURSE
# ==========================================

@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"]
)
async def create_course(
    course: CourseCreate,
    response: Response,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.code == course.code
        )
    )

    existing_course = (
        result.scalar_one_or_none()
    )

    if existing_course:

        raise HTTPException(
            status_code=400,
            detail="Course code already exists"
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

    response.headers["Location"] = (
        f"/api/v1/courses/{new_course.id}"
    )

    return new_course


# ==========================================
# LIST COURSES
# ==========================================

@app.get(
    "/api/v1/courses/",
    tags=["Courses"]
)
async def get_courses(
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    db: AsyncSession = Depends(get_db)
):

    if page < 1:

        raise HTTPException(
            status_code=400,
            detail="Page must be greater than 0"
        )

    if page_size < 1:

        raise HTTPException(
            status_code=400,
            detail="Page size must be greater than 0"
        )

    query = select(Course)

    count_query = select(
        func.count(Course.id)
    )

    if search:

        search_filter = or_(
            Course.name.ilike(
                f"%{search}%"
            ),
            Course.code.ilike(
                f"%{search}%"
            )
        )

        query = query.where(
            search_filter
        )

        count_query = count_query.where(
            search_filter
        )

    count_result = await db.execute(
        count_query
    )

    total_count = count_result.scalar_one()

    offset = (
        page - 1
    ) * page_size

    query = (
        query
        .offset(offset)
        .limit(page_size)
    )

    result = await db.execute(query)

    courses = result.scalars().all()

    course_results = [
        CourseResponse.model_validate(
            course
        ).model_dump()
        for course in courses
    ]

    next_page = None

    if offset + page_size < total_count:

        next_page = (
            f"/api/v1/courses/"
            f"?page={page + 1}"
            f"&page_size={page_size}"
        )

        if search:

            next_page += (
                f"&search={search}"
            )

    previous_page = None

    if page > 1:

        previous_page = (
            f"/api/v1/courses/"
            f"?page={page - 1}"
            f"&page_size={page_size}"
        )

        if search:

            previous_page += (
                f"&search={search}"
            )

    return {
        "count": total_count,
        "next": next_page,
        "previous": previous_page,
        "results": course_results
    }


# ==========================================
# GET COURSE BY ID
# ==========================================

@app.get(
    "/api/v1/courses/{course_id}",
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


# ==========================================
# REPLACE COURSE USING PUT
# ==========================================

@app.put(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def replace_course(
    course_id: int,
    course_data: CourseReplace,
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

    course.name = course_data.name
    course.code = course_data.code
    course.credits = course_data.credits
    course.department_id = (
        course_data.department_id
    )

    await db.commit()

    await db.refresh(course)

    return course


# ==========================================
# PARTIAL UPDATE USING PATCH
# ==========================================

@app.patch(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def patch_course(
    course_id: int,
    course_data: CoursePatch,
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


# ==========================================
# DELETE COURSE
# ==========================================

@app.delete(
    "/api/v1/courses/{course_id}",
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
