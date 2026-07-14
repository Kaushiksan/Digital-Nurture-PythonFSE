from datetime import (
    datetime,
    timedelta,
    timezone
)

from jose import jwt

from passlib.context import CryptContext


# ==========================================
# JWT CONFIGURATION
# ==========================================

SECRET_KEY = "course-management-secret-key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ==========================================
# PASSWORD HASHING
# ==========================================

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_password_hash(
    password: str
) -> str:

    # bcrypt is intentionally slow and uses a work factor.
    # This makes brute-force password attacks expensive.
    #
    # MD5 and SHA-256 are designed to be fast, so they
    # should not be used directly for password storage.

    return password_context.hash(
        password
    )


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return password_context.verify(
        plain_password,
        hashed_password
    )


# ==========================================
# CREATE JWT ACCESS TOKEN
# ==========================================

def create_access_token(
    data: dict
) -> str:

    token_data = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    token_data.update({
        "exp": expire
    })

    return jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
