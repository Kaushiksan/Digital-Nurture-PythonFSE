from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict
)


# ==========================================
# COURSE CREATE
# ==========================================

class CourseCreate(BaseModel):

    name: str
    code: str
    credits: int
    department_id: int


# ==========================================
# COURSE PUT
# ==========================================

class CourseReplace(BaseModel):

    name: str
    code: str
    credits: int
    department_id: int


# ==========================================
# COURSE PATCH
# ==========================================

class CoursePatch(BaseModel):

    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


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
