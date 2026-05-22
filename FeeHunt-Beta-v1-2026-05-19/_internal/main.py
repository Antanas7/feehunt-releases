import base64
import json
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
    MAX_EMAILS_TO_SCAN,
    DEFAULT_ESTIMATED_SAVINGS_PER_SUBSCRIPTION,
)

from feehunt_analyzer import analyze_email


RESULTS_FILE = APP_DIR / "last_scan_results.json"


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
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


# ============================================================
# Gmail auth
# ============================================================

def get_gmail_service():
    credentials_path = GMAIL_CREDENTIALS_FILE
    token_path = GMAIL_TOKEN_FILE

    if not credentials_path.exists():
        raise FileNotFoundError(f"Nerastas Gmail OAuth failas: {credentials_path}")

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

        with open(token_path, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds, cache_discovery=False)


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

            print(
                f"PROGRESS:{index}/{total}:{subject[:60] if subject else '(be temos)'}",
                flush=True,
            )

        except Exception as error:
            print(f"Klaida apdorojant laišką {message.get('id', 'unknown')}: {error}")

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
    print(f"{APP_NAME} {APP_VERSION}")
    print(f"Darbinis katalogas: {APP_DIR}")
    print("Pradedamas Gmail skenavimas...")

    try:
        scan_result = scan_gmail()
        save_scan_results(scan_result)

        print(f"FeeHunt Gmail skenavimas baigtas.")
        print(f"Rasta {scan_result['subscriptions_found']} prenumeratų / grėsmių.")
        print(f"Rasta {scan_result['promotions_found']} reklaminių / parduotuvių / naujienlaiškių.")
        print(f"Galimas sutaupymas: ${scan_result['estimated_savings']}")
        print(f"Rezultatai: {RESULTS_FILE}")

    except Exception as error:
        print(f"Kritinė klaida: {error}")
        raise


if __name__ == "__main__":
    main()
