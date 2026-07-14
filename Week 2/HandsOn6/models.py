from sqlalchemy import (
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database import Base


# ==========================================
# DEPARTMENT MODEL
# ==========================================

class Department(Base):

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    courses: Mapped[list["Course"]] = relationship(
        back_populates="department"
    )


# ==========================================
# COURSE MODEL
# ==========================================

class Course(Base):

    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id")
    )

    department: Mapped["Department"] = relationship(
        back_populates="courses"
    )
