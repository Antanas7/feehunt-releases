from urllib.parse import urlparse

from config import GMAIL_USER_ID
from gmail_auth import get_gmail_service as get_authorized_gmail_service
from licensing import register_gmail_account


# ============================================================
# Gmail Service
# ============================================================

def get_gmail_service(*, force_reauth: bool = False):
    service = get_authorized_gmail_service(force_reauth=force_reauth)
    profile = service.users().getProfile(userId=GMAIL_USER_ID).execute()
    registration = register_gmail_account(profile.get("emailAddress", ""))
    if not registration.get("registered") and registration.get("status") == "plan_limit_exceeded":
        raise PermissionError(registration.get("message") or "FeeHunt plan limit reached.")
    return service


# ============================================================
# Internal helper
# ============================================================

def modify_message(message_id: str, body: dict) -> dict:
    service = get_gmail_service()
    return service.users().messages().modify(
        userId=GMAIL_USER_ID,
        id=message_id,
        body=body,
    ).execute()


# ============================================================
# Core Actions
# ============================================================

def archive_email(message_id: str) -> dict:
    return modify_message(message_id, {"removeLabelIds": ["INBOX"]})


def unarchive_email(message_id: str) -> dict:
    return modify_message(message_id, {"addLabelIds": ["INBOX"]})


def mark_as_important(message_id: str) -> dict:
    return modify_message(message_id, {"addLabelIds": ["IMPORTANT"]})


def remove_important(message_id: str) -> dict:
    return modify_message(message_id, {"removeLabelIds": ["IMPORTANT"]})


def mark_as_spam(message_id: str) -> dict:
    return modify_message(message_id, {"addLabelIds": ["SPAM"]})


def unmark_spam(message_id: str) -> dict:
    return modify_message(message_id, {"removeLabelIds": ["SPAM"], "addLabelIds": ["INBOX"]})


def mark_as_read(message_id: str) -> dict:
    return modify_message(message_id, {"removeLabelIds": ["UNREAD"]})


def mark_as_unread(message_id: str) -> dict:
    return modify_message(message_id, {"addLabelIds": ["UNREAD"]})


def star_email(message_id: str) -> dict:
    return modify_message(message_id, {"addLabelIds": ["STARRED"]})


def unstar_email(message_id: str) -> dict:
    return modify_message(message_id, {"removeLabelIds": ["STARRED"]})


def delete_email(message_id: str) -> dict:
    service = get_gmail_service()
    return service.users().messages().trash(
        userId=GMAIL_USER_ID,
        id=message_id,
    ).execute()


def delete_emails(message_ids: list[str]) -> dict:
    service = get_gmail_service()
    changed = []
    errors = []

    for message_id in message_ids:
        if not message_id:
            continue
        try:
            service.users().messages().trash(
                userId=GMAIL_USER_ID,
                id=message_id,
            ).execute()
            changed.append(message_id)
        except Exception as error:
            errors.append({"message_id": message_id, "error": str(error)})

    return {"changed": changed, "errors": errors}


def restore_trashed_email(message_id: str) -> dict:
    service = get_gmail_service()
    return service.users().messages().untrash(
        userId=GMAIL_USER_ID,
        id=message_id,
    ).execute()


# ============================================================
# Message Retrieval
# ============================================================

def get_message_metadata(message_id: str) -> dict:
    service = get_gmail_service()
    return service.users().messages().get(
        userId=GMAIL_USER_ID,
        id=message_id,
        format="metadata",
    ).execute()


def get_message_full(message_id: str) -> dict:
    service = get_gmail_service()
    return service.users().messages().get(
        userId=GMAIL_USER_ID,
        id=message_id,
        format="full",
    ).execute()


# ============================================================
# Unsubscribe Support
# ============================================================

DIRECT_BROWSER_UNFRIENDLY_UNSUBSCRIBE_HOSTS = {
    "unsubscribes.spmta.com",
    "mg.account.hostinger.com",
}


def is_direct_browser_unfriendly_unsubscribe_url(url: str | None) -> bool:
    if not url:
        return False

    parsed = urlparse(url)
    host = parsed.netloc.lower()
    return (
        host in DIRECT_BROWSER_UNFRIENDLY_UNSUBSCRIBE_HOSTS
        or host.endswith(".spmta.com")
        or (host.startswith("mg.") and "hostinger" in host)
    )


def extract_unsubscribe_url(header_value: str) -> str | None:
    if not header_value:
        return None

    parts = [part.strip() for part in header_value.split(",")]

    for part in parts:
        if part.startswith("<") and part.endswith(">"):
            candidate = part[1:-1].strip()
            if candidate.startswith(("http://", "https://")):
                parsed = urlparse(candidate)
                if parsed.scheme in ("http", "https") and parsed.netloc:
                    return candidate

    return None


def get_unsubscribe_link(message_id: str, *, include_browser_unfriendly: bool = False) -> str | None:
    service = get_gmail_service()

    message = service.users().messages().get(
        userId=GMAIL_USER_ID,
        id=message_id,
        format="metadata",
        metadataHeaders=["List-Unsubscribe"],
    ).execute()

    headers = message.get("payload", {}).get("headers", [])

    for header in headers:
        if header.get("name", "").lower() == "list-unsubscribe":
            unsubscribe_url = extract_unsubscribe_url(header.get("value", ""))
            if (
                unsubscribe_url
                and not include_browser_unfriendly
                and is_direct_browser_unfriendly_unsubscribe_url(unsubscribe_url)
            ):
                return None
            return unsubscribe_url

    return None


def has_unsubscribe_link(message_id: str) -> bool:
    return get_unsubscribe_link(message_id) is not None

