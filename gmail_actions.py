from urllib.parse import urlparse

from config import GMAIL_USER_ID
from gmail_auth import (
    get_gmail_service as get_authorized_gmail_service,
    save_connected_email,
    save_account_token,
)
from licensing import register_gmail_account


# ============================================================
# Gmail Service
# ============================================================

def get_gmail_service(*, force_reauth: bool = False):
    service = get_authorized_gmail_service(force_reauth=force_reauth)
    profile = service.users().getProfile(userId=GMAIL_USER_ID).execute()
    email_address = profile.get("emailAddress", "")
    save_connected_email(email_address)
    save_account_token(email_address)
    registration = register_gmail_account(email_address)
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
    """Single best target, kept for compatibility. New code uses
    _expand_blacklist_query_targets() which returns several variants so
    senders that rotate subdomains (Pinterest, Hostinger, Klaviyo-style
    ESP setups) get caught even when the user added only one address.
    """
    targets = _expand_blacklist_query_targets(entry)
    return targets[0] if targets else ""


def _expand_blacklist_query_targets(entry: str) -> list[str]:
    """Return one or more Gmail query targets for a single blacklist entry.

    Real example: a user adds 'Pinterest <recommendations@inspire.pinterest.com>'
    expecting all Pinterest emails to be matched, but Pinterest rotates
    between `inspire.`, `explore.`, `discover.`, and `ideas.` subdomains.
    Searching only `from:"recommendations@inspire.pinterest.com"` misses
    three quarters of their mail. So when the entry contains an email,
    also try the registrable parent domain.

    Returns at most three targets, in order of specificity:
      [exact sender, full host, registrable domain]
    Duplicates are removed; bare display names pass through unchanged.
    """
    if not entry:
        return []
    text = entry.strip()

    # Pull email out of 'Name <email@host>' if present.
    email_value = ""
    if "<" in text and ">" in text:
        start = text.index("<") + 1
        end = text.index(">", start)
        candidate = text[start:end].strip()
        if candidate:
            email_value = candidate
    elif "@" in text and " " not in text:
        # Bare 'user@host' entry.
        email_value = text

    targets: list[str] = []

    if email_value:
        targets.append(email_value)
        host = email_value.split("@", 1)[1] if "@" in email_value else email_value
        host = host.strip().lower()
        if host and host not in targets:
            targets.append(host)
        registrable = _registrable_domain(host)
        if registrable and registrable not in targets:
            targets.append(registrable)
    else:
        # Bare domain like 'canva.com' or 'mail.canva.com'.
        if "." in text and " " not in text:
            host = text.lower()
            targets.append(host)
            registrable = _registrable_domain(host)
            if registrable and registrable not in targets:
                targets.append(registrable)
        else:
            # Display name like 'Hostinger' or 'Lucia (UptimeRobot)' —
            # nothing to expand. Gmail will fuzzy-match the display name.
            targets.append(text)

    return targets


def _registrable_domain(host: str) -> str:
    """Best-effort registrable domain extraction without a full PSL.
    For 'inspire.pinterest.com' returns 'pinterest.com'.
    For 'pinterest.com' returns 'pinterest.com'.
    For 'mail.amazon.co.uk' returns 'amazon.co.uk' (handles the common
    two-label public suffixes).
    """
    if not host or "." not in host:
        return ""
    host = host.strip().lower().strip(".")
    labels = host.split(".")
    # Two-label public suffixes we want to keep intact when forming the
    # registrable domain. Not exhaustive — but covers the realistic cases
    # FeeHunt users will hit.
    two_label_suffixes = {
        "co.uk", "co.jp", "co.nz", "co.za", "com.au", "com.br", "com.mx",
        "com.tr", "com.sg", "com.hk", "com.tw", "com.cn", "co.kr", "ne.jp",
        "or.jp", "ac.uk", "gov.uk", "org.uk", "co.in",
    }
    if len(labels) >= 3:
        last_two = ".".join(labels[-2:])
        if last_two in two_label_suffixes:
            return ".".join(labels[-3:])
    if len(labels) >= 2:
        return ".".join(labels[-2:])
    return host


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
        targets = _expand_blacklist_query_targets(sender)
        if not targets:
            continue

        # Iterate every target variant; collect unique message ids across
        # them. This is what catches Pinterest's 4 sub-domains when the
        # user only added one specific address.
        message_ids: list[str] = []
        seen_ids: set[str] = set()
        had_error = False
        for target in targets:
            query = f'from:{target}' if ("@" in target or "." in target) and " " not in target else f'from:"{target}"'
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
                        mid = msg["id"]
                        if mid not in seen_ids:
                            seen_ids.add(mid)
                            message_ids.append(mid)
                    page_token = response.get("nextPageToken")
                    if not page_token:
                        break
            except Exception as error:
                summary["errors"].append({"sender": sender, "target": target, "error": str(error)})
                had_error = True
        if had_error and not message_ids:
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

