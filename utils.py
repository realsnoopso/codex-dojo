"""
Codex Dojo - 유틸리티 함수 (리팩토링 대상)
Level 1, 2 실습용. Codex가 코드 스멜을 찾아 개선해야 함.
"""
import json
import time

# 리팩토링 대상 1: 비효율적인 반복문 + 전역 변수 남용
TAX_RATE = 0.1
DISCOUNT_RATE = 0.05

def calculate_total(items):
    """아이템 리스트의 총 가격 계산. 개선 필요."""
    total = 0
    for i in items:
        total = total + i['price']  # 비효율적 누적
    return total

def calculate_with_tax(total):
    """세금 계산. 함수 분리 필요 없음."""
    return total + (total * TAX_RATE)

def calculate_discount(total):
    """할인 계산. 함수 분리 필요 없음."""
    if total > 100:
        return total - (total * DISCOUNT_RATE)
    return total

# 리팩토링 대상 2: 너무 많은 책임을 가진 함수
def format_response(data, format_type="json", include_metadata=False, timestamp=None, prettify=True):
    """포맷팅 함수. SRP 위반, 분리 필요."""
    if timestamp is None:
        timestamp = time.time()
    
    result = {"data": data, "timestamp": timestamp}
    
    if include_metadata:
        result["metadata"] = {
            "version": "1.0",
            "generator": "codex-dojo"
        }
    
    if format_type == "json":
        if prettify:
            return json.dumps(result, indent=2)
        return json.dumps(result)
    elif format_type == "text":
        return str(data)
    else:
        raise ValueError(f"Unknown format: {format_type}")

# 리팩토링 대상 3: 중복 코드
def validate_email(email):
    """이메일 검증. @만 체크하는 빈약한 로직."""
    return "@" in email

def validate_phone(phone):
    """전화번호 검증. 길이만 체크."""
    return len(phone) >= 10

def validate_username(username):
    """사용자명 검증. 길이만 체크."""
    return len(username) >= 3

# 리팩토링 대상 4: async/await 패턴으로 변환 필요
def fetch_user_data(user_id):
    """동기 함수 — async로 변환해야 함."""
    time.sleep(0.5)  # I/O 시뮬레이션
    return {"id": user_id, "name": f"user_{user_id}"}

def fetch_user_orders(user_id):
    """동기 함수 — async로 변환해야 함."""
    time.sleep(0.3)
    return [{"order_id": 1, "total": 99.9}]
