"""Pydantic models for item payloads."""

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Shared item fields."""

    name: str = Field(min_length=1, max_length=100)
    price: float = Field(ge=0)
    description: str | None = Field(default=None, max_length=500)


class ItemCreate(ItemBase):
    """Request body for creating an item."""

    pass


class ItemUpdate(BaseModel):
    """Request body for partially updating an item."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: float | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, max_length=500)


class ItemRead(ItemBase):
    """Response body for item records."""

    id: str
