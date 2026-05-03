"""
Codex Dojo - 테스트 파일 (의도적으로 불완전)
Level 1, 2 실습용. Codex가 빠진 테스트를 채워야 함.
"""
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

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
    # 버그: tax 필드 검증 누락

# 빠진 테스트들 (Codex가 작성해야 함):
# - test_get_item_not_found (404 처리)
# - test_delete_item_not_found (404 처리)
# - test_list_items (빈 리스트, 여러 아이템)
# - test_create_item_invalid (잘못된 입력)
# - test_calculate_total (utils.py)
# - test_calculate_with_tax (utils.py)
# - test_format_response (utils.py)
