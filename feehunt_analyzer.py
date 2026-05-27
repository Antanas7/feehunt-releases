import json

from config import (
    SETTINGS_FILE,
    KEYWORDS,
    HIGH_CONFIDENCE_SUBSCRIPTION_KEYWORDS,
    HIGH_CONFIDENCE_PROMOTIONAL_KEYWORDS,
    HIGH_CONFIDENCE_SHOP_KEYWORDS,
    HIGH_CONFIDENCE_FINANCIAL_KEYWORDS,
)


# ============================================================
# Raktažodžiai iš config.py
# ============================================================

SUBSCRIPTION_KEYWORDS = KEYWORDS["subscription"]
PROMO_KEYWORDS = KEYWORDS["promotional"]
SHOP_KEYWORDS = KEYWORDS["shops"]
NEWSLETTER_KEYWORDS = KEYWORDS["newsletters"]
FINANCIAL_KEYWORDS = KEYWORDS["financial_risks"]


# ============================================================
# Vartotojo taisyklės iš feehunt_settings.json
# ============================================================

def load_user_settings() -> dict:
    defaults = {
        "promo_senders": [],
        "promo_keywords": [],
    }

    if not SETTINGS_FILE.exists():
        return defaults

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return defaults

        return {
            "promo_senders": data.get("promo_senders", []) or [],
            "promo_keywords": data.get("promo_keywords", []) or [],
        }
    except Exception:
        return defaults


def get_user_promo_senders() -> list[str]:
    return [
        str(sender).strip().lower()
        for sender in load_user_settings().get("promo_senders", [])
        if str(sender).strip()
    ]


def get_user_promo_keywords() -> list[str]:
    return [
        str(keyword).strip().lower()
        for keyword in load_user_settings().get("promo_keywords", [])
        if str(keyword).strip()
    ]


# ============================================================
# Techniniai / sisteminiai laiškai – ignoruojami
# ============================================================

IGNORE_KEYWORDS = [
    "google cloud", "firebase",
    "gcp", "bigquery", "google play console", "play console",
    "api key", "api quota", "developer console",
    "aws", "amazon web services", "azure", "github actions",
    "vercel", "netlify", "docker hub", "render.com", "railway",
    "cloudflare", "analytics report", "search console",
]

IGNORE_SENDER_KEYWORDS = [
    "noreply@google.com", "no-reply@google.com",
    "cloud-noreply@google.com", "firebase-noreply@google.com",
    "notifications@github.com",
]

MIN_KEYWORD_MATCHES = 2

SUBSCRIPTION_SIGNAL_KEYWORDS = [
    "subscription access", "subscription renews", "renews soon",
    "subscription was canceled", "subscription has been paused",
    "recurring payment", "auto-renew", "auto renewal", "renewal",
    "billing account", "invoice", "membership",
    "your subscription", "your plan", "the next charge",
    "next billing", "next payment", "thanks for subscribing",
    "thank you for subscribing", "monthly plan", "annual plan",
    "prenumerata", "prenumeratos", "atnaujinimas", "jūsų prenumerata",
    "narystė", "metinis planas", "mėnesinis planas",
]

SUBSCRIPTION_LIFECYCLE_KEYWORDS = [
    # Strong "this is a real subscription event" signals — these flip the
    # NON_RISK_RECEIPT short-circuit so transactional Pro-plan / Welcome /
    # subscription-started emails still get categorized.
    "subscription access", "subscription renews", "renews soon",
    "subscription was canceled", "subscription has been paused",
    "recurring payment", "auto-renew", "auto renewal", "renewal",
    "your subscription", "the next charge", "next billing",
    "next payment", "starting your", "your plan", "pro plan",
    "annual plan", "monthly plan", "thanks for subscribing",
    "thank you for subscribing", "subscription started",
    "prenumerata", "prenumeratos", "atnaujinimas",
    "jūsų prenumerata", "kitas mokėjimas",
]

SUBSCRIPTION_SOFT_KEYWORDS = [
    "invoice", "billing account", "membership", "payment method",
]

FINANCIAL_RISK_SIGNAL_KEYWORDS = [
    # Failed payment / overdue / suspended account
    "failed payment", "payment failed", "payment failed to process",
    "failed to process", "card declined", "insufficient funds",
    "insufficient funds on card", "past due", "overdue",
    "account suspended", "payment required", "invalid payment",
    "payment was unsuccessful", "was unsuccessful",
    "subscription access has been paused", "subscription paused",
    "update your payment", "payment method needs",
    # Identity / phishing-adjacent signals (Bybit "Action required" /
    # Stripe "verification link" type patterns)
    "action required", "verify your identity", "verify your account",
    "confirm your identity", "confirm your account",
    "biometric verification", "set up biometric",
    "security alert", "unusual sign-in", "suspicious sign-in",
    "suspicious activity", "unauthorized access", "unauthorized sign",
    "account locked", "your account has been locked",
    "regulatory compliance", "kyc verification", "identity verification",
    "click here to verify", "verify now", "verification required",
    "verification link",
    # Lithuanian
    "nepavyko apmokėti", "nepavyko apmoketi",
    "kortelė atmesta", "kortele atmesta",
    "vėluojantis mokėjimas", "veluojantis mokejimas",
    "paskyra sustabdyta", "paskyra užblokuota", "paskyra uzblokuota",
    "patvirtinkite tapatybę", "patvirtinkite tapatybe",
    "patvirtinkite paskyrą", "patvirtinkite paskyra",
    "tapatybės patikrinimas", "tapatybes patikrinimas",
    "saugumo įspėjimas", "saugumo ispejimas",
    "įtartina veikla", "itartina veikla",
    "neatidėliotinas veiksmas", "neatideliotinas veiksmas",
]

NON_RISK_RECEIPT_KEYWORDS = [
    "payment received", "your receipt", "receipt from",
    "order summary", "license key", "welcome to",
]

NON_SUBSCRIPTION_MARKETING_KEYWORDS = [
    "sample invoice", "ready to learn", "learn more",
    "local seller", "boost 3x revenue", "hot-selling products",
    "verified suppliers", "webinars",
]


# ============================================================
# Helper funkcijos
# ============================================================

def normalize_content(content: str) -> str:
    return content.lower() if content else ""


def contains_any_keyword(content: str, keywords: list[str]) -> bool:
    return any(str(kw).lower() in content for kw in keywords if str(kw).strip())


def count_keyword_matches(content: str, keywords: list[str]) -> int:
    return sum(1 for kw in keywords if str(kw).lower() in content)


def get_matching_keywords(content: str, keywords: list[str]) -> list[str]:
    return [kw for kw in keywords if str(kw).lower() in content]


def should_ignore_email(content: str) -> bool:
    return (
        contains_any_keyword(content, IGNORE_KEYWORDS)
        or contains_any_keyword(content, IGNORE_SENDER_KEYWORDS)
    )


def get_user_promotional_matches(content: str) -> list[str]:
    user_rules = get_user_promo_senders() + get_user_promo_keywords()
    return get_matching_keywords(content, user_rules)


# ============================================================
# Confidence Score sistema
# ============================================================

def _confidence(content: str, high_conf_keywords: list[str], all_keywords: list[str]) -> float:
    if contains_any_keyword(content, high_conf_keywords):
        return 1.0
    matches = count_keyword_matches(content, all_keywords)
    if matches >= 2:
        return 0.8
    if matches == 1:
        return 0.3
    return 0.0


THRESHOLD = 0.5


def get_subscription_confidence(content: str) -> float:
    if contains_any_keyword(content, FINANCIAL_RISK_SIGNAL_KEYWORDS):
        return 1.0

    if contains_any_keyword(content, NON_SUBSCRIPTION_MARKETING_KEYWORDS):
        return 0.0

    if contains_any_keyword(content, NON_RISK_RECEIPT_KEYWORDS) and not contains_any_keyword(content, SUBSCRIPTION_LIFECYCLE_KEYWORDS):
        return 0.0

    promotional_confidence = get_promotional_confidence(content)
    newsletter_confidence = get_newsletter_confidence(content)
    has_lifecycle_signal = contains_any_keyword(content, SUBSCRIPTION_LIFECYCLE_KEYWORDS)
    has_soft_signal = contains_any_keyword(content, SUBSCRIPTION_SOFT_KEYWORDS)

    if (promotional_confidence >= THRESHOLD or newsletter_confidence >= THRESHOLD) and not has_lifecycle_signal:
        return 0.0

    if has_lifecycle_signal:
        return 1.0

    if has_soft_signal and count_keyword_matches(content, SUBSCRIPTION_KEYWORDS) >= 2:
        return 0.8

    return 0.0


def get_promotional_confidence(content: str) -> float:
    # Vartotojo pasirinkti siuntėjai / raktažodžiai turi aukščiausią prioritetą.
    if contains_any_keyword(content, get_user_promo_senders()):
        return 1.0

    if contains_any_keyword(content, get_user_promo_keywords()):
        return 1.0

    return _confidence(content, HIGH_CONFIDENCE_PROMOTIONAL_KEYWORDS, PROMO_KEYWORDS)


def get_shop_confidence(content: str) -> float:
    return _confidence(content, HIGH_CONFIDENCE_SHOP_KEYWORDS, SHOP_KEYWORDS)


def get_newsletter_confidence(content: str) -> float:
    matches = count_keyword_matches(content, NEWSLETTER_KEYWORDS)
    if matches >= 2:
        return 0.8
    if matches == 1:
        return 0.3
    return 0.0


def get_financial_confidence(content: str) -> float:
    if contains_any_keyword(content, FINANCIAL_RISK_SIGNAL_KEYWORDS):
        return 1.0
    return 0.0


# ============================================================
# Pagrindinės aptikimo funkcijos
# ============================================================

def check_for_subscription_risk(content: str) -> bool:
    normalized = normalize_content(content)
    if not normalized or should_ignore_email(normalized):
        return False
    return get_subscription_confidence(normalized) >= THRESHOLD


def check_for_promotional_email(content: str) -> bool:
    normalized = normalize_content(content)
    if not normalized or should_ignore_email(normalized):
        return False
    return get_promotional_confidence(normalized) >= THRESHOLD


def check_for_shop_email(content: str) -> bool:
    normalized = normalize_content(content)
    if not normalized or should_ignore_email(normalized):
        return False
    return get_shop_confidence(normalized) >= THRESHOLD


def check_for_newsletter(content: str) -> bool:
    normalized = normalize_content(content)
    if not normalized or should_ignore_email(normalized):
        return False
    return get_newsletter_confidence(normalized) >= THRESHOLD


def check_for_financial_risk(content: str) -> bool:
    normalized = normalize_content(content)
    if not normalized or should_ignore_email(normalized):
        return False
    return get_financial_confidence(normalized) >= THRESHOLD


# ============================================================
# Pilna kategorijų analizė viename funkcijos kvietimu
# ============================================================

def analyze_email(content: str) -> dict:
    normalized = normalize_content(content)

    if not normalized or should_ignore_email(normalized):
        return {
            "categories": [],
            "is_subscription": False,
            "is_promotional": False,
            "is_shop": False,
            "is_newsletter": False,
            "is_financial_risk": False,
            "matched_keywords": {},
        }

    user_promo_matches = get_user_promotional_matches(normalized)

    is_financial = get_financial_confidence(normalized) >= THRESHOLD
    is_subscription = get_subscription_confidence(normalized) >= THRESHOLD
    is_promotional = get_promotional_confidence(normalized) >= THRESHOLD
    is_shop = get_shop_confidence(normalized) >= THRESHOLD
    is_newsletter = get_newsletter_confidence(normalized) >= THRESHOLD

    categories = []
    if is_financial:
        categories.append("financial_risks")
    if is_subscription:
        categories.append("subscriptions")
    if is_shop:
        categories.append("shops")
    if is_newsletter:
        categories.append("newsletters")
    if is_promotional:
        categories.append("promotions")

    matched = {}
    if is_subscription:
        matched["subscription"] = get_matching_keywords(normalized, SUBSCRIPTION_KEYWORDS)
    if is_promotional:
        matched["promotional"] = get_matching_keywords(normalized, PROMO_KEYWORDS)
        if user_promo_matches:
            matched["user_rules"] = user_promo_matches
    if is_shop:
        matched["shops"] = get_matching_keywords(normalized, SHOP_KEYWORDS)
    if is_newsletter:
        matched["newsletters"] = get_matching_keywords(normalized, NEWSLETTER_KEYWORDS)
    if is_financial:
        matched["financial_risks"] = get_matching_keywords(normalized, FINANCIAL_KEYWORDS)

    return {
        "categories": categories,
        "is_subscription": is_subscription,
        "is_promotional": is_promotional,
        "is_shop": is_shop,
        "is_newsletter": is_newsletter,
        "is_financial_risk": is_financial,
        "matched_keywords": matched,
    }


# ============================================================
# Helper funkcijos
# ============================================================

def get_subscription_matches(content: str) -> list[str]:
    normalized = normalize_content(content)
    if should_ignore_email(normalized):
        return []
    return get_matching_keywords(normalized, SUBSCRIPTION_KEYWORDS)


def get_promotional_matches(content: str) -> list[str]:
    normalized = normalize_content(content)
    if should_ignore_email(normalized):
        return []

    keywords = PROMO_KEYWORDS + get_user_promo_senders() + get_user_promo_keywords()
    return get_matching_keywords(normalized, keywords)
