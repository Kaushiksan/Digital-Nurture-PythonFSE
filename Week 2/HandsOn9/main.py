from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer

from jose import (
    JWTError,
    jwt
)

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from database import (
    engine,
    Base,
    get_db
)

from models import (
    User,
    Course
)

from schemas import (
    UserRegister,
    UserResponse,
    LoginRequest,
    TokenResponse,
    CourseCreate,
    CourseResponse
)

from security import (
    SECRET_KEY,
    ALGORITHM,
    get_password_hash,
    verify_password,
    create_access_token
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Course Management Security API",
    description="JWT Authentication and API Security",
    version="1.0"
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==========================================
# OAUTH2 TOKEN SCHEME
# ==========================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/"
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
# GET CURRENT USER
# ==========================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:

            raise credentials_exception

    except JWTError:

        raise credentials_exception

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar_one_or_none()

    if user is None:

        raise credentials_exception

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )

    return user


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get(
    "/",
    tags=["General"]
)
async def root():

    return {
        "message": "Security API running"
    }


# ==========================================
# USER REGISTRATION
# ==========================================

@app.post(
    "/api/v1/auth/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"]
)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(
            User.email == user_data.email
        )
    )

    existing_user = (
        result.scalar_one_or_none()
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(
        user_data.password
    )

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(new_user)

    await db.commit()

    await db.refresh(new_user)

    return new_user


# ==========================================
# USER LOGIN
# ==========================================

@app.post(
    "/api/v1/auth/login/",
    response_model=TokenResponse,
    tags=["Authentication"]
)
async def login_user(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(
            User.email == login_data.email
        )
    )

    user = result.scalar_one_or_none()

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    password_valid = verify_password(
        login_data.password,
        user.hashed_password
    )

    if not password_valid:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================================
# GET ALL COURSES - PUBLIC
# ==========================================

@app.get(
    "/api/v1/courses/",
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


# ==========================================
# CREATE COURSE - PROTECTED
# ==========================================

@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"]
)
async def create_course(
    course: CourseCreate,
    current_user: User = Depends(
        get_current_user
    ),
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
            status_code=status.HTTP_409_CONFLICT,
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

    return new_course


# ==========================================
# DELETE COURSE - PROTECTED
# ==========================================

@app.delete(
    "/api/v1/courses/{course_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"]
)
async def delete_course(
    course_id: int,
    current_user: User = Depends(
        get_current_user
    ),
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    await db.delete(course)

    await db.commit()

    return None


# ==========================================
# SECURITY NOTES
# ==========================================

# JWT payloads are Base64 encoded, not encrypted.
# Sensitive information such as passwords and card
# details must never be stored inside JWT payloads.

# CORS tells browsers which origins may access the API.
# CORS is enforced by browsers and is not an API
# authentication or authorization mechanism.

# OAuth2 Authorization Code Flow:
# A user is redirected to an authorization server.
# After successful authorization, the client receives
# an authorization code. The client exchanges the code
# for an access token.
#
# The simple JWT login implemented in this project is
# different. The user sends email and password directly
# to this API, and this API creates the JWT access token.
