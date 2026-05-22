import base64
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import (
    APP_DIR,
    APP_NAME,
    APP_VERSION,
    GMAIL_SCOPES,
    GMAIL_CREDENTIALS_FILE,
    GMAIL_TOKEN_FILE,
    LAST_SCAN_RESULTS_FILE,
    USER_DATA_DIR,
    MAX_EMAILS_TO_SCAN,
    DEFAULT_ESTIMATED_SAVINGS_PER_SUBSCRIPTION,
)

from feehunt_analyzer import analyze_email
from licensing import register_gmail_account


RESULTS_FILE = LAST_SCAN_RESULTS_FILE


# ============================================================
# Windows-safe console output
# ============================================================

def configure_console_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def safe_text(value: Any) -> str:
    text = str(value).encode("utf-8", errors="replace").decode("utf-8", errors="replace")
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")


def safe_print(value: Any = "", *, flush: bool = False) -> None:
    try:
        sys.stdout.write(safe_text(value) + "\n")
        if flush:
            sys.stdout.flush()
    except Exception:
        pass


configure_console_encoding()


# ============================================================
# Gmail helpers
# ============================================================

def decode_body(data: str | None) -> str:
    if not data:
        return ""
    try:
        decoded_bytes = base64.urlsafe_b64decode(data + "===")
        return decoded_bytes.decode("utf-8", errors="replace")
    except Exception:
        return ""


def extract_text_from_payload(payload: dict | None) -> str:
    if not payload:
        return ""
    text_parts: list[str] = []

    def process_part(part: dict) -> None:
        body = part.get("body", {})
        data = body.get("data")
        if data:
            text_parts.append(decode_body(data))
        for nested_part in part.get("parts", []):
            process_part(nested_part)

    process_part(payload)
    return "\n".join(part for part in text_parts if part)


def get_header(headers: list[dict], name: str) -> str:
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")
    return ""


def save_scan_results(data: dict[str, Any]) -> None:
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def format_critical_error(error: Exception) -> str:
    if isinstance(error, FileNotFoundError) and "credentials.json" in str(error):
        return (
            "What is wrong: FeeHunt cannot find its bundled Gmail OAuth client file (credentials.json).\n"
            "Why it matters: Google sign-in cannot start without this app configuration file.\n"
            "How to fix it: download the official FeeHunt Beta v1.1 ZIP again, extract the whole ZIP, "
            "and run FeeHunt.exe from the extracted FeeHunt folder."
        )

    return (
        f"What is wrong: {error}\n"
        "Why it matters: FeeHunt could not complete the Gmail connection or scan.\n"
        "How to fix it: check your internet connection, close any old FeeHunt windows, "
        "then open FeeHunt.exe and try Connect Gmail again."
    )


# ============================================================
# Gmail auth
# ============================================================

def get_gmail_service():
    credentials_path = GMAIL_CREDENTIALS_FILE
    token_path = GMAIL_TOKEN_FILE

    if not credentials_path.exists():
        raise FileNotFoundError(f"credentials.json not found at {credentials_path}")

    creds = None
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), GMAIL_SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)

        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    try:
        profile = service.users().getProfile(userId="me").execute()
        registration = register_gmail_account(profile.get("emailAddress", ""))
        if not registration.get("registered") and registration.get("status") == "plan_limit_exceeded":
            raise PermissionError(registration.get("message") or "FeeHunt plan limit reached.")
    except PermissionError:
        raise
    except Exception:
        pass
    return service


# ============================================================
# Skenavimas
# ============================================================

def scan_gmail() -> dict[str, Any]:
    service = get_gmail_service()

    response = service.users().messages().list(
        userId="me",
        maxResults=MAX_EMAILS_TO_SCAN,
    ).execute()

    messages = response.get("messages", [])
    total = len(messages)

    financial_risks = []
    subscriptions = []
    promotional_emails = []
    shop_emails = []
    newsletter_emails = []

    for index, message in enumerate(messages, start=1):
        try:
            msg = service.users().messages().get(
                userId="me",
                id=message["id"],
                format="full",
            ).execute()

            payload = msg.get("payload", {})
            headers = payload.get("headers", [])

            subject = get_header(headers, "Subject")
            sender = get_header(headers, "From")
            date = get_header(headers, "Date")
            snippet = msg.get("snippet", "")
            body = extract_text_from_payload(payload)
            content = f"{subject}\n{sender}\n{snippet}\n{body}"

            analysis = analyze_email(content)

            email_data = {
                "message_id": msg["id"],
                "subject": subject,
                "sender": sender,
                "date": date,
                "snippet": snippet,
                "categories": analysis["categories"],
                "matched_keywords": analysis["matched_keywords"],
            }

            if analysis["is_financial_risk"]:
                financial_risks.append(email_data)
            if analysis["is_subscription"]:
                subscriptions.append(email_data)
            if analysis["is_promotional"]:
                promotional_emails.append(email_data)
            if analysis["is_shop"]:
                shop_emails.append(email_data)
            if analysis["is_newsletter"]:
                newsletter_emails.append(email_data)

            safe_print(
                f"PROGRESS:{index}/{total}:{subject[:60] if subject else '(be temos)'}",
                flush=True,
            )

        except Exception as error:
            safe_print(f"Klaida apdorojant laišką {message.get('id', 'unknown')}: {error}")

    subscription_count = len(subscriptions)
    promo_count = len(promotional_emails) + len(shop_emails) + len(newsletter_emails)
    estimated_savings = subscription_count * DEFAULT_ESTIMATED_SAVINGS_PER_SUBSCRIPTION

    return {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "last_scan_at": datetime.now().isoformat(timespec="seconds"),
        "emails_scanned": total,
        "subscriptions_found": subscription_count,
        "promotions_found": promo_count,
        "estimated_savings": estimated_savings,
        "financial_risks": financial_risks,
        "subscriptions": subscriptions,
        "promotional_emails": promotional_emails,
        "shop_emails": shop_emails,
        "newsletter_emails": newsletter_emails,
    }


# ============================================================
# Main
# ============================================================

def main() -> None:
    safe_print(f"{APP_NAME} {APP_VERSION}")
    safe_print(f"Darbinis katalogas: {APP_DIR}")
    safe_print(f"Vartotojo duomenys: {USER_DATA_DIR}")
    safe_print("Pradedamas Gmail skenavimas...")

    try:
        scan_result = scan_gmail()
        save_scan_results(scan_result)

        safe_print("FeeHunt Gmail skenavimas baigtas.")
        safe_print(f"Rasta {scan_result['subscriptions_found']} prenumeratų / grėsmių.")
        safe_print(f"Rasta {scan_result['promotions_found']} reklaminių / parduotuvių / naujienlaiškių.")
        safe_print(f"Galimas sutaupymas: ${scan_result['estimated_savings']}")
        safe_print(f"Rezultatai: {RESULTS_FILE}")

    except Exception as error:
        safe_print(format_critical_error(error))
        raise


if __name__ == "__main__":
    main()
