from __future__ import annotations

import json
from typing import Any

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import GMAIL_CREDENTIALS_FILE, GMAIL_SCOPES, GMAIL_TOKEN_FILE, GMAIL_USER_ID


FULL_GMAIL_SCOPE = "https://mail.google.com/"


class GmailAuthError(RuntimeError):
    """Raised when Gmail OAuth cannot create a usable Gmail service."""


def clear_gmail_token() -> None:
    try:
        if GMAIL_TOKEN_FILE.exists():
            GMAIL_TOKEN_FILE.unlink()
    except Exception:
        pass


def _credentials_client_id() -> str:
    try:
        data = json.loads(GMAIL_CREDENTIALS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return ""
    installed = data.get("installed") or data.get("web") or {}
    return str(installed.get("client_id") or "")


def _token_data() -> dict[str, Any] | None:
    if not GMAIL_TOKEN_FILE.exists():
        return None
    try:
        data = json.loads(GMAIL_TOKEN_FILE.read_text(encoding="utf-8"))
    except Exception:
        clear_gmail_token()
        return None
    return data if isinstance(data, dict) else None


def _token_scopes(data: dict[str, Any]) -> set[str]:
    scopes = data.get("scopes") or data.get("scope") or []
    if isinstance(scopes, str):
        scopes = scopes.split()
    if not isinstance(scopes, list):
        return set()
    return {str(scope).strip() for scope in scopes if str(scope).strip()}


def _token_has_required_scopes(data: dict[str, Any]) -> bool:
    scopes = _token_scopes(data)
    if not scopes:
        return False
    if FULL_GMAIL_SCOPE in scopes:
        return True
    return set(GMAIL_SCOPES).issubset(scopes)


def _token_matches_credentials(data: dict[str, Any]) -> bool:
    expected_client_id = _credentials_client_id()
    token_client_id = str(data.get("client_id") or "")
    return not expected_client_id or not token_client_id or token_client_id == expected_client_id


def _load_existing_credentials() -> Credentials | None:
    data = _token_data()
    if not data:
        return None
    if not _token_matches_credentials(data) or not _token_has_required_scopes(data):
        clear_gmail_token()
        return None
    try:
        return Credentials.from_authorized_user_file(str(GMAIL_TOKEN_FILE), GMAIL_SCOPES)
    except Exception:
        clear_gmail_token()
        return None


def has_saved_gmail_connection() -> bool:
    data = _token_data()
    return bool(data and _token_matches_credentials(data) and _token_has_required_scopes(data))


def _save_credentials(creds: Credentials) -> None:
    GMAIL_TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    GMAIL_TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")


def _run_oauth_flow() -> Credentials:
    if not GMAIL_CREDENTIALS_FILE.exists():
        raise FileNotFoundError(f"credentials.json not found at {GMAIL_CREDENTIALS_FILE}")

    flow = InstalledAppFlow.from_client_secrets_file(str(GMAIL_CREDENTIALS_FILE), GMAIL_SCOPES)
    return flow.run_local_server(
        host="localhost",
        port=0,
        open_browser=True,
        authorization_prompt_message="Opening Google sign-in for FeeHunt...",
        success_message="FeeHunt is connected to Gmail. You can close this browser tab.",
        access_type="offline",
    )


def get_gmail_credentials(*, force_reauth: bool = False) -> Credentials:
    if force_reauth:
        clear_gmail_token()

    creds = _load_existing_credentials()
    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save_credentials(creds)
            return creds
        except RefreshError:
            clear_gmail_token()
            creds = None
        except Exception:
            clear_gmail_token()
            creds = None

    if not creds or not creds.valid:
        creds = _run_oauth_flow()
        _save_credentials(creds)

    return creds


def _format_http_error(error: HttpError) -> str:
    status = getattr(getattr(error, "resp", None), "status", "")
    raw = ""
    try:
        raw = error.content.decode("utf-8", errors="replace")
    except Exception:
        raw = str(error)
    lower = raw.lower()
    if status == 403 and ("accessnotconfigured" in lower or "service_disabled" in lower):
        return (
            "Gmail API is not enabled for the Google Cloud project used by FeeHunt. "
            "Enable Gmail API in Google Cloud Console, then reconnect Gmail."
        )
    if status == 403 and ("insufficient" in lower or "permission" in lower):
        clear_gmail_token()
        return (
            "The saved Gmail connection does not include the permissions FeeHunt needs. "
            "Reconnect Gmail and approve the requested access."
        )
    if status in (401, 403):
        clear_gmail_token()
        return "Google rejected the saved Gmail connection. Reconnect Gmail and approve access."
    return f"Gmail returned an error while checking the connection: {error}"


def validate_gmail_service(service: Any) -> dict[str, Any]:
    try:
        return service.users().getProfile(userId=GMAIL_USER_ID).execute()
    except HttpError as error:
        raise GmailAuthError(_format_http_error(error)) from error


def get_gmail_service(*, force_reauth: bool = False, validate: bool = True):
    creds = get_gmail_credentials(force_reauth=force_reauth)
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    if validate:
        validate_gmail_service(service)
    return service
