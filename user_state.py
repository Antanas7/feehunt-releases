"""Small privacy-first user state helpers for adaptive calm UX."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class UserStateProfile:
    state: str
    help_level: str
    clutter_level: str
    show_extra_guidance: bool
    prefer_calm_signals: bool
    priority: int
    noise_budget: str


def _count_promotions(scan_data: dict[str, Any] | None) -> int:
    if not scan_data:
        return 0
    explicit_count = scan_data.get("promotions_found")
    if isinstance(explicit_count, int):
        return explicit_count
    return sum(
        len(scan_data.get(section, []) or [])
        for section in ("promotional_emails", "shop_emails", "newsletter_emails")
    )


def _count_subscriptions(scan_data: dict[str, Any] | None) -> int:
    if not scan_data:
        return 0
    explicit_count = scan_data.get("subscriptions_found")
    if isinstance(explicit_count, int):
        return explicit_count
    return len(scan_data.get("subscriptions", []) or [])


def _days_since(value: Any) -> int | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return max((datetime.now(timezone.utc) - parsed.astimezone(timezone.utc)).days, 0)


def build_user_state_profile(
    settings: dict[str, Any] | None,
    scan_data: dict[str, Any] | None,
    memory: dict[str, Any] | None = None,
) -> UserStateProfile:
    settings = settings or {}
    progress = (memory or {}).get("progress", {}) if isinstance(memory, dict) else {}
    if settings.get("adaptive_guidance_enabled") is False:
        return UserStateProfile(
            state="steady",
            help_level="balanced",
            clutter_level="manual",
            show_extra_guidance=True,
            prefer_calm_signals=True,
            priority=40,
            noise_budget="medium",
        )

    is_new = not bool(settings.get("ftue_completed")) or not scan_data
    scans_completed = int(progress.get("scans_completed") or 0)
    days_since_visit = _days_since(progress.get("last_visit_at") or progress.get("last_seen_at"))
    promotions = _count_promotions(scan_data)
    subscriptions = _count_subscriptions(scan_data)
    risks = len((scan_data or {}).get("financial_risks", []) or [])

    if is_new:
        return UserStateProfile(
            state="new",
            help_level="guided",
            clutter_level="unknown",
            show_extra_guidance=True,
            prefer_calm_signals=False,
            priority=10,
            noise_budget="guided",
        )

    if scans_completed > 0 and days_since_visit is not None and days_since_visit >= 3:
        return UserStateProfile(
            state="returning",
            help_level="summary",
            clutter_level="unknown",
            show_extra_guidance=False,
            prefer_calm_signals=True,
            priority=60,
            noise_budget="low",
        )

    if promotions >= 25 or subscriptions >= 6 or risks >= 2:
        return UserStateProfile(
            state="overwhelmed",
            help_level="supportive",
            clutter_level="high",
            show_extra_guidance=True,
            prefer_calm_signals=False,
            priority=90,
            noise_budget="step_by_step",
        )

    if promotions <= 3 and subscriptions <= 2 and risks == 0:
        return UserStateProfile(
            state="calm",
            help_level="minimal",
            clutter_level="low",
            show_extra_guidance=False,
            prefer_calm_signals=True,
            priority=20,
            noise_budget="minimal",
        )

    return UserStateProfile(
        state="steady",
        help_level="balanced",
        clutter_level="medium",
        show_extra_guidance=True,
        prefer_calm_signals=True,
        priority=50,
        noise_budget="balanced",
    )
