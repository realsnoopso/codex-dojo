"""Utility functions for Codex Dojo."""

import asyncio
import json
import time
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class Config:
    """Runtime configuration for utility calculations."""

    tax_rate: float = 0.1
    discount_rate: float = 0.05


DEFAULT_CONFIG = Config()


def calculate_total(items: Iterable[Mapping[str, float]]) -> float:
    """Calculate the total price from item mappings."""
    return sum(item["price"] for item in items)


def calculate_with_tax(total: float, config: Config = DEFAULT_CONFIG) -> float:
    """Calculate a total after applying the configured tax rate."""
    return total + (total * config.tax_rate)


def calculate_discount(total: float, config: Config = DEFAULT_CONFIG) -> float:
    """Apply the configured discount rate when the total qualifies."""
    if total > 100:
        return total - (total * config.discount_rate)
    return total


def build_response_dict(
    data: Any,
    include_metadata: bool = False,
    timestamp: float | None = None,
) -> dict[str, Any]:
    """Build a response dictionary with an optional metadata block."""
    if timestamp is None:
        timestamp = time.time()

    result = {"data": data, "timestamp": timestamp}

    if include_metadata:
        result["metadata"] = {"version": "1.0", "generator": "codex-dojo"}

    return result


def serialize_response(
    response: Mapping[str, Any],
    format_type: Literal["json", "text"] = "json",
    prettify: bool = True,
) -> str:
    """Serialize a response dictionary as JSON or plain text."""
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
    """Build and serialize a response in one compatibility helper."""
    response = build_response_dict(data, include_metadata, timestamp)
    return serialize_response(response, format_type, prettify)


@dataclass(frozen=True)
class Validator:
    """Validate common user-facing string fields."""

    min_phone_length: int = 10
    min_username_length: int = 3

    def validate_email(self, email: str) -> bool:
        """Return whether an email contains the minimum required marker."""
        return "@" in email

    def validate_phone(self, phone: str) -> bool:
        """Return whether a phone number meets the minimum length."""
        return len(phone) >= self.min_phone_length

    def validate_username(self, username: str) -> bool:
        """Return whether a username meets the minimum length."""
        return len(username) >= self.min_username_length


DEFAULT_VALIDATOR = Validator()


def validate_email(email: str) -> bool:
    """Validate an email address with the default validator."""
    return DEFAULT_VALIDATOR.validate_email(email)


def validate_phone(phone: str) -> bool:
    """Validate a phone number with the default validator."""
    return DEFAULT_VALIDATOR.validate_phone(phone)


def validate_username(username: str) -> bool:
    """Validate a username with the default validator."""
    return DEFAULT_VALIDATOR.validate_username(username)


async def fetch_user_data(user_id: int) -> dict[str, Any]:
    """Fetch user profile data asynchronously."""
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"user_{user_id}"}


async def fetch_user_orders(user_id: int) -> list[dict[str, float | int]]:
    """Fetch user order data asynchronously."""
    await asyncio.sleep(0.3)
    return [{"order_id": 1, "total": 99.9}]
