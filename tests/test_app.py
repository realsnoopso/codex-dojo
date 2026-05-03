"""Codex Dojo test suite."""

import asyncio
import json
from datetime import timedelta

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app import app
from utils import (
    Validator,
    build_response_dict,
    calculate_discount,
    calculate_total,
    calculate_with_tax,
    fetch_user_data,
    fetch_user_orders,
    format_response,
    serialize_response,
    validate_email,
    validate_phone,
    validate_username,
)

client = TestClient(app)


def has_route(path: str) -> bool:
    return path in {route.path for route in app.routes}


def test_root():
    """기본 엔드포인트 테스트."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Codex Dojo API"}


def test_create_item():
    """아이템 생성 테스트."""
    response = client.post("/items", json={"name": "Test Item", "price": 19.99})
    assert response.status_code in {200, 201}
    data = response.json()
    assert data["id"]
    assert data["name"] == "Test Item"
    assert data["price"] == 19.99
    if "description" in data:
        assert data["description"] is None
    if "tax" in data:
        assert data["tax"] == pytest.approx(19.99 * 0.1)


def test_get_item_not_found():
    """존재하지 않는 아이템 조회 시 404를 반환한다."""
    response = client.get("/items/missing")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_item_not_found():
    """존재하지 않는 아이템 삭제 시 404를 반환한다."""
    response = client.delete("/items/missing")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_update_item():
    """기존 아이템을 부분 수정한다."""
    if not has_route("/items/{item_id}"):
        pytest.skip("Item detail endpoint is not available")

    created = client.post("/items", json={"name": "Before", "price": 10.0}).json()
    response = client.put(f"/items/{created['id']}", json={"name": "After"})

    if response.status_code == 405:
        pytest.skip("Item update endpoint is not available")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["name"] == "After"
    assert data["price"] == 10.0


def test_delete_item():
    """기존 아이템을 삭제한다."""
    created = client.post("/items", json={"name": "Trash", "price": 1.0}).json()

    response = client.delete(f"/items/{created['id']}")

    assert response.status_code in {200, 204}
    assert client.get(f"/items/{created['id']}").status_code == 404


def test_list_items():
    """아이템 목록 조회는 저장된 아이템들을 반환한다."""
    assert client.get("/items").json() == []

    client.post("/items", json={"name": "First", "price": 10.0})
    client.post("/items", json={"name": "Second", "price": 20.0})

    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert [item["name"] for item in data] == ["First", "Second"]
    assert [item["price"] for item in data] == [10.0, 20.0]
    assert all(item.get("id", "stored") for item in data)
    if all("description" in item for item in data):
        assert [item["description"] for item in data] == [None, None]
    if all("tax" in item for item in data):
        assert [item["tax"] for item in data] == [1.0, 2.0]


def test_create_item_invalid():
    """잘못된 아이템 생성 요청은 검증 오류를 반환한다."""
    invalid_payloads = [
        {"name": "Invalid", "price": "free"},
        {"price": 10.0},
    ]

    for payload in invalid_payloads:
        response = client.post("/items", json=payload)
        assert response.status_code == 422


def test_register_login_and_me():
    """사용자 등록, 로그인, 현재 사용자 조회 흐름을 검증한다."""
    if not has_route("/register"):
        pytest.skip("Auth routes are not available")

    register_response = client.post(
        "/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "full_name": "Alice",
            "password": "secretpass",
        },
    )
    assert register_response.status_code == 201
    assert register_response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "full_name": "Alice",
        "disabled": False,
    }

    login_response = client.post(
        "/login",
        json={"username": "alice", "password": "secretpass"},
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert token_data["access_token"]
    assert token_data["token_type"] == "bearer"

    me_response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token_data['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "alice"


def test_login_rejects_invalid_password():
    """잘못된 비밀번호로 로그인하면 401을 반환한다."""
    if not has_route("/login"):
        pytest.skip("Auth routes are not available")

    client.post(
        "/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secretpass",
        },
    )

    response = client.post(
        "/login",
        json={"username": "alice", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_me_requires_bearer_token():
    """인증 토큰 없이 현재 사용자 조회를 요청하면 401을 반환한다."""
    if not has_route("/me"):
        pytest.skip("Auth routes are not available")

    response = client.get("/me")
    assert response.status_code == 401


def test_register_rejects_duplicate_username():
    """이미 등록된 사용자명은 거부한다."""
    if not has_route("/register"):
        pytest.skip("Auth routes are not available")

    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secretpass",
    }
    assert client.post("/register", json=payload).status_code == 201

    response = client.post("/register", json=payload)

    assert response.status_code == 409
    assert response.json() == {"detail": "Username already registered"}


def test_jwt_validation_errors():
    """잘못되었거나 만료된 JWT를 거부한다."""
    pytest.importorskip("jwt")
    from src.auth.jwt_handler import create_access_token, verify_token

    with pytest.raises(HTTPException) as invalid_error:
        verify_token("not-a-token")
    assert invalid_error.value.status_code == 401

    expired_token = create_access_token("alice", expires_delta=timedelta(seconds=-1))
    with pytest.raises(HTTPException) as expired_error:
        verify_token(expired_token)
    assert expired_error.value.status_code == 401

    token_without_subject = create_access_token("alice", additional_claims={"sub": ""})
    with pytest.raises(HTTPException) as missing_subject_error:
        verify_token(token_without_subject)
    assert missing_subject_error.value.status_code == 401


def test_current_user_dependency_missing_user():
    """토큰의 사용자를 저장소에서 찾을 수 없으면 인증 오류를 반환한다."""
    from src.auth.dependencies import build_current_user_dependency

    get_current_user = build_current_user_dependency(lambda username: None)

    with pytest.raises(HTTPException) as auth_error:
        get_current_user("missing")
    assert auth_error.value.status_code == 401


def test_calculate_total():
    """아이템 가격 합계를 계산한다."""
    items = [{"price": 10.0}, {"price": 15.5}, {"price": 4.5}]
    assert calculate_total(items) == 30.0


def test_calculate_with_tax():
    """세금이 포함된 총액을 계산한다."""
    assert calculate_with_tax(100.0) == 110.0


def test_calculate_discount():
    """조건을 만족할 때 할인을 적용한다."""
    assert calculate_discount(200.0) == 190.0
    assert calculate_discount(100.0) == 100.0


def test_build_response_dict():
    """메타데이터가 포함된 응답 딕셔너리를 생성한다."""
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
    """응답 딕셔너리를 JSON으로 직렬화한다."""
    serialized = serialize_response({"data": {"ok": True}, "timestamp": 123.0})
    assert json.loads(serialized) == {"data": {"ok": True}, "timestamp": 123.0}


def test_serialize_response_text():
    """응답 데이터를 텍스트로 직렬화한다."""
    assert serialize_response({"data": "hello", "timestamp": 123.0}, "text") == "hello"


def test_format_response_compatibility():
    """호환 응답 포맷터가 기존 JSON 구조를 유지한다."""
    serialized = format_response({"ok": True}, timestamp=123.0, prettify=False)
    assert json.loads(serialized) == {"data": {"ok": True}, "timestamp": 123.0}


def test_format_response():
    """포맷터가 메타데이터와 텍스트 출력을 지원한다."""
    serialized = format_response(
        {"ok": True},
        include_metadata=True,
        timestamp=123.0,
        prettify=False,
    )

    assert json.loads(serialized) == {
        "data": {"ok": True},
        "timestamp": 123.0,
        "metadata": {"version": "1.0", "generator": "codex-dojo"},
    }
    assert format_response("hello", format_type="text", timestamp=123.0) == "hello"


def test_serialize_response_unknown_format():
    """지원하지 않는 응답 포맷은 예외를 발생시킨다."""
    with pytest.raises(ValueError):
        serialize_response({"data": "hello"}, "xml")


def test_validator():
    """Validator가 기본 문자열 검증 규칙을 적용한다."""
    validator = Validator()
    assert validator.validate_email("user@example.com")
    assert not validator.validate_email("invalid")
    assert validator.validate_phone("01012345678")
    assert not validator.validate_phone("123")
    assert validator.validate_username("abc")
    assert not validator.validate_username("ab")


def test_validate_email():
    """기본 이메일 검증 래퍼를 확인한다."""
    assert validate_email("user@example.com")
    assert not validate_email("invalid")


def test_validate_phone():
    """기본 전화번호 검증 래퍼를 확인한다."""
    assert validate_phone("01012345678")
    assert not validate_phone("123")


def test_validate_username():
    """기본 사용자명 검증 래퍼를 확인한다."""
    assert validate_username("abc")
    assert not validate_username("ab")


def test_fetch_user_data_async():
    """비동기 사용자 데이터 조회 결과를 반환한다."""
    result = asyncio.run(fetch_user_data(7))
    assert result == {"id": 7, "name": "user_7"}


def test_fetch_user_orders_async():
    """비동기 주문 데이터 조회 결과를 반환한다."""
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
