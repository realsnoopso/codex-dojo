"""Authentication route definitions."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext

from src.auth.dependencies import build_current_user_dependency
from src.auth.jwt_handler import create_access_token
from src.models.user import Token, User, UserCreate, UserLogin

router: APIRouter = APIRouter(tags=["auth"])
password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
users_db: dict[str, dict[str, Any]] = {}


def hash_password(password: str) -> str:
    """Hash a plain-text password for storage."""
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored hash."""
    return password_context.verify(plain_password, hashed_password)


def get_stored_user(username: str) -> dict[str, Any] | None:
    """Return a stored user record by username."""
    return users_db.get(username)


get_current_user = build_current_user_dependency(get_stored_user)
current_user_dependency = Depends(get_current_user)


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate) -> User:
    """Register a new user."""
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered",
        )

    user_data = user.model_dump(exclude={"password"})
    users_db[user.username] = {
        **user_data,
        "hashed_password": hash_password(user.password),
    }
    return User.model_validate(user_data)


@router.post("/login", response_model=Token)
def login(credentials: UserLogin) -> Token:
    """Authenticate a user and return a bearer token."""
    stored_user = users_db.get(credentials.username)
    if stored_user is None or not verify_password(
        credentials.password,
        stored_user["hashed_password"],
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=create_access_token(subject=credentials.username))


@router.get("/me", response_model=User)
def read_me(current_user: User = current_user_dependency) -> User:
    """Return the currently authenticated user."""
    return current_user
