"""
Codex Dojo - 유틸리티 함수 (리팩토링 대상)
Level 1, 2 실습용. Codex가 코드 스멜을 찾아 개선해야 함.
"""
import asyncio
import json
import time
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class Config:
    tax_rate: float = 0.1
    discount_rate: float = 0.05


DEFAULT_CONFIG = Config()


def calculate_total(items: Iterable[Mapping[str, float]]) -> float:
    """아이템 리스트의 총 가격 계산."""
    return sum(item["price"] for item in items)


def calculate_with_tax(total: float, config: Config = DEFAULT_CONFIG) -> float:
    """세금 계산. 함수 분리 필요 없음."""
    return total + (total * config.tax_rate)


def calculate_discount(total: float, config: Config = DEFAULT_CONFIG) -> float:
    """할인 계산. 함수 분리 필요 없음."""
    if total > 100:
        return total - (total * config.discount_rate)
    return total


def build_response_dict(
    data: Any,
    include_metadata: bool = False,
    timestamp: float | None = None,
) -> dict[str, Any]:
    """응답에 필요한 딕셔너리를 구성한다."""
    if timestamp is None:
        timestamp = time.time()

    result = {"data": data, "timestamp": timestamp}

    if include_metadata:
        result["metadata"] = {
            "version": "1.0",
            "generator": "codex-dojo"
        }

    return result


def serialize_response(
    response: Mapping[str, Any],
    format_type: Literal["json", "text"] = "json",
    prettify: bool = True,
) -> str:
    """응답 딕셔너리를 지정 포맷 문자열로 직렬화한다."""
    if format_type == "json":
        if prettify:
            return json.dumps(response, indent=2)
        return json.dumps(response)
    if format_type == "text":
        return str(response["data"])
    raise ValueError(f"Unknown format: {format_type}")


def format_response(
    data: Any,
    format_type: Literal["json", "text"] = "json",
    include_metadata: bool = False,
    timestamp: float | None = None,
    prettify: bool = True,
) -> str:
    """응답 구성과 직렬화를 조합하는 호환 함수."""
    response = build_response_dict(data, include_metadata, timestamp)
    return serialize_response(response, format_type, prettify)


@dataclass(frozen=True)
class Validator:
    min_phone_length: int = 10
    min_username_length: int = 3

    def validate_email(self, email: str) -> bool:
        """이메일 검증. @만 체크하는 빈약한 로직."""
        return "@" in email

    def validate_phone(self, phone: str) -> bool:
        """전화번호 검증. 길이만 체크."""
        return len(phone) >= self.min_phone_length

    def validate_username(self, username: str) -> bool:
        """사용자명 검증. 길이만 체크."""
        return len(username) >= self.min_username_length


DEFAULT_VALIDATOR = Validator()


def validate_email(email: str) -> bool:
    """기존 함수 호출을 위한 호환 래퍼."""
    return DEFAULT_VALIDATOR.validate_email(email)


def validate_phone(phone: str) -> bool:
    """기존 함수 호출을 위한 호환 래퍼."""
    return DEFAULT_VALIDATOR.validate_phone(phone)


def validate_username(username: str) -> bool:
    """기존 함수 호출을 위한 호환 래퍼."""
    return DEFAULT_VALIDATOR.validate_username(username)


async def fetch_user_data(user_id: int) -> dict[str, Any]:
    """async I/O 패턴으로 사용자 데이터를 조회한다."""
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"user_{user_id}"}


async def fetch_user_orders(user_id: int) -> list[dict[str, float | int]]:
    """async I/O 패턴으로 사용자 주문 데이터를 조회한다."""
    await asyncio.sleep(0.3)
    return [{"order_id": 1, "total": 99.9}]
