"""
Codex Dojo - 테스트 파일 (의도적으로 불완전)
Level 1, 2 실습용. Codex가 빠진 테스트를 채워야 함.
"""
import asyncio
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app, items_db
from fastapi.testclient import TestClient
from utils import (
    DEFAULT_CONFIG,
    Validator,
    build_response_dict,
    calculate_discount,
    calculate_total,
    calculate_with_tax,
    fetch_user_data,
    fetch_user_orders,
    format_response,
    serialize_response,
)

client = TestClient(app)


def setup_function():
    items_db.clear()


def test_root():
    """기본 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Codex Dojo API"}

def test_create_item():
    """아이템 생성 테스트"""
    response = client.post("/items", json={"name": "Test Item", "price": 19.99})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["tax"] == pytest.approx(19.99 * DEFAULT_CONFIG.tax_rate)


def test_get_item_not_found():
    response = client.get("/items/missing")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_item_not_found():
    response = client.delete("/items/missing")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_list_items():
    assert client.get("/items").json() == []

    client.post("/items", json={"name": "First", "price": 10.0})
    client.post("/items", json={"name": "Second", "price": 20.0})

    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "First", "price": 10.0, "tax": 1.0},
        {"name": "Second", "price": 20.0, "tax": 2.0},
    ]


def test_create_item_invalid():
    response = client.post("/items", json={"name": "Invalid", "price": "free"})
    assert response.status_code == 422


def test_calculate_total():
    items = [{"price": 10.0}, {"price": 15.5}, {"price": 4.5}]
    assert calculate_total(items) == 30.0


def test_calculate_with_tax():
    assert calculate_with_tax(100.0) == 110.0


def test_calculate_discount():
    assert calculate_discount(200.0) == 190.0
    assert calculate_discount(100.0) == 100.0


def test_build_response_dict():
    response = build_response_dict(
        {"ok": True},
        include_metadata=True,
        timestamp=123.0,
    )
    assert response == {
        "data": {"ok": True},
        "timestamp": 123.0,
        "metadata": {"version": "1.0", "generator": "codex-dojo"},
    }


def test_serialize_response_json():
    serialized = serialize_response({"data": {"ok": True}, "timestamp": 123.0})
    assert json.loads(serialized) == {"data": {"ok": True}, "timestamp": 123.0}


def test_serialize_response_text():
    assert serialize_response({"data": "hello", "timestamp": 123.0}, "text") == "hello"


def test_format_response_compatibility():
    serialized = format_response({"ok": True}, timestamp=123.0, prettify=False)
    assert json.loads(serialized) == {"data": {"ok": True}, "timestamp": 123.0}


def test_serialize_response_unknown_format():
    with pytest.raises(ValueError):
        serialize_response({"data": "hello"}, "xml")


def test_validator():
    validator = Validator()
    assert validator.validate_email("user@example.com")
    assert not validator.validate_email("invalid")
    assert validator.validate_phone("01012345678")
    assert not validator.validate_phone("123")
    assert validator.validate_username("abc")
    assert not validator.validate_username("ab")


def test_fetch_user_data_async():
    result = asyncio.run(fetch_user_data(7))
    assert result == {"id": 7, "name": "user_7"}


def test_fetch_user_orders_async():
    result = asyncio.run(fetch_user_orders(7))
    assert result == [{"order_id": 1, "total": 99.9}]

# 빠진 테스트들 (Codex가 작성해야 함):
# - test_get_item_not_found (404 처리)
# - test_delete_item_not_found (404 처리)
# - test_list_items (빈 리스트, 여러 아이템)
# - test_create_item_invalid (잘못된 입력)
# - test_calculate_total (utils.py)
# - test_calculate_with_tax (utils.py)
# - test_format_response (utils.py)
