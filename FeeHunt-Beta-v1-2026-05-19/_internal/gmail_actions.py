from pathlib import Path
from urllib.parse import urlparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import (
    GMAIL_SCOPES,
    GMAIL_CREDENTIALS_FILE,
    GMAIL_TOKEN_FILE,
    GMAIL_USER_ID,
)
from translations import t


CREDENTIALS_PATH = GMAIL_CREDENTIALS_FILE
TOKEN_PATH = GMAIL_TOKEN_FILE


# ============================================================
# Gmail Service
# ============================================================

def get_gmail_service():
    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            t("gmail.credentials_missing").format(path=CREDENTIALS_PATH)
        )

    creds = None

    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(
                str(TOKEN_PATH), GMAIL_SCOPES
            )
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), GMAIL_SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds, cache_discovery=False)


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


def permanently_delete_email(message_id: str) -> dict:
    service = get_gmail_service()
    return service.users().messages().delete(
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


def get_unsubscribe_link(message_id: str) -> str | None:
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
            return extract_unsubscribe_url(header.get("value", ""))

    return None


def has_unsubscribe_link(message_id: str) -> bool:
    return get_unsubscribe_link(message_id) is not None

