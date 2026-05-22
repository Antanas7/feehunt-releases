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
}


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
