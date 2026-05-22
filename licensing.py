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


DEFAULT_TRIAL_DAYS = 14
OFFLINE_GRACE_DAYS = 7
LICENSE_KEY_PREFIX = "FHUNT-"


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
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
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
        return {"ok": False, "offline": False, "error": data.get("error") or f"HTTP {exc.code}"}
    except Exception as exc:
        return {"ok": False, "offline": True, "error": str(exc)}

    try:
        data = json.loads(text)
    except Exception:
        return {"ok": False, "offline": False, "error": "FeeHunt server returned unreadable data."}
    return data if isinstance(data, dict) else {"ok": False, "error": "FeeHunt server returned invalid data."}


def load_license() -> dict[str, Any] | None:
    return _read_json(LICENSE_FILE)


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
