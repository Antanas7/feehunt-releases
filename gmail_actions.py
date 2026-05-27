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


def _extract_blacklist_query_target(entry: str) -> str:
    """Pick the most specific Gmail-searchable substring from a blacklist
    rule. Users add entries in mixed shapes: 'Name <email@host>', bare
    'email@host', a domain like 'canva.com', or just a display name like
    'Hostinger'. For 'Name <email>' shape, pulling the email gives a far
    more precise Gmail query than the full display string.
    """
    if not entry:
        return ""
    text = entry.strip()
    if "<" in text and ">" in text:
        start = text.index("<") + 1
        end = text.index(">", start)
        candidate = text[start:end].strip()
        if candidate:
            return candidate
    return text


def apply_blacklist_to_gmail_directly(
    senders: list[str],
    *,
    dry_run: bool = False,
    max_per_sender: int = 500,
) -> dict:
    """Search Gmail directly for messages whose `From` matches each blacklist
    entry and trash them. Independent of the keyword-based scan, so a Canva
    "Welcome" email with no subscription/promo keywords still gets caught
    when the user has `canva.com` on their unwanted-senders list.

    The blacklist rule itself is never mutated — only Gmail messages move.

    Returns:
      {
        "senders_searched": int,
        "messages_trashed": int,
        "by_sender": {rule_entry: [{"message_id", "sender_rule"}, ...]},
        "errors": [{"sender", "error"} or {"sender", "message_id", "error"}],
        "dry_run": bool,
      }
    """
    summary = {
        "senders_searched": 0,
        "messages_trashed": 0,
        "by_sender": {},
        "errors": [],
        "dry_run": dry_run,
    }
    if not senders:
        return summary

    service = get_gmail_service()

    for sender in senders:
        summary["senders_searched"] += 1
        target = _extract_blacklist_query_target(sender)
        if not target:
            continue
        # Always quote — handles display-name entries with spaces or
        # punctuation ('Lucia (UptimeRobot)'). Gmail accepts quoted emails
        # and domains too.
        query = f'from:"{target}"'

        message_ids: list[str] = []
        try:
            page_token = None
            while len(message_ids) < max_per_sender:
                request = {
                    "userId": GMAIL_USER_ID,
                    "q": query,
                    "maxResults": min(100, max_per_sender - len(message_ids)),
                }
                if page_token:
                    request["pageToken"] = page_token
                response = service.users().messages().list(**request).execute()
                for msg in response.get("messages", []) or []:
                    message_ids.append(msg["id"])
                page_token = response.get("nextPageToken")
                if not page_token:
                    break
        except Exception as error:
            summary["errors"].append({"sender": sender, "error": str(error)})
            summary["by_sender"][sender] = []
            continue

        trashed_for_sender = []
        if dry_run:
            trashed_for_sender = [
                {"message_id": mid, "sender_rule": sender} for mid in message_ids
            ]
        else:
            for mid in message_ids:
                try:
                    service.users().messages().trash(
                        userId=GMAIL_USER_ID,
                        id=mid,
                    ).execute()
                    trashed_for_sender.append({"message_id": mid, "sender_rule": sender})
                except Exception as error:
                    summary["errors"].append(
                        {"sender": sender, "message_id": mid, "error": str(error)}
                    )

        summary["by_sender"][sender] = trashed_for_sender
        summary["messages_trashed"] += len(trashed_for_sender)

    return summary


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

