from typing import Optional, List

from pydantic import BaseModel, ConfigDict


# ==========================================
# COURSE CREATE SCHEMA
# ==========================================

class CourseCreate(BaseModel):

    name: str
    code: str
    credits: int
    department_id: int


# ==========================================
# COURSE UPDATE SCHEMA
# ==========================================

class CourseUpdate(BaseModel):

    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


# ==========================================
# COURSE RESPONSE SCHEMA
# ==========================================

class CourseResponse(BaseModel):

    id: int
    name: str
    code: str
    credits: int
    department_id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# DEPARTMENT RESPONSE SCHEMA
# ==========================================

class DepartmentResponse(BaseModel):

    id: int
    name: str
    courses: List[CourseResponse] = []

    model_config = ConfigDict(from_attributes=True)
