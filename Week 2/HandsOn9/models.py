from sqlalchemy import (
    Integer,
    String,
    Boolean
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from database import Base


# ==========================================
# USER MODEL
# ==========================================

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
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
        Integer,
        nullable=False
    )
