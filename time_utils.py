"""Timezone-safe helpers for global FeeHunt UX."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


FALLBACK_TIMEZONE = "UTC"


def is_valid_timezone(timezone_name: str | None) -> bool:
    if not timezone_name:
        return False
    try:
        ZoneInfo(str(timezone_name).strip())
        return True
    except ZoneInfoNotFoundError:
        return False


def get_system_timezone_name() -> str:
    env_timezone = os.environ.get("TZ")
    if is_valid_timezone(env_timezone):
        return str(env_timezone).strip()

    local_tz = datetime.now().astimezone().tzinfo
    key = getattr(local_tz, "key", None)
    if is_valid_timezone(key):
        return str(key)

    return FALLBACK_TIMEZONE


def normalize_timezone(timezone_name: str | None) -> str:
    if is_valid_timezone(timezone_name):
        return str(timezone_name).strip()
    return get_system_timezone_name()


def get_timezone(timezone_name: str | None = None) -> ZoneInfo:
    return ZoneInfo(normalize_timezone(timezone_name))


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def local_now(timezone_name: str | None = None) -> datetime:
    return now_utc().astimezone(get_timezone(timezone_name))


def parse_datetime_utc(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def days_until_local(value: Any, timezone_name: str | None = None) -> int:
    end_utc = parse_datetime_utc(value)
    if not end_utc:
        return 0
    tz = get_timezone(timezone_name)
    end_date = end_utc.astimezone(tz).date()
    today = local_now(timezone_name).date()
    return max((end_date - today).days, 0)


def format_local_datetime(value: Any, timezone_name: str | None = None) -> str:
    parsed = parse_datetime_utc(value)
    if not parsed:
        return str(value or "")
    local_value = parsed.astimezone(get_timezone(timezone_name))
    return local_value.strftime("%Y-%m-%d %H:%M")


def greeting_key(timezone_name: str | None = None) -> str:
    hour = local_now(timezone_name).hour
    if 5 <= hour < 12:
        return "greeting.morning"
    if 12 <= hour < 17:
        return "greeting.afternoon"
    if 17 <= hour < 22:
        return "greeting.evening"
    return "greeting.late"
