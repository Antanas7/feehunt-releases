"""FeeHunt license-key client based on the BeSafe trial model."""

from __future__ import annotations

import hashlib
import json
import platform
import socket
import urllib.error
import urllib.request
from datetime import datetime
from typing import Any

from config import LICENSE_FILE, LICENSING_API_BASE_URL
from time_utils import days_until_local, now_utc, parse_datetime_utc


DEFAULT_TRIAL_DAYS = 7
OFFLINE_GRACE_DAYS = 7
LICENSE_KEY_PREFIX = "FHUNT-"

# Trial users get this many full scans (with all features) before being
# asked to activate a paid plan. Once exhausted, the app keeps showing
# the prior scan's results but blocks new scans and auto-cleanup.
TRIAL_SCAN_LIMIT = 3


def _now() -> datetime:
    return now_utc()


def _parse_datetime(value: Any) -> datetime | None:
    return parse_datetime_utc(value)


def _days_until(value: Any) -> int:
    return days_until_local(value)


def normalize_license_key(value: str) -> str:
    return str(value or "").strip().upper().replace(" ", "")


def is_license_key_shape(value: str) -> bool:
    key = normalize_license_key(value)
    parts = key.split("-")
    return (
        len(parts) == 5
        and parts[0] == "FHUNT"
        and all(len(part) == 4 and part.isalnum() for part in parts[1:])
    )


def get_device_fingerprint() -> str:
    raw = "|".join(
        [
            platform.node(),
            platform.system(),
            platform.release(),
            platform.machine(),
            socket.gethostname(),
        ]
    )
    digest = hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()[:24]
    return f"fh_{digest}"


def _read_json(path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def _write_json(path, data: dict[str, Any]) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def _api_post(endpoint: str, payload: dict[str, Any], timeout: int = 20) -> dict[str, Any]:
    url = f"{LICENSING_API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "User-Agent": "FeeHunt/1.3.0 (+https://feehunt.pro)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            text = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(text)
        except Exception:
            data = {}
        return {
            "ok": False,
            "offline": False,
            "status": str(data.get("status") or "error"),
            "http_status": exc.code,
            "error": data.get("error") or data.get("message") or f"HTTP {exc.code}",
        }
    except Exception as exc:
        return {"ok": False, "offline": True, "error": str(exc)}

    try:
        data = json.loads(text)
    except Exception:
        return {"ok": False, "offline": False, "error": "FeeHunt server returned unreadable data."}
    return data if isinstance(data, dict) else {"ok": False, "error": "FeeHunt server returned invalid data."}


def load_license() -> dict[str, Any] | None:
    return _read_json(LICENSE_FILE)


# Fields that live on the local license file only — server never returns
# them, so each refresh of the gate must merge them back in or the trial
# counter (and similar local-only state) would be wiped on every save.
_LOCAL_ONLY_LICENSE_FIELDS = (
    "trial_scans_used",
    "trial_scan_last_used_at",
    "trial_first_scan_at",
    "connected_gmail_accounts",
)


def _merge_local_only_fields(gate: dict[str, Any]) -> dict[str, Any]:
    """Copy local-only fields from the existing license file into the new
    gate dict before it's written back. Without this, save_license(gate)
    overwrites trial_scans_used and the scan quota never enforces."""
    existing = _read_json(LICENSE_FILE) or {}
    for field in _LOCAL_ONLY_LICENSE_FIELDS:
        if field in existing and field not in gate:
            gate[field] = existing[field]
    return gate


def save_license(license_data: dict[str, Any]) -> bool:
    return _write_json(LICENSE_FILE, license_data)


def clear_license() -> None:
    try:
        if LICENSE_FILE.exists():
            LICENSE_FILE.unlink()
    except Exception:
        pass


def activate_license(license_key: str) -> dict[str, Any]:
    key = normalize_license_key(license_key)
    if not is_license_key_shape(key):
        return {
            "ok": False,
            "allowed": False,
            "status": "invalid",
            "message": "Enter the FeeHunt license key from your email. It should look like FHUNT-XXXX-XXXX-XXXX-XXXX.",
        }

    result = _api_post(
        "verify-license",
        {
            "license_key": key,
            "device_fingerprint": get_device_fingerprint(),
            "device_name": platform.node() or "Windows PC",
        },
    )
    gate = _gate_from_verify_response(key, result, online=not result.get("offline"))
    if gate.get("allowed"):
        _merge_local_only_fields(gate)
        save_license(gate)
    return gate


def check_license(force_online: bool = False) -> dict[str, Any]:
    local = load_license()
    if not local or not local.get("license_key"):
        return {
            "ok": False,
            "allowed": False,
            "status": "missing_license",
            "message": "Activate FeeHunt with the license key from your email.",
        }

    result = _api_post(
        "verify-license",
        {
            "license_key": local["license_key"],
            "device_fingerprint": get_device_fingerprint(),
            "device_name": platform.node() or "Windows PC",
        },
    )

    if result.get("offline") and not force_online:
        last_checked = _parse_datetime(local.get("last_checked_at"))
        if last_checked and (_now() - last_checked).days <= OFFLINE_GRACE_DAYS:
            cached = {**local, "online": False}
            cached["allowed"] = local.get("status") in {"trial", "active"}
            cached["message"] = f"Offline access is allowed for up to {OFFLINE_GRACE_DAYS} days after the last successful license check."
            return cached

    gate = _gate_from_verify_response(local["license_key"], result, online=not result.get("offline"))
    if gate.get("allowed"):
        _merge_local_only_fields(gate)
        save_license(gate)
    return gate


def _gate_from_verify_response(license_key: str, data: dict[str, Any], online: bool) -> dict[str, Any]:
    status = str(data.get("status") or ("offline" if data.get("offline") else "invalid")).lower()
    allowed = status in {"trial", "active"}
    trial_ends_at = data.get("trial_ends_at")
    days_remaining = int(data.get("days_remaining") or _days_until(trial_ends_at))

    if status in {"read_only", "expired"}:
        status = "expired"

    return {
        "ok": bool(allowed),
        "allowed": allowed,
        "online": online,
        "license_key": normalize_license_key(license_key),
        "status": status,
        "plan_type": data.get("plan") or "personal",
        "billing": data.get("billing") or "monthly",
        "trial_days": DEFAULT_TRIAL_DAYS,
        "days_remaining": days_remaining,
        "trial_ends_at": trial_ends_at,
        "last_checked_at": _now().isoformat() if allowed else None,
        "message": data.get("message") or data.get("error") or ("FeeHunt license is active." if allowed else "FeeHunt license could not be verified."),
    }

def get_trial_status(license_data: dict[str, Any] | None = None) -> dict[str, Any]:
    data = license_data or load_license() or {}
    status = str(data.get("status") or "invalid")
    return {
        "trial_active": status == "trial",
        "trial_started_at": data.get("trial_started_at"),
        "trial_ends_at": data.get("trial_ends_at"),
        "checked_at": _now().isoformat(),
        "status": status,
        "days_remaining": int(data.get("days_remaining") or _days_until(data.get("trial_ends_at"))),
        "message": data.get("message") or "",
    }


def get_plan_limits(plan_name: str | None = None) -> dict[str, int | str]:
    plan = (plan_name or "personal").strip().lower()
    if plan == "personal":
        plan = "basic"
    limits = {"trial": 1, "basic": 1, "personal": 1, "family": 3, "pro": 10}
    return {"plan": plan, "gmail_accounts": limits.get(plan, 1)}


def get_license_overview(license_data: dict[str, Any] | None = None) -> dict[str, Any]:
    data = license_data or load_license() or {}
    plan_limits = get_plan_limits(data.get("plan_type"))
    accounts = data.get("connected_gmail_accounts", [])
    if not isinstance(accounts, list):
        accounts = []
    return {
        "status": data.get("status") or "invalid",
        "trial_days_remaining": int(data.get("days_remaining") or _days_until(data.get("trial_ends_at"))),
        "plan_name": plan_limits["plan"],
        "allowed_gmail_accounts": plan_limits["gmail_accounts"],
        "connected_gmail_accounts": accounts,
        "connected_gmail_count": len(accounts),
        "trial": get_trial_status(data),
    }


def register_gmail_account(gmail_address: str, license_key: str | None = None) -> dict[str, Any]:
    normalized_email = str(gmail_address or "").strip().lower()
    if not normalized_email:
        return {"registered": False, "status": "missing_email", "gmail_address": ""}
    data = load_license() or {}
    accounts = data.get("connected_gmail_accounts", [])
    if not isinstance(accounts, list):
        accounts = []
    overview = get_license_overview(data)
    allowed_accounts = int(overview.get("allowed_gmail_accounts") or 1)
    if normalized_email not in accounts:
        if len(accounts) >= allowed_accounts:
            return {
                "registered": False,
                "status": "plan_limit_exceeded",
                "gmail_address": normalized_email,
                "connected_gmail_accounts": accounts,
                "message": (
                    f"This FeeHunt plan allows {allowed_accounts} Gmail account(s). "
                    "Disconnect another account or upgrade your plan before connecting this Gmail account."
                ),
            }
        accounts.append(normalized_email)
    data["connected_gmail_accounts"] = accounts
    if license_key:
        data["license_key"] = normalize_license_key(license_key)
    save_license(data)
    return {"registered": True, "status": "registered", "gmail_address": normalized_email, "connected_gmail_accounts": accounts}


def can_add_gmail_account(license_data: dict[str, Any] | None, gmail_address: str) -> dict[str, Any]:
    overview = get_license_overview(license_data)
    normalized_email = str(gmail_address or "").strip().lower()
    accounts = overview["connected_gmail_accounts"]
    if normalized_email in accounts:
        return {"allowed": True, "status": "already_registered", "gmail_address": normalized_email}
    allowed = overview["connected_gmail_count"] < overview["allowed_gmail_accounts"]
    return {
        "allowed": allowed,
        "status": "allowed" if allowed else "plan_limit_exceeded",
        "gmail_address": normalized_email,
        "message": "" if allowed else "Upgrade your FeeHunt plan to connect more Gmail accounts.",
    }


# ============================================================
# Trial scan quota tracking
# ============================================================
#
# Trial users get TRIAL_SCAN_LIMIT full scans (with all features) before
# the app shifts to read-only-mode and asks them to activate a paid plan.
# Active (paid) users are never quota-limited. The trial date window is
# enforced separately by trial_ends_at.
#
# State lives on the local license file (not local memory) so it survives
# settings reset but is naturally scoped per device. Cross-device tracking
# would require server-side enforcement (Phase 2).

def trial_scans_used(license_data: dict[str, Any] | None = None) -> int:
    data = license_data if license_data is not None else load_license() or {}
    try:
        return max(0, int(data.get("trial_scans_used", 0) or 0))
    except (TypeError, ValueError):
        return 0


def trial_scans_remaining(license_data: dict[str, Any] | None = None) -> int:
    return max(0, TRIAL_SCAN_LIMIT - trial_scans_used(license_data))


def mark_trial_scan_used() -> int:
    """Increment trial_scans_used on the local license file. Returns the
    new count. Safe to call for non-trial users — it just increments the
    counter (which is ignored by effective_can_scan when status='active')."""
    data = load_license() or {}
    used = trial_scans_used(data) + 1
    data["trial_scans_used"] = used
    data["trial_scan_last_used_at"] = _now().isoformat()
    if used == 1:
        data.setdefault("trial_first_scan_at", data["trial_scan_last_used_at"])
    save_license(data)
    return used


def _trial_window_expired(license_data: dict[str, Any]) -> bool:
    ends_at = _parse_datetime(license_data.get("trial_ends_at"))
    if ends_at is None:
        return False
    return _now() >= ends_at


def trial_lock_reason(gate: dict[str, Any] | None = None) -> str:
    """Return why a trial user is blocked, or 'none' if not blocked.
    Values: 'none' | 'scan_quota' | 'expired' | 'no_license'"""
    data = gate if gate is not None else (load_license() or {})
    status = str(data.get("status") or "").strip().lower()
    if status == "active":
        return "none"
    if status not in {"trial", "expired", "read_only"}:
        return "no_license"
    if status in {"expired", "read_only"}:
        return "expired"
    if _trial_window_expired(data):
        return "expired"
    if trial_scans_used(data) >= TRIAL_SCAN_LIMIT:
        return "scan_quota"
    return "none"


def effective_can_scan(gate: dict[str, Any] | None = None) -> bool:
    """True only when the user is allowed to start a NEW scan right now."""
    data = gate if gate is not None else (load_license() or {})
    if not data.get("allowed"):
        return False
    status = str(data.get("status") or "").strip().lower()
    if status == "active":
        return True
    if status == "trial":
        return trial_lock_reason(data) == "none"
    return False


def effective_can_modify(gate: dict[str, Any] | None = None) -> bool:
    """True when the user can change Gmail state via FeeHunt rules
    (blacklist auto-apply, whitelist auto-protect, post-scan cleanup
    automation). Manual per-email actions on already-shown results stay
    open regardless — gate them at scan initiation, not action time."""
    return effective_can_scan(gate)
