from datetime import date

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Date,
    UniqueConstraint
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

    students: Mapped[list["Student"]] = relationship(
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

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan"
    )


# ==========================================
# STUDENT MODEL
# ==========================================

class Student(Base):

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id")
    )

    enrollment_year: Mapped[int] = mapped_column(
        Integer
    )

    department: Mapped["Department"] = relationship(
        back_populates="students"
    )

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan"
    )


# ==========================================
# ENROLLMENT MODEL
# ==========================================

class Enrollment(Base):

    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"),
        nullable=False
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False
    )

    enrollment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    grade: Mapped[str | None] = mapped_column(
        String(2),
        nullable=True
    )

    student: Mapped["Student"] = relationship(
        back_populates="enrollments"
    )

    course: Mapped["Course"] = relationship(
        back_populates="enrollments"
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "course_id",
            name="uq_student_course"
        ),
    )
