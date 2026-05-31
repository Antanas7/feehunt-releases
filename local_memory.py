"""Transparent local-only memory for FeeHunt progress."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from config import MEMORY_FILE


DEFAULT_MEMORY = {
    "version": 1,
    "scan_history": [],
    "progress": {
        "scans_completed": 0,
        "promotions_archived": 0,
        "last_user_state": "new",
        "last_seen_at": None,
        "last_visit_at": None,
        "previous_visit_at": None,
    },
    # Per-service cancellation status, keyed by a stable service identity (NOT the
    # message id) so a "cancelled" mark survives next month's billing email and
    # app restarts. The control center reads/writes this. See subscription_status
    # helpers below.
    "subscription_status": {},
}

# The only statuses a subscription can hold. Absence of a key means "pending".
SUBSCRIPTION_STATUSES = ("cancelled", "needs_you", "keeping")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_memory() -> dict[str, Any]:
    if not MEMORY_FILE.exists():
        return json.loads(json.dumps(DEFAULT_MEMORY))
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception:
        return json.loads(json.dumps(DEFAULT_MEMORY))
    if not isinstance(data, dict):
        return json.loads(json.dumps(DEFAULT_MEMORY))
    memory = json.loads(json.dumps(DEFAULT_MEMORY))
    memory.update(data)
    memory["progress"] = {**DEFAULT_MEMORY["progress"], **data.get("progress", {})}
    if not isinstance(memory.get("scan_history"), list):
        memory["scan_history"] = []
    if not isinstance(memory.get("subscription_status"), dict):
        memory["subscription_status"] = {}
    return memory


def save_memory(memory: dict[str, Any]) -> bool:
    try:
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(memory, file, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def clear_memory() -> bool:
    try:
        if MEMORY_FILE.exists():
            MEMORY_FILE.unlink()
        return True
    except Exception:
        return False


def remember_scan(scan_data: dict[str, Any] | None, user_state: str) -> bool:
    if not scan_data:
        return False
    memory = load_memory()
    history_item = {
        "saved_at": _now_iso(),
        "subscriptions": scan_data.get("subscriptions_found", len(scan_data.get("subscriptions", []) or [])),
        "promotions": scan_data.get("promotions_found", 0),
        "financial_risks": len(scan_data.get("financial_risks", []) or []),
        "estimated_savings": scan_data.get("estimated_savings", "$0"),
        "user_state": user_state,
    }
    memory["scan_history"] = (memory.get("scan_history", []) + [history_item])[-30:]
    memory["progress"]["scans_completed"] = int(memory["progress"].get("scans_completed") or 0) + 1
    memory["progress"]["last_user_state"] = user_state
    memory["progress"]["last_seen_at"] = _now_iso()
    return save_memory(memory)


def remember_visit(user_state: str | None = None) -> bool:
    memory = load_memory()
    current_visit = memory["progress"].get("last_visit_at")
    memory["progress"]["previous_visit_at"] = current_visit
    memory["progress"]["last_visit_at"] = _now_iso()
    if user_state:
        memory["progress"]["last_user_state"] = user_state
    return save_memory(memory)


def remember_archived_promotions(count: int) -> bool:
    if count <= 0:
        return False
    memory = load_memory()
    memory["progress"]["promotions_archived"] = int(memory["progress"].get("promotions_archived") or 0) + count
    return save_memory(memory)


# ============================================================
# Subscription cancellation status (control center)
# ============================================================
#
# FeeHunt never cancels for the user, so the only thing it can record is what the
# user TELLS it: "I cancelled", "I need to come back", or "I'm keeping this". The
# store is keyed by a stable per-service identity so the mark outlives the next
# billing email. `marked_message_id` is kept so the control center can warn when a
# NEW charge email arrives for something the user already marked cancelled.


def load_subscription_status() -> dict[str, Any]:
    """All recorded per-service cancellation statuses, keyed by service identity."""
    statuses = load_memory().get("subscription_status")
    return statuses if isinstance(statuses, dict) else {}


def get_subscription_status(service_key: str) -> dict[str, Any] | None:
    """The recorded status entry for one service, or None if never marked
    (i.e. still 'pending'). Entry shape: {status, service_name, updated_at,
    marked_message_id}."""
    if not service_key:
        return None
    entry = load_subscription_status().get(service_key)
    return entry if isinstance(entry, dict) else None


def set_subscription_status(service_key: str, status: str,
                            service_name: str = "",
                            message_id: str | None = None) -> bool:
    """Record the user's own decision for a service. `status` must be one of
    SUBSCRIPTION_STATUSES; anything else clears the mark back to pending."""
    if not service_key:
        return False
    memory = load_memory()
    store = memory.get("subscription_status")
    if not isinstance(store, dict):
        store = {}
    if status not in SUBSCRIPTION_STATUSES:
        store.pop(service_key, None)
    else:
        store[service_key] = {
            "status": status,
            "service_name": service_name or service_key,
            "updated_at": _now_iso(),
            "marked_message_id": message_id,
        }
    memory["subscription_status"] = store
    return save_memory(memory)


def clear_subscription_status(service_key: str) -> bool:
    """Forget a service's mark, returning it to pending."""
    if not service_key:
        return False
    memory = load_memory()
    store = memory.get("subscription_status")
    if not isinstance(store, dict) or service_key not in store:
        return False
    store.pop(service_key, None)
    memory["subscription_status"] = store
    return save_memory(memory)
