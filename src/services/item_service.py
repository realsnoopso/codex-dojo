"""In-memory item persistence service."""

from uuid import uuid4

from src.models.item import ItemCreate, ItemRead, ItemUpdate


class ItemService:
    """Manage item records in memory."""

    def __init__(self) -> None:
        """Initialize an empty item store."""
        self._items: dict[str, ItemRead] = {}

    def create(self, item: ItemCreate) -> ItemRead:
        """Create and store a new item."""
        item_id: str = str(uuid4())
        created_item: ItemRead = ItemRead(id=item_id, **item.model_dump())
        self._items[item_id] = created_item
        return created_item

    def list(self) -> list[ItemRead]:
        """Return all stored items."""
        return list(self._items.values())

    def get(self, item_id: str) -> ItemRead | None:
        """Return an item by ID, if it exists."""
        return self._items.get(item_id)

    def update(self, item_id: str, item: ItemUpdate) -> ItemRead | None:
        """Update an item by ID, if it exists."""
        current_item: ItemRead | None = self._items.get(item_id)
        if current_item is None:
            return None

        update_data: dict[str, object] = item.model_dump(exclude_unset=True)
        updated_item: ItemRead = current_item.model_copy(update=update_data)
        self._items[item_id] = updated_item
        return updated_item

    def delete(self, item_id: str) -> bool:
        """Delete an item by ID and report whether it existed."""
        if item_id not in self._items:
            return False

        del self._items[item_id]
        return True

    def clear(self) -> None:
        """Remove all stored items."""
        self._items.clear()


item_service: ItemService = ItemService()
