from __future__ import annotations

import json
import re
from typing import Any

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import GMAIL_CREDENTIALS_FILE, GMAIL_SCOPES, GMAIL_TOKEN_FILE, GMAIL_USER_ID
import secure_store


FULL_GMAIL_SCOPE = "https://mail.google.com/"

# Plain-text file holding the email address of the Gmail account the current
# token belongs to. Cached next to the token so the UI can show which account
# is being processed without making a network getProfile call on every render.
GMAIL_EMAIL_FILE = GMAIL_TOKEN_FILE.parent / "connected_email.txt"

# Per-account token archive. The active account always lives in GMAIL_TOKEN_FILE
# (so the rest of the app keeps working unchanged); here we keep a copy of every
# account that has been connected, keyed by email, so the user can switch
# between them instantly without signing in to Google again. ACCOUNTS_INDEX_FILE
# records the known emails (and their order) since token files don't carry one.
ACCOUNTS_DIR = GMAIL_TOKEN_FILE.parent / "accounts"
ACCOUNTS_INDEX_FILE = ACCOUNTS_DIR / "index.json"


class GmailAuthError(RuntimeError):
    """Raised when Gmail OAuth cannot create a usable Gmail service."""


def _account_filename(email: str) -> str:
    safe = re.sub(r"[^a-z0-9]+", "_", str(email or "").strip().lower()).strip("_")
    return f"{safe or 'account'}.json"


def _read_accounts_index() -> list[str]:
    try:
        data = json.loads(ACCOUNTS_INDEX_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(data, list):
        return []
    result: list[str] = []
    for item in data:
        email = str(item or "").strip().lower()
        if email and email not in result:
            result.append(email)
    return result


def _write_accounts_index(emails: list[str]) -> None:
    cleaned: list[str] = []
    for item in emails:
        email = str(item or "").strip().lower()
        if email and email not in cleaned:
            cleaned.append(email)
    try:
        ACCOUNTS_DIR.mkdir(parents=True, exist_ok=True)
        ACCOUNTS_INDEX_FILE.write_text(json.dumps(cleaned), encoding="utf-8")
    except Exception:
        pass


def save_account_token(email: str) -> None:
    """Archive the currently active token under ``email`` so the account can be
    switched back to later without a fresh Google sign-in. Idempotent: safe to
    call on every Gmail service request — it simply refreshes the archived copy."""
    address = str(email or "").strip().lower()
    if not address or not GMAIL_TOKEN_FILE.exists():
        return
    try:
        ACCOUNTS_DIR.mkdir(parents=True, exist_ok=True)
        # Copy the encrypted token bytes verbatim — same Windows user, so the
        # DPAPI ciphertext stays decryptable. Archived tokens are encrypted too.
        token_bytes = GMAIL_TOKEN_FILE.read_bytes()
        (ACCOUNTS_DIR / _account_filename(address)).write_bytes(token_bytes)
    except Exception:
        return
    index = _read_accounts_index()
    if address not in index:
        index.append(address)
    _write_accounts_index(index)


def list_saved_accounts() -> list[str]:
    """Emails that have an archived token available for instant switching."""
    return [
        email
        for email in _read_accounts_index()
        if (ACCOUNTS_DIR / _account_filename(email)).exists()
    ]


def switch_account(email: str) -> bool:
    """Make ``email`` the active Gmail account by restoring its archived token.
    Returns False when no archived token exists (the caller should then fall
    back to a fresh Google sign-in)."""
    address = str(email or "").strip().lower()
    if not address:
        return False
    token_path = ACCOUNTS_DIR / _account_filename(address)
    if not token_path.exists():
        return False
    try:
        GMAIL_TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        # Restore the archived encrypted token bytes verbatim (see save_account_token).
        tmp_path = GMAIL_TOKEN_FILE.with_suffix(GMAIL_TOKEN_FILE.suffix + ".tmp")
        tmp_path.write_bytes(token_path.read_bytes())
        tmp_path.replace(GMAIL_TOKEN_FILE)
    except Exception:
        return False
    save_connected_email(address)
    return True


def remove_saved_account(email: str) -> None:
    """Forget an archived account. If it was the active one, the active token is
    cleared too so the app no longer treats it as connected."""
    address = str(email or "").strip().lower()
    if not address:
        return
    try:
        (ACCOUNTS_DIR / _account_filename(address)).unlink()
    except FileNotFoundError:
        pass
    except Exception:
        pass
    _write_accounts_index([e for e in _read_accounts_index() if e != address])
    if get_connected_email().strip().lower() == address:
        clear_gmail_token()


def save_connected_email(email: str) -> None:
    address = str(email or "").strip()
    if not address:
        return
    try:
        GMAIL_EMAIL_FILE.parent.mkdir(parents=True, exist_ok=True)
        GMAIL_EMAIL_FILE.write_text(address, encoding="utf-8")
    except Exception:
        pass


def get_connected_email() -> str:
    if not GMAIL_TOKEN_FILE.exists():
        return ""
    try:
        return GMAIL_EMAIL_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def ensure_connected_email() -> str:
    """If a Gmail token is connected but its email was never cached (e.g. the
    account was connected by an older FeeHunt version, before connected_email.txt),
    fetch it once via getProfile and cache it so the UI can name the active inbox
    and tester-mode can recognise it. Never launches an interactive sign-in: if the
    token can't be refreshed silently it just returns ''. Returns the email or ''."""
    cached = get_connected_email()
    if cached:
        return cached
    creds = _load_existing_credentials()
    if not creds:
        return ""
    try:
        if not creds.valid and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            _save_credentials(creds)
        if not creds.valid:
            return ""
        service = build("gmail", "v1", credentials=creds, cache_discovery=False)
        profile = service.users().getProfile(userId=GMAIL_USER_ID).execute()
        email = str(profile.get("emailAddress") or "").strip()
    except Exception:
        return ""
    if email:
        save_connected_email(email)
        save_account_token(email)  # also register it for the account switcher
    return email


def clear_gmail_token() -> None:
    try:
        if GMAIL_TOKEN_FILE.exists():
            GMAIL_TOKEN_FILE.unlink()
    except Exception:
        pass
    try:
        if GMAIL_EMAIL_FILE.exists():
            GMAIL_EMAIL_FILE.unlink()
    except Exception:
        pass


def clear_all_saved_accounts() -> None:
    """Forget every Gmail account saved on this Windows profile.

    Use this when a different FeeHunt license holder signs in on the same
    computer. Switching Gmail accounts inside one Family plan keeps using the
    archive above; switching license holders must not inherit those tokens.
    """
    clear_gmail_token()
    try:
        if ACCOUNTS_DIR.exists():
            for path in ACCOUNTS_DIR.iterdir():
                if path.is_file():
                    path.unlink()
            ACCOUNTS_DIR.rmdir()
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
        data = json.loads(secure_store.unseal(GMAIL_TOKEN_FILE.read_bytes()))
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
        # Build from the already-decrypted token dict (the file on disk is
        # DPAPI-encrypted, so from_authorized_user_file can't read it directly).
        return Credentials.from_authorized_user_info(data, GMAIL_SCOPES)
    except Exception:
        clear_gmail_token()
        return None


def has_saved_gmail_connection() -> bool:
    data = _token_data()
    return bool(data and _token_matches_credentials(data) and _token_has_required_scopes(data))


def _save_credentials(creds: Credentials) -> None:
    # Encrypt the token at rest with DPAPI (per Windows user) and write
    # atomically (temp + replace), so a reader never sees a half-written file
    # and the access/refresh tokens never sit on disk as plain text.
    GMAIL_TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = GMAIL_TOKEN_FILE.with_suffix(GMAIL_TOKEN_FILE.suffix + ".tmp")
    tmp_path.write_bytes(secure_store.seal(creds.to_json()))
    tmp_path.replace(GMAIL_TOKEN_FILE)


def _run_oauth_flow() -> Credentials:
    if not GMAIL_CREDENTIALS_FILE.exists():
        raise FileNotFoundError(f"credentials.json not found at {GMAIL_CREDENTIALS_FILE}")

    flow = InstalledAppFlow.from_client_secrets_file(str(GMAIL_CREDENTIALS_FILE), GMAIL_SCOPES)
    try:
        creds = flow.run_local_server(
            host="localhost",
            port=0,
            open_browser=True,
            authorization_prompt_message="Opening Google sign-in for FeeHunt...",
            success_message="FeeHunt is connected to Gmail. You can close this browser tab.",
            access_type="offline",
            # Always show the Google account chooser. Without this, if the browser
            # is already signed in to one Google account, OAuth silently picks it —
            # so a user trying to connect a different inbox (e.g. a spouse's) could
            # end up connecting the wrong account without realising it.
            prompt="select_account consent",
            # Don't wait forever. If the user closes the Google window without
            # finishing, this would otherwise block the whole app indefinitely.
            timeout_seconds=300,
        )
    except GmailAuthError:
        raise
    except Exception as exc:
        # Closed sign-in window, timeout, or the local callback port was blocked.
        # Surface a clear, recoverable message instead of a hang or raw traceback.
        raise GmailAuthError(
            "oauth_not_completed: Google sign-in was not completed. "
            "Open Connect Gmail again and finish signing in."
        ) from exc
    if not creds:
        raise GmailAuthError(
            "oauth_not_completed: Google sign-in was not completed. "
            "Open Connect Gmail again and finish signing in."
        )
    return creds


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
