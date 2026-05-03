"""Item route definitions."""

from fastapi import APIRouter, HTTPException, status

from src.models.item import ItemCreate, ItemRead, ItemUpdate
from src.services.item_service import item_service

router: APIRouter = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate) -> ItemRead:
    """Create a new item."""
    return item_service.create(item)


@router.get("", response_model=list[ItemRead])
def list_items() -> list[ItemRead]:
    """Return all stored items."""
    return item_service.list()


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: str) -> ItemRead:
    """Return a single item by ID."""
    item: ItemRead | None = item_service.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


@router.put("/{item_id}", response_model=ItemRead)
def update_item(item_id: str, item: ItemUpdate) -> ItemRead:
    """Update an existing item by ID."""
    updated_item: ItemRead | None = item_service.update(item_id, item)
    if updated_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str) -> None:
    """Delete an existing item by ID."""
    deleted: bool = item_service.delete(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
