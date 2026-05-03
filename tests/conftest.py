"""Shared pytest fixtures for the API test suite."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as app_module


@pytest.fixture
def items_db():
    """Return the active in-memory item store."""
    if hasattr(app_module, "items_db"):
        return app_module.items_db

    from src.services.item_service import item_service

    return item_service._items


@pytest.fixture(autouse=True)
def reset_items_db(items_db):
    """Clear item state before and after each test."""
    items_db.clear()
    yield
    items_db.clear()


@pytest.fixture(autouse=True)
def reset_users_db():
    try:
        from src.routes.auth import users_db
    except ImportError:
        yield
        return

    users_db.clear()
    yield
    users_db.clear()
