import base64
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from config import (
    APP_DIR,
    APP_NAME,
    APP_VERSION,
    LAST_SCAN_RESULTS_FILE,
    USER_DATA_DIR,
    MAX_EMAILS_TO_SCAN,
    MAX_EMAILS_PER_TARGETED_QUERY,
    GMAIL_TARGETED_SCAN_QUERIES,
    DEFAULT_ESTIMATED_SAVINGS_PER_SUBSCRIPTION,
)

from feehunt_analyzer import analyze_email
from phishing_detector import analyze_phishing
from gmail_auth import get_gmail_service as get_authorized_gmail_service
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


def extract_html_from_payload(payload: dict | None) -> str:
    if not payload:
        return ""
    html_parts: list[str] = []

    def process_part(part: dict) -> None:
        if part.get("mimeType", "").lower() == "text/html":
            data = part.get("body", {}).get("data")
            if data:
                html_parts.append(decode_body(data))
        for nested_part in part.get("parts", []):
            process_part(nested_part)

    process_part(payload)
    return "\n".join(part for part in html_parts if part)


def get_header(headers: list[dict], name: str) -> str:
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")
    return ""


def save_scan_results(data: dict[str, Any]) -> None:
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def list_messages(service, *, query: str | None = None, limit: int = MAX_EMAILS_TO_SCAN) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    page_token = None

    while len(messages) < limit:
        request = {
            "userId": "me",
            "maxResults": min(100, limit - len(messages)),
        }
        if query:
            request["q"] = query
        if page_token:
            request["pageToken"] = page_token

        response = service.users().messages().list(**request).execute()
        messages.extend(response.get("messages", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return messages


def collect_scan_messages(service) -> list[dict[str, str]]:
    seen_ids: set[str] = set()
    collected: list[dict[str, str]] = []

    for message in list_messages(service, limit=MAX_EMAILS_TO_SCAN):
        message_id = message.get("id")
        if message_id and message_id not in seen_ids:
            seen_ids.add(message_id)
            collected.append(message)

    for query in GMAIL_TARGETED_SCAN_QUERIES:
        for message in list_messages(service, query=query, limit=MAX_EMAILS_PER_TARGETED_QUERY):
            message_id = message.get("id")
            if message_id and message_id not in seen_ids:
                seen_ids.add(message_id)
                collected.append(message)

    return collected


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
    service = get_authorized_gmail_service()
    profile = service.users().getProfile(userId="me").execute()
    registration = register_gmail_account(profile.get("emailAddress", ""))
    if not registration.get("registered") and registration.get("status") == "plan_limit_exceeded":
        raise PermissionError(registration.get("message") or "FeeHunt plan limit reached.")
    return service


# ============================================================
# Skenavimas
# ============================================================

def scan_gmail() -> dict[str, Any]:
    service = get_gmail_service()

    messages = collect_scan_messages(service)
    total = len(messages)

    phishing_risks = []
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
            html_body = extract_html_from_payload(payload)
            content = f"{subject}\n{sender}\n{snippet}\n{body}"

            analysis = analyze_email(content)
            phishing = analyze_phishing(sender, subject, f"{snippet}\n{body}", html_body)

            email_data = {
                "message_id": msg["id"],
                "subject": subject,
                "sender": sender,
                "date": date,
                "snippet": snippet,
                "categories": analysis["categories"],
                "matched_keywords": analysis["matched_keywords"],
            }

            # A phishing email is the most important thing to surface, so it
            # takes priority and is shown only in its own section (no duplicates).
            if phishing["is_phishing_risk"]:
                email_data["phishing_reasons"] = phishing["reasons"]
                phishing_risks.append(email_data)
            else:
                if analysis["is_financial_risk"]:
                    financial_risks.append(email_data)
                if analysis["is_subscription"] and not analysis["is_financial_risk"]:
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
    subscription_and_risk_count = subscription_count + len(financial_risks)
    promo_count = len(promotional_emails) + len(shop_emails) + len(newsletter_emails)
    estimated_savings = subscription_count * DEFAULT_ESTIMATED_SAVINGS_PER_SUBSCRIPTION

    return {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "last_scan_at": datetime.now().isoformat(timespec="seconds"),
        "emails_scanned": total,
        "subscriptions_found": subscription_and_risk_count,
        "promotions_found": promo_count,
        "phishing_found": len(phishing_risks),
        "estimated_savings": estimated_savings,
        "phishing_risks": phishing_risks,
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
