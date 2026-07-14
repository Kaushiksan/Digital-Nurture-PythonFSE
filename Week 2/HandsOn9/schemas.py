from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr
)


# ==========================================
# USER REGISTRATION
# ==========================================

class UserRegister(BaseModel):

    email: EmailStr

    password: str


# ==========================================
# USER RESPONSE
# ==========================================

class UserResponse(BaseModel):

    id: int

    email: EmailStr

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================
# LOGIN SCHEMA
# ==========================================

class LoginRequest(BaseModel):

    email: EmailStr

    password: str


# ==========================================
# TOKEN RESPONSE
# ==========================================

class TokenResponse(BaseModel):

    access_token: str

    token_type: str


# ==========================================
# COURSE CREATE
# ==========================================

class CourseCreate(BaseModel):

    name: str

    code: str

    credits: int

    department_id: int


# ==========================================
# COURSE RESPONSE
# ==========================================

class CourseResponse(BaseModel):

    id: int

    name: str

    code: str

    credits: int

    department_id: int

    model_config = ConfigDict(
        from_attributes=True
    )
