"""User and authentication Pydantic models."""

from pydantic import BaseModel, Field


class User(BaseModel):
    """Public user profile fields."""

    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=3, max_length=254)
    full_name: str | None = Field(default=None, max_length=100)
    disabled: bool = False


class UserCreate(User):
    """Request body for user registration."""

    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Request body for user login."""

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=1, max_length=128)


class Token(BaseModel):
    """Bearer token response body."""

    access_token: str
    token_type: str = "bearer"
