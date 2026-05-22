import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from gmail_actions import (
    archive_email,
    mark_as_important,
    delete_email,
    mark_as_spam,
    get_unsubscribe_link,
)
from subscription_actions import cancel_subscription

from config import (
    APP_NAME,
    APP_VERSION,
    APP_DIR,
    GMAIL_CREDENTIALS_FILE,
    LAST_SCAN_RESULTS_FILE,
    SETTINGS_FILE,
    RULES_FILE,
    DEFAULT_SETTINGS,
    DEFAULT_RULES,
    EMAIL_CATEGORIES,
    CATEGORY_ACTIONS,
    PROTECTED_CATEGORY_ALLOWED_ACTIONS,
)
from translations import normalize_auto_scan, normalize_language, t


MAIN_FILE = APP_DIR / "main.py"
RESULTS_FILE = LAST_SCAN_RESULTS_FILE
CREDENTIALS_FILE = GMAIL_CREDENTIALS_FILE
FEEDBACK_URL = "https://feehunt.pro/feedback"


st.set_page_config(
    page_title="FeeHunt",
    page_icon="💸",
    layout="wide",
)


# ============================================================
# Helpers
# ============================================================

def safe_rerun() -> None:
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()


def load_json_file(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return default


def save_json_file(path: Path, data: Any) -> bool:
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def load_settings() -> dict:
    saved = load_json_file(SETTINGS_FILE, {})
    if not isinstance(saved, dict):
        saved = {}
    settings = DEFAULT_SETTINGS.copy()
    settings.update(saved)
    settings["language"] = normalize_language(settings.get("language", "en"))
    settings["auto_scan"] = normalize_auto_scan(settings.get("auto_scan", "off"))
    if not SETTINGS_FILE.exists():
        save_settings(settings)
    return settings


def save_settings(settings: dict) -> bool:
    return save_json_file(SETTINGS_FILE, settings)


def load_rules() -> dict:
    saved = load_json_file(RULES_FILE, {})
    if not isinstance(saved, dict):
        saved = {}
    rules = {
        "category_actions": DEFAULT_RULES["category_actions"].copy(),
        "whitelist": [],
        "blacklist": [],
        "custom_categories": [],
    }
    rules.update(saved)
    return rules


def save_rules(rules: dict) -> bool:
    return save_json_file(RULES_FILE, rules)


def load_last_scan_results() -> dict | None:
    data = load_json_file(RESULTS_FILE, None)
    return data if isinstance(data, dict) else None


def normalize_savings(value: Any, currency: str = "USD") -> str:
    symbol_map = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbol_map.get(currency, "$")
    if isinstance(value, str) and value.startswith(("$", "€", "£")):
        return value
    try:
        return f"{symbol}{int(value)}"
    except Exception:
        return f"{symbol}0"




def normalize_rule_value(value: Any) -> str:
    """Sutvarko vartotojo įvestą siuntėją/raktažodį taisyklėms."""
    if not value:
        return ""
    return str(value).strip().lower()


def add_unique_rule_value(items: list[str], value: str) -> list[str]:
    """Prideda reikšmę į sąrašą be dublikatų."""
    normalized = normalize_rule_value(value)
    existing = [normalize_rule_value(item) for item in items if normalize_rule_value(item)]
    if normalized and normalized not in existing:
        existing.append(normalized)
    return existing


def collect_detected_senders(scan_data: dict | None) -> list[str]:
    """Surenka unikalius siuntėjus iš paskutinio Gmail skenavimo rezultatų."""
    if not scan_data:
        return []

    possible_sections = [
        "financial_risks",
        "subscriptions",
        "promotional_emails",
        "shop_emails",
        "newsletter_emails",
    ]

    senders = set()

    for section in possible_sections:
        emails = scan_data.get(section, []) or []
        for item in emails:
            if not isinstance(item, dict):
                continue
            sender = normalize_rule_value(item.get("sender"))
            if sender:
                senders.add(sender)

    return sorted(senders)

def refresh_scan_data() -> None:
    latest = load_last_scan_results()
    if latest:
        currency = st.session_state.get("settings", DEFAULT_SETTINGS).get("currency", "USD")
        latest["estimated_savings"] = normalize_savings(latest.get("estimated_savings", 0), currency)
        st.session_state.last_scan = latest


def get_email_identity(item: dict, card_type: str = "") -> str:
    message_id = item.get("message_id") or f"{item.get('sender', '')}_{item.get('subject', '')}"
    # Pridedame card_type kad išvengtume dublikatų kai tas pats laiškas rodomas keliose vietose
    suffix = f"_{card_type}" if card_type else ""
    return f"{message_id}{suffix}"


def current_language() -> str:
    return normalize_language(st.session_state.get("settings", {}).get("language", "en"))


# ============================================================
# Onboarding
# ============================================================

def show_onboarding() -> None:
    lang = current_language()
    st.title(t("onboarding.title", lang))
    st.subheader(t("onboarding.subtitle", lang))

    st.error(t("onboarding.credentials_missing", lang))

    st.divider()
    st.markdown(t("onboarding.how_to", lang))

    st.link_button(t("onboarding.open_console", lang), "https://console.cloud.google.com/")

    st.markdown(t("onboarding.steps", lang))

    st.code(str(APP_DIR), language=None)

    st.markdown(t("onboarding.reload", lang))

    st.divider()

    if st.button(t("onboarding.check_credentials", lang), type="primary"):
        if CREDENTIALS_FILE.exists():
            st.success(t("onboarding.credentials_found", lang))
            safe_rerun()
        else:
            st.error(t("onboarding.file_not_found", lang).format(path=APP_DIR))

    st.caption(t("onboarding.footer", lang))


# ============================================================
# Gmail Scan su progress bar
# ============================================================

def run_gmail_scan_with_progress() -> tuple[bool, str, str]:
    if not MAIN_FILE.exists():
        return False, "", t("scan.main_missing", current_language()).format(path=MAIN_FILE)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    python_executable = Path(sys.executable)

    try:
        process = subprocess.Popen(
            [str(python_executable), str(MAIN_FILE)],
            cwd=str(APP_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )

        progress_bar = st.progress(0, text=t("scan.progress_preparing", current_language()))
        status_text = st.empty()
        stdout_lines = []

        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            line = line.rstrip()
            if not line:
                continue
            stdout_lines.append(line)

            if line.startswith("PROGRESS:"):
                try:
                    parts = line.split(":", 2)
                    current, total = map(int, parts[1].split("/"))
                    subject_part = parts[2] if len(parts) > 2 else ""
                    pct = current / total if total > 0 else 0
                    progress_bar.progress(pct, text=f"Skenuojama {current}/{total}...")
                    status_text.caption(f"📧 {subject_part}")
                except Exception:
                    pass

        progress_bar.progress(1.0, text="Skenavimas baigtas!")
        status_text.empty()
        stderr_output = process.stderr.read() or ""
        return process.poll() == 0, "\n".join(stdout_lines), stderr_output

    except Exception as error:
        return False, "", str(error)


# ============================================================
# Taisyklių pritaikymas po skenavimo
# ============================================================

def apply_rules_to_scan(scan_data: dict, rules: dict) -> dict:
    """
    Automatiškai pritaiko kategorijų taisykles prie nuskenuotų laiškų.
    Grąžina dict su veiksmų rezultatais.
    """
    lang = current_language()
    category_actions = rules.get("category_actions", {})
    whitelist = [w.lower() for w in rules.get("whitelist", [])]
    blacklist = [b.lower() for b in rules.get("blacklist", [])]

    results = {
        "auto_deleted": [],
        "auto_archived": [],
        "needs_review": [],
        "notified": [],
        "ignored": [],
    }

    # Surenkame visus laiškus pagal kategorijas
    category_map = {
        "financial_risks": scan_data.get("financial_risks", []),
        "subscriptions": scan_data.get("subscriptions", []),
        "promotions": scan_data.get("promotional_emails", []),
        "shops": scan_data.get("shop_emails", []),
        "newsletters": scan_data.get("newsletter_emails", []),
    }

    processed_ids = set()

    for category_id, emails in category_map.items():
        action = category_actions.get(category_id, "ask")

        for email in emails:
            mid = email.get("message_id")
            if not mid or mid in processed_ids:
                continue

            sender = email.get("sender", "").lower()

            # Baltasis sąrašas – visada praleisti
            if any(w in sender for w in whitelist):
                results["ignored"].append({**email, "reason": t("rules.reason_whitelist", lang)})
                processed_ids.add(mid)
                continue

            # Juodasis sąrašas – visada ištrinti
            if any(b in sender for b in blacklist):
                try:
                    delete_email(mid)
                    results["auto_deleted"].append({**email, "reason": t("rules.reason_blacklist", lang)})
                except Exception as e:
                    results["needs_review"].append({**email, "reason": t("rules.error", lang).format(error=e)})
                processed_ids.add(mid)
                continue

            # Kategorijos veiksmas
            if action == "delete":
                try:
                    delete_email(mid)
                    results["auto_deleted"].append({**email, "category": category_id})
                except Exception as e:
                    results["needs_review"].append({**email, "reason": t("rules.delete_error", lang).format(error=e)})

            elif action == "archive":
                try:
                    archive_email(mid)
                    results["auto_archived"].append({**email, "category": category_id})
                except Exception as e:
                    results["needs_review"].append({**email, "reason": t("rules.archive_error", lang).format(error=e)})

            elif action == "ask":
                results["needs_review"].append({**email, "category": category_id})

            elif action == "notify":
                results["notified"].append({**email, "category": category_id})

            elif action == "ignore":
                results["ignored"].append({**email, "category": category_id})

            processed_ids.add(mid)

    return results


# ============================================================
# Email Card
# ============================================================

def show_email_card(item: dict, icon: str, card_type: str = "generic") -> None:
    lang = current_language()
    subject = item.get("subject") or t("email.no_subject", lang)
    sender = item.get("sender") or t("email.unknown_sender", lang)
    date = item.get("date") or ""
    snippet = item.get("snippet") or ""
    keywords = item.get("matched_keywords", {})
    message_id = item.get("message_id")
    safe_key = get_email_identity(item, card_type)
    gmail_url = f"https://mail.google.com/mail/u/0/#all/{message_id}" if message_id else None

    all_keywords = []
    if isinstance(keywords, dict):
        for kw_list in keywords.values():
            all_keywords.extend(kw_list)
    elif isinstance(keywords, list):
        all_keywords = keywords

    with st.expander(f"{icon} {subject}"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.write(f"**{t('email.sender_label', lang)}:** {sender}")
        with col_b:
            st.write(f"**{t('email.date_label', lang)}:** {date}")

        if all_keywords:
            st.write(f"**{t('email.detected_keywords', lang)}:** {', '.join(set(all_keywords))}")

        if snippet:
            st.caption(f"_{snippet}_")

        if not message_id:
            st.warning(t("email.missing_message_id", lang))
            return

        if gmail_url:
            st.link_button(t("actions.open_gmail", lang), gmail_url)

        st.write(t("email.actions_label", lang))
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button(t("actions.archive", lang), key=f"archive_{safe_key}"):
                try:
                    archive_email(message_id)
                    st.success(t("actions.archived", lang))
                    refresh_scan_data()
                    safe_rerun()
                except Exception as e:
                    st.error(str(e))

        with col2:
            if st.button(t("actions.delete", lang), key=f"delete_{safe_key}"):
                try:
                    delete_email(message_id)
                    st.success(t("actions.deleted", lang))
                    refresh_scan_data()
                    safe_rerun()
                except Exception as e:
                    st.error(str(e))

        with col3:
            if st.button(t("actions.spam", lang), key=f"spam_{safe_key}"):
                try:
                    mark_as_spam(message_id)
                    st.success(t("actions.spam_marked", lang))
                    refresh_scan_data()
                    safe_rerun()
                except Exception as e:
                    st.error(str(e))

        with col4:
            if st.button(t("actions.important", lang), key=f"important_{safe_key}"):
                try:
                    mark_as_important(message_id)
                    st.success(t("actions.important_marked", lang))
                    refresh_scan_data()
                    safe_rerun()
                except Exception as e:
                    st.error(str(e))

        # Unsubscribe
        unsubscribe_url = None
        try:
            unsubscribe_url = get_unsubscribe_link(message_id)
        except Exception:
            pass

        if unsubscribe_url:
            st.link_button(t("actions.unsubscribe", lang), unsubscribe_url)
        elif card_type in ("financial_risk", "subscriptions"):
            st.info(t("actions.no_unsubscribe", lang))

        if card_type in ("financial_risk", "subscriptions"):
            service_name = sender.split("<", 1)[0].strip() or sender
            if st.button(t("actions.cancel_subscription", lang), key=f"cancel_subscription_{safe_key}"):
                try:
                    cancel_subscription(service_name, message_id)
                    st.info(t("actions.cancel_aftercare", lang))
                except Exception as e:
                    st.error(str(e))

        # Whitelist / Blacklist mygtukai
        st.divider()
        col_w, col_b = st.columns(2)
        rules = st.session_state.get("rules", load_rules())

        with col_w:
            if st.button(t("actions.whitelist", lang), key=f"whitelist_{safe_key}",
                         help=t("actions.whitelist_help", lang)):
                if sender not in rules["whitelist"]:
                    rules["whitelist"].append(sender)
                    save_rules(rules)
                    st.session_state.rules = rules
                    st.success(t("actions.added_whitelist", lang).format(sender=sender))

        with col_b:
            if st.button(t("actions.blacklist", lang), key=f"blacklist_{safe_key}",
                         help=t("actions.blacklist_help", lang)):
                if sender not in rules["blacklist"]:
                    rules["blacklist"].append(sender)
                    save_rules(rules)
                    st.session_state.rules = rules
                    st.success(t("actions.added_blacklist", lang).format(sender=sender))


# ============================================================
# Bulk Actions
# ============================================================

def bulk_action(emails: list[dict], action_fn, label: str) -> None:
    lang = current_language()
    count, errors = 0, []
    for item in emails:
        mid = item.get("message_id")
        if mid:
            try:
                action_fn(mid)
                count += 1
            except Exception as e:
                errors.append(str(e))
    st.success(t("bulk.result", lang).format(label=label, count=count))
    if errors:
        st.warning(t("bulk.errors", lang).format(count=len(errors)))


def show_bulk_actions(emails: list[dict], location_key: str) -> None:
    if not emails:
        return
    lang = current_language()
    st.caption(t("bulk.caption", lang))
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(t("actions.archive", lang), type="primary", key=f"arch_all_{location_key}"):
            bulk_action(emails, archive_email, t("bulk.archived", lang))
            safe_rerun()
    with col2:
        if st.button(t("actions.delete", lang), key=f"del_all_{location_key}"):
            bulk_action(emails, delete_email, t("bulk.deleted", lang))
            safe_rerun()
    with col3:
        if st.button(t("actions.spam", lang), key=f"spam_all_{location_key}"):
            bulk_action(emails, mark_as_spam, t("bulk.spam", lang))
            safe_rerun()


# ============================================================
# Status Panel
# ============================================================

def show_status_panel() -> None:
    lang = current_language()
    st.caption(f"{APP_NAME} {APP_VERSION}")
    st.caption(t("status.app_folder", lang).format(path=APP_DIR))
    st.success(t("status.main_found", lang)) if MAIN_FILE.exists() else st.error(t("status.main_missing", lang))
    st.success(t("status.results_found", lang)) if RESULTS_FILE.exists() else st.info(t("status.not_created", lang))
    st.success(t("status.credentials_found", lang)) if CREDENTIALS_FILE.exists() else st.error(t("status.credentials_missing", lang))


def show_feedback_section() -> None:
    lang = current_language()
    st.divider()
    st.info(t("feedback.message", lang))
    st.link_button(t("feedback.button", lang), FEEDBACK_URL)


def show_how_to_use_page() -> None:
    lang = current_language()
    st.title(t("how_to.title", lang))

    st.subheader(t("how_to.intro_heading", lang))
    st.write(t("how_to.intro", lang))

    st.subheader(t("how_to.scan_heading", lang))
    st.markdown(t("how_to.scan_steps", lang))

    st.subheader(t("how_to.results_heading", lang))
    st.markdown(t("how_to.results_bullets", lang))

    st.subheader(t("how_to.cancel_heading", lang))
    st.markdown(t("how_to.cancel_steps", lang))

    st.subheader(t("how_to.delete_heading", lang))
    st.markdown(t("how_to.delete_bullets", lang))

    st.subheader(t("how_to.privacy_heading", lang))
    st.markdown(t("how_to.privacy_bullets", lang))

    st.subheader(t("how_to.tips_heading", lang))
    st.markdown(t("how_to.tips_bullets", lang))
    show_feedback_section()


# ============================================================
# State Init
# ============================================================

def initialize_state() -> None:
    if "settings" not in st.session_state:
        st.session_state.settings = load_settings()
    if "last_scan" not in st.session_state:
        st.session_state.last_scan = load_last_scan_results()
    if "rules" not in st.session_state:
        st.session_state.rules = load_rules()
    if "cleanup_results" not in st.session_state:
        st.session_state.cleanup_results = None


initialize_state()


# ============================================================
# Onboarding patikrinimas
# ============================================================

if not CREDENTIALS_FILE.exists():
    show_onboarding()
    st.stop()

lang = current_language()


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.title(t("app.brand_title", lang))
    st.caption(t("sidebar.caption", lang))

    page_options = ["Dashboard", "Subscriptions", "How to Use FeeHunt", "Cleanup Rules", "Settings"]
    page = st.radio(
        t("sidebar.navigation", lang),
        page_options,
        format_func=lambda x: {
            "Dashboard": t("page.dashboard", lang),
            "Subscriptions": t("page.subscriptions", lang),
            "How to Use FeeHunt": t("page.how_to_use", lang),
            "Cleanup Rules": t("page.cleanup_rules", lang),
            "Settings": t("page.settings", lang),
        }.get(x, x),
    )

    st.divider()
    st.caption(t("sidebar.footer", lang))


# ============================================================
# Dashboard
# ============================================================

if page == "Dashboard":
    st.title(t("dashboard.title", lang))
    st.subheader(t("dashboard.subtitle", lang))

    st.info(t("dashboard.plan_info", lang))

    apply_after = st.session_state.settings.get("apply_rules_after_scan", False)

    if apply_after:
        st.success(t("dashboard.auto_cleanup_on", lang))

    if st.button(t("dashboard.scan_button", lang), type="primary"):
        success, stdout, stderr = run_gmail_scan_with_progress()

        if success:
            currency = st.session_state.settings.get("currency", "USD")
            saved = load_last_scan_results()
            if saved:
                saved["estimated_savings"] = normalize_savings(saved.get("estimated_savings", 0), currency)
                st.session_state.last_scan = saved

            st.success(t("dashboard.scan_success", lang))

            # Automatinis taisyklių pritaikymas
            if apply_after and saved:
                with st.spinner(t("dashboard.apply_rules_spinner", lang)):
                    results = apply_rules_to_scan(saved, st.session_state.rules)
                    st.session_state.cleanup_results = results

                deleted = len(results.get("auto_deleted", []))
                archived = len(results.get("auto_archived", []))
                review = len(results.get("needs_review", []))

                if deleted or archived:
                    st.success(t("dashboard.auto_deleted", lang).format(deleted=deleted, archived=archived))
                if review:
                    st.info(t("dashboard.needs_review", lang).format(review=review))
        else:
            st.error(t("dashboard.scan_error", lang))
            st.code(stderr or t("dashboard.no_error_text", lang))

    scan_data = st.session_state.last_scan

    st.subheader(t("dashboard.results_heading", lang))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t("dashboard.metric_subscriptions", lang),
                  scan_data.get("subscriptions_found", 0) if scan_data else 0)
    with col2:
        st.metric(t("dashboard.metric_promotions", lang),
                  scan_data.get("promotions_found", 0) if scan_data else 0)
    with col3:
        st.metric(t("dashboard.metric_savings", lang),
                  scan_data.get("estimated_savings", "$0") if scan_data else "$0")

    if scan_data:
        last_scan_at = scan_data.get("last_scan_at")
        if last_scan_at:
            st.caption(t("dashboard.last_scan", lang).format(last_scan_at=last_scan_at))

        st.divider()
        max_items = int(st.session_state.settings.get("max_dashboard_items", 3) or 3)
        financial_risks = scan_data.get("financial_risks", []) or []
        subscriptions = scan_data.get("subscriptions", []) or []
        promotional_items = []
        seen_promotional_ids = set()
        for section in ("promotional_emails", "shop_emails", "newsletter_emails"):
            for item in scan_data.get(section, []) or []:
                item_id = item.get("message_id") or get_email_identity(item, section)
                if item_id not in seen_promotional_ids:
                    promotional_items.append(item)
                    seen_promotional_ids.add(item_id)

        if financial_risks:
            st.subheader(t("financial_risks.heading", lang))
            for item in financial_risks[:max_items]:
                show_email_card(item, "💳", "financial_risk")
        else:
            st.success(t("financial_risks.none", lang))

        if subscriptions:
            st.subheader(t("subscriptions.heading", lang))
            for item in subscriptions[:max_items]:
                show_email_card(item, "🔄", "subscriptions")

        if promotional_items:
            st.subheader(t("promotions.heading", lang))
            for item in promotional_items[:max_items]:
                show_email_card(item, "📢", "promotions")

    else:
        st.divider()
        st.markdown(t("dashboard.get_started", lang))
        st.markdown(t("dashboard.no_scan", lang))
        col_a, col_b = st.columns(2)
        with col_a:
            st.info(t("dashboard.privacy", lang))
        with col_b:
            st.info(t("dashboard.fast", lang))

    st.divider()
    st.caption(t("dashboard.footer", lang))


# ============================================================
# Subscriptions
# ============================================================

elif page == "Subscriptions":
    st.title(t("subscriptions.page_title", lang))

    scan_data = st.session_state.last_scan

    if not scan_data:
        st.info(t("subscriptions.no_scan", lang))
        st.markdown(t("subscriptions.no_scan_instruction", lang))
    else:
        financial_risks = scan_data.get("financial_risks", []) or []
        subscriptions = scan_data.get("subscriptions", []) or []

        if financial_risks:
            st.subheader(t("financial_risks.heading", lang))
            st.warning(t("financial_risks.warning", lang).format(count=len(financial_risks)))
            for item in financial_risks:
                show_email_card(item, "💳", "financial_risk")
        else:
            st.success(t("financial_risks.none", lang))

        if subscriptions:
            st.subheader(t("subscriptions.heading", lang))
            st.info(t("subscriptions.found", lang).format(count=len(subscriptions)))
            for item in subscriptions:
                show_email_card(item, "🔄", "subscriptions")
        else:
            st.success(t("subscriptions.none", lang))


# ============================================================
# How to Use FeeHunt
# ============================================================

elif page == "How to Use FeeHunt":
    show_how_to_use_page()


# ============================================================
# Cleanup Rules
# ============================================================

elif page == "Cleanup Rules":
    st.title(t("cleanup.title", lang))

    tabs = st.tabs([
        t("cleanup.tab_unwanted", lang),
        t("cleanup.tab_category_rules", lang),
        t("cleanup.tab_whitelist", lang),
        t("cleanup.tab_blacklist", lang),
        t("cleanup.tab_custom", lang),
        t("cleanup.tab_results", lang),
    ])

    rules = st.session_state.rules



    # ── Tab 1: Mano nepageidaujami siuntėjai ──
    with tabs[0]:
        st.subheader(t("cleanup.unwanted_title", lang))
        st.caption(t("cleanup.unwanted_caption", lang))

        settings = st.session_state.settings.copy()
        unwanted_senders = [
            normalize_rule_value(sender)
            for sender in settings.get("promo_senders", [])
            if normalize_rule_value(sender)
        ]
        unwanted_keywords = [
            normalize_rule_value(keyword)
            for keyword in settings.get("promo_keywords", [])
            if normalize_rule_value(keyword)
        ]

        st.info(t("cleanup.control_info", lang))

        scan_data = st.session_state.last_scan
        detected_senders = collect_detected_senders(scan_data)
        all_senders = sorted(set(detected_senders + unwanted_senders))

        st.markdown(t("cleanup.mark_unwanted", lang))

        if not all_senders:
            st.info(t("cleanup.no_detected_senders", lang))
        else:
            selected_senders = []
            for sender in all_senders:
                checked = sender in unwanted_senders
                if st.checkbox(sender, value=checked, key=f"unwanted_sender_{sender}"):
                    selected_senders.append(sender)

            if st.button(t("cleanup.save_unwanted", lang), type="primary", key="save_unwanted_senders"):
                settings["promo_senders"] = sorted(set(selected_senders))
                settings["promo_keywords"] = sorted(set(unwanted_keywords))
                if save_settings(settings):
                    st.session_state.settings = settings
                    st.success(t("cleanup.unwanted_saved", lang))
                    st.caption(t("cleanup.rescan_caption", lang))
                    safe_rerun()
                else:
                    st.error(t("cleanup.save_error", lang))

        st.divider()
        st.markdown(t("cleanup.add_sender_heading", lang))
        manual_sender = st.text_input(
            t("cleanup.sender_input", lang),
            placeholder=t("cleanup.sender_placeholder", lang),
            key="manual_unwanted_sender",
        )

        if st.button(t("cleanup.add_sender", lang), key="add_manual_unwanted_sender"):
            normalized_sender = normalize_rule_value(manual_sender)
            if not normalized_sender:
                st.warning(t("cleanup.enter_sender", lang))
            else:
                settings["promo_senders"] = add_unique_rule_value(unwanted_senders, normalized_sender)
                settings["promo_keywords"] = sorted(set(unwanted_keywords))
                if save_settings(settings):
                    st.session_state.settings = settings
                    st.success(t("cleanup.sender_added", lang).format(sender=normalized_sender))
                    safe_rerun()
                else:
                    st.error(t("cleanup.save_error", lang))

        st.divider()
        st.markdown(t("cleanup.keywords_heading", lang))
        st.caption(t("cleanup.keywords_caption", lang))

        manual_keyword = st.text_input(
            t("cleanup.keyword_input", lang),
            placeholder=t("cleanup.keyword_placeholder", lang),
            key="manual_promo_keyword",
        )

        col_kw_add, col_kw_save = st.columns(2)
        with col_kw_add:
            if st.button(t("cleanup.add_keyword", lang), key="add_manual_promo_keyword"):
                normalized_keyword = normalize_rule_value(manual_keyword)
                if not normalized_keyword:
                    st.warning(t("cleanup.enter_keyword", lang))
                else:
                    settings["promo_senders"] = sorted(set(unwanted_senders))
                    settings["promo_keywords"] = add_unique_rule_value(unwanted_keywords, normalized_keyword)
                    if save_settings(settings):
                        st.session_state.settings = settings
                        st.success(t("cleanup.keyword_added", lang).format(keyword=normalized_keyword))
                        safe_rerun()
                    else:
                        st.error(t("cleanup.save_error", lang))

        if unwanted_keywords:
            st.markdown(t("cleanup.current_keywords", lang))
            selected_keywords = []
            for keyword in sorted(set(unwanted_keywords)):
                if st.checkbox(keyword, value=True, key=f"promo_keyword_{keyword}"):
                    selected_keywords.append(keyword)

            with col_kw_save:
                if st.button(t("cleanup.save_keywords", lang), key="save_promo_keywords"):
                    settings["promo_senders"] = sorted(set(unwanted_senders))
                    settings["promo_keywords"] = sorted(set(selected_keywords))
                    if save_settings(settings):
                        st.session_state.settings = settings
                        st.success(t("cleanup.keywords_saved", lang))
                        safe_rerun()
                    else:
                        st.error(t("cleanup.save_error", lang))
        else:
            st.caption(t("cleanup.no_keywords", lang))

        st.divider()
        st.markdown(t("cleanup.how_heading", lang))
        st.write(t("cleanup.how_text", lang))

    # ── Tab 1: Kategorijų taisyklės ──
    with tabs[1]:
        st.subheader(t("cleanup.category_title", lang))
        st.caption(t("cleanup.category_caption", lang))

        updated_actions = rules["category_actions"].copy()
        changed = False

        for cat in EMAIL_CATEGORIES:
            cat_id = cat["id"]
            icon = cat["icon"]
            label = t(f"category.{cat_id}.label", lang)
            desc = t(f"category.{cat_id}.description", lang)
            protected = cat.get("protected", False)

            col_label, col_select = st.columns([2, 2])

            with col_label:
                st.markdown(f"**{icon} {label}**")
                st.caption(desc)
                if protected:
                    st.caption(t("cleanup.protected", lang))

            with col_select:
                if protected:
                    st.selectbox(
                        t("cleanup.action_label", lang),
                        options=["notify"],
                        format_func=lambda x: t(f"category_action.{x}", lang),
                        key=f"action_{cat_id}",
                        disabled=True,
                    )
                else:
                    current = updated_actions.get(cat_id, "ask")
                    options = list(CATEGORY_ACTIONS.keys())
                    new_val = st.selectbox(
                        t("cleanup.action_label", lang),
                        options=options,
                        format_func=lambda x: t(f"category_action.{x}", lang),
                        index=options.index(current) if current in options else 0,
                        key=f"action_{cat_id}",
                    )
                    if new_val != current:
                        updated_actions[cat_id] = new_val
                        changed = True

            st.divider()

        if st.button(t("cleanup.save_rules", lang), type="primary", key="save_cat_rules"):
            rules["category_actions"] = updated_actions
            save_rules(rules)
            st.session_state.rules = rules
            st.success(t("cleanup.rules_saved", lang))

        st.divider()

        # Pritaikyti dabar
        scan_data = st.session_state.last_scan
        if scan_data:
            if st.button(t("cleanup.apply_now", lang), key="apply_rules_now"):
                with st.spinner(t("dashboard.apply_rules_spinner", lang)):
                    results = apply_rules_to_scan(scan_data, rules)
                    st.session_state.cleanup_results = results
                    refresh_scan_data()

                deleted = len(results.get("auto_deleted", []))
                archived = len(results.get("auto_archived", []))
                review = len(results.get("needs_review", []))

                st.success(t("cleanup.done", lang).format(deleted=deleted, archived=archived))
                if review:
                    st.info(t("cleanup.review_waiting", lang).format(review=review))
        else:
            st.info(t("cleanup.scan_first", lang))

    # ── Tab 2: Baltasis sąrašas ──
    with tabs[2]:
        st.subheader(t("cleanup.whitelist_title", lang))
        st.caption(t("cleanup.whitelist_caption", lang))

        whitelist = rules.get("whitelist", [])

        new_white = st.text_input(
            t("cleanup.whitelist_input", lang),
            placeholder=t("cleanup.whitelist_placeholder", lang),
            key="new_whitelist_entry",
        )

        if st.button(t("cleanup.whitelist_add", lang), key="add_white"):
            if new_white and new_white not in whitelist:
                whitelist.append(new_white.strip())
                rules["whitelist"] = whitelist
                save_rules(rules)
                st.session_state.rules = rules
                st.success(t("cleanup.whitelist_added", lang).format(sender=new_white))
                safe_rerun()

        if whitelist:
            st.markdown(t("cleanup.whitelist_current", lang))
            for i, entry in enumerate(whitelist):
                col_e, col_d = st.columns([4, 1])
                with col_e:
                    st.write(f"✅ {entry}")
                with col_d:
                    if st.button(t("actions.remove", lang), key=f"rm_white_{i}"):
                        whitelist.pop(i)
                        rules["whitelist"] = whitelist
                        save_rules(rules)
                        st.session_state.rules = rules
                        safe_rerun()
        else:
            st.info(t("cleanup.whitelist_empty", lang))

    # ── Tab 3: Juodasis sąrašas ──
    with tabs[3]:
        st.subheader(t("cleanup.blacklist_title", lang))
        st.caption(t("cleanup.blacklist_caption", lang))

        blacklist = rules.get("blacklist", [])

        new_black = st.text_input(
            t("cleanup.blacklist_input", lang),
            placeholder=t("cleanup.blacklist_placeholder", lang),
            key="new_blacklist_entry",
        )

        if st.button(t("cleanup.blacklist_add", lang), key="add_black"):
            if new_black and new_black not in blacklist:
                blacklist.append(new_black.strip())
                rules["blacklist"] = blacklist
                save_rules(rules)
                st.session_state.rules = rules
                st.success(t("cleanup.blacklist_added", lang).format(sender=new_black))
                safe_rerun()

        if blacklist:
            st.markdown(t("cleanup.blacklist_current", lang))
            for i, entry in enumerate(blacklist):
                col_e, col_d = st.columns([4, 1])
                with col_e:
                    st.write(f"🚫 {entry}")
                with col_d:
                    if st.button(t("actions.remove", lang), key=f"rm_black_{i}"):
                        blacklist.pop(i)
                        rules["blacklist"] = blacklist
                        save_rules(rules)
                        st.session_state.rules = rules
                        safe_rerun()
        else:
            st.info(t("cleanup.blacklist_empty", lang))

    # ── Tab 4: Mano kategorijos ──
    with tabs[4]:
        st.subheader(t("cleanup.custom_title", lang))
        st.caption(t("cleanup.custom_caption", lang))

        custom_categories = rules.get("custom_categories", [])

        with st.form("new_custom_category"):
            c_name = st.text_input(t("cleanup.custom_name", lang), placeholder=t("cleanup.custom_name_placeholder", lang))
            c_keywords = st.text_input(t("cleanup.custom_keywords", lang), placeholder=t("cleanup.custom_keywords_placeholder", lang))
            c_action = st.selectbox(
                t("cleanup.action_label", lang),
                options=list(CATEGORY_ACTIONS.keys()),
                format_func=lambda x: t(f"category_action.{x}", lang),
            )
            submitted = st.form_submit_button(t("cleanup.custom_create", lang))

            if submitted and c_name and c_keywords:
                kw_list = [k.strip() for k in c_keywords.split(",") if k.strip()]
                custom_categories.append({
                    "id": f"custom_{len(custom_categories)}",
                    "label": c_name,
                    "keywords": kw_list,
                    "action": c_action,
                })
                rules["custom_categories"] = custom_categories
                save_rules(rules)
                st.session_state.rules = rules
                st.success(t("cleanup.custom_created", lang).format(name=c_name))
                safe_rerun()

        if custom_categories:
            st.markdown(t("cleanup.custom_current", lang))
            for i, cat in enumerate(custom_categories):
                col_info, col_del = st.columns([4, 1])
                with col_info:
                    action_label = t(f"category_action.{cat['action']}", lang)
                    st.write(f"**{cat['label']}** – {action_label}")
                    st.caption(t("cleanup.custom_keyword_label", lang).format(keywords=", ".join(cat.get("keywords", []))))
                with col_del:
                    if st.button(t("actions.remove", lang), key=f"rm_cat_{i}"):
                        custom_categories.pop(i)
                        rules["custom_categories"] = custom_categories
                        save_rules(rules)
                        st.session_state.rules = rules
                        safe_rerun()
        else:
            st.info(t("cleanup.custom_empty", lang))

    # ── Tab 5: Valymo rezultatai ──
    with tabs[5]:
        st.subheader(t("cleanup.results_title", lang))

        cleanup_results = st.session_state.get("cleanup_results")

        if not cleanup_results:
            st.info(t("cleanup.no_results", lang))
        else:
            deleted = cleanup_results.get("auto_deleted", [])
            archived = cleanup_results.get("auto_archived", [])
            review = cleanup_results.get("needs_review", [])
            notified = cleanup_results.get("notified", [])

            col1, col2, col3, col4 = st.columns(4)
            col1.metric(t("cleanup.metric_deleted", lang), len(deleted))
            col2.metric(t("cleanup.metric_archived", lang), len(archived))
            col3.metric(t("cleanup.metric_review", lang), len(review))
            col4.metric(t("cleanup.metric_notified", lang), len(notified))

            if review:
                st.divider()
                st.subheader(t("cleanup.waiting_title", lang))
                st.caption(t("cleanup.waiting_caption", lang))
                for item in review:
                    show_email_card(item, "❓", "review")

            if deleted:
                st.divider()
                with st.expander(t("cleanup.deleted_expander", lang).format(count=len(deleted))):
                    for item in deleted:
                        subject = item.get("subject") or t("email.no_subject", lang)
                        sender = item.get("sender") or ""
                        reason = item.get("reason") or item.get("category") or ""
                        st.write(f"🗑 **{subject}** – {sender} _{reason}_")

            if archived:
                st.divider()
                with st.expander(t("cleanup.archived_expander", lang).format(count=len(archived))):
                    for item in archived:
                        subject = item.get("subject") or t("email.no_subject", lang)
                        sender = item.get("sender") or ""
                        st.write(f"📥 **{subject}** – {sender}")


# ============================================================
# Settings
# ============================================================

elif page == "Settings":
    st.title(t("settings.title", lang))

    settings = st.session_state.settings.copy()
    settings_lang = normalize_language(settings.get("language", "en"))
    language_options = {
        t("language.english", settings_lang): "en",
        t("language.lithuanian", settings_lang): "lt",
    }
    language_labels = list(language_options.keys())
    current_language_label = (
        t("language.lithuanian", settings_lang)
        if settings_lang == "lt"
        else t("language.english", settings_lang)
    )

    selected_language = st.selectbox(
        t("settings.language", lang),
        language_labels,
        index=language_labels.index(current_language_label),
    )
    settings["language"] = language_options[selected_language]

    settings["currency"] = st.selectbox(
        t("settings.currency", settings["language"]),
        ["USD", "EUR", "GBP"],
        index=["USD", "EUR", "GBP"].index(settings.get("currency", "USD")),
    )

    settings["auto_scan"] = st.selectbox(
        t("settings.auto_scan", settings["language"]),
        ["off", "hourly", "daily"],
        index=["off", "hourly", "daily"].index(settings.get("auto_scan", "off")),
        format_func=lambda x: {
            "off": t("settings.auto_scan_off", settings["language"]),
            "hourly": t("settings.auto_scan_hourly", settings["language"]),
            "daily": t("settings.auto_scan_daily", settings["language"]),
        }.get(x, x),
    )

    settings["apply_rules_after_scan"] = st.checkbox(
        t("settings.apply_rules", settings["language"]),
        value=bool(settings.get("apply_rules_after_scan", False)),
        help=t("settings.apply_rules_help", settings["language"]),
    )

    settings["safe_mode"] = st.checkbox(
        t("settings.safe_mode", settings["language"]),
        value=bool(settings.get("safe_mode", True)),
        help=t("settings.safe_mode_help", settings["language"]),
    )

    settings["max_dashboard_items"] = st.slider(
        t("settings.max_dashboard", settings["language"]),
        min_value=1,
        max_value=10,
        value=int(settings.get("max_dashboard_items", 3) or 3),
    )

    if st.button(t("settings.save", settings["language"]), type="primary"):
        if save_settings(settings):
            st.session_state.settings = settings
            refresh_scan_data()
            st.success(t("settings.saved", settings["language"]))
            safe_rerun()
        else:
            st.error(t("settings.save_error", settings["language"]))

    st.divider()
    st.subheader(t("settings.technical_info", settings["language"]))
    with st.container():
        show_status_panel()
    show_feedback_section()
