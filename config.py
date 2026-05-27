import os
import sys
from pathlib import Path


# ============================================================
# FeeHunt produkto informacija
# ============================================================

APP_NAME = "FeeHunt"
APP_VERSION = "1.2.0-beta"
APP_STAGE = "Smart Cleanup MVP"
APP_TAGLINE = "Nebereikia bėgti nuo savo el. pašto. FeeHunt padeda susigrąžinti kontrolę."


# ============================================================
# Failų keliai
# ============================================================

def get_resource_dir() -> Path:
    """Return the bundled app/resource directory."""
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass).resolve()

    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        internal_dir = exe_dir / "_internal"
        return internal_dir if internal_dir.exists() else exe_dir

    return Path(__file__).resolve().parent


def get_user_data_dir() -> Path:
    """Return the writable per-user FeeHunt folder."""
    base = os.environ.get("APPDATA") or os.environ.get("LOCALAPPDATA")
    return Path(base) / APP_NAME if base else Path.home() / ".FeeHunt"


RESOURCE_DIR = get_resource_dir()
APP_DIR = RESOURCE_DIR
USER_DATA_DIR = get_user_data_dir()


def get_oauth_credentials_file() -> Path:
    """Find the Gmail OAuth client configuration bundled with the app."""
    candidates = [
        RESOURCE_DIR / "credentials.json",
        RESOURCE_DIR / "_internal" / "credentials.json",
        Path.cwd() / "credentials.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


GMAIL_CREDENTIALS_FILE = get_oauth_credentials_file()
GMAIL_TOKEN_FILE = USER_DATA_DIR / "token.json"
LAST_SCAN_RESULTS_FILE = USER_DATA_DIR / "last_scan_results.json"
MEMORY_FILE = USER_DATA_DIR / "feehunt_memory.json"
SETTINGS_FILE = USER_DATA_DIR / "feehunt_settings.json"
RULES_FILE = USER_DATA_DIR / "feehunt_rules.json"
LICENSE_FILE = USER_DATA_DIR / "feehunt_license.json"
LICENSE_SESSION_FILE = USER_DATA_DIR / "feehunt_session.json"
LICENSING_API_BASE_URL = os.environ.get("FEEHUNT_API_BASE_URL", "https://feehunt.pro/api")


# ============================================================
# Gmail OAuth
# ============================================================

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


# ============================================================
# Gmail skenavimo nustatymai
# ============================================================

MAX_EMAILS_TO_SCAN = 200
MAX_EMAILS_PER_TARGETED_QUERY = 80

GMAIL_TARGETED_SCAN_QUERIES = [
    'newer_than:365d -in:trash "payment failed"',
    'newer_than:365d -in:trash "failed payment"',
    'newer_than:365d -in:trash "failed to process"',
    'newer_than:365d -in:trash "insufficient funds"',
    'newer_than:365d -in:trash "card declined"',
    'newer_than:365d -in:trash "payment required"',
    'newer_than:365d -in:trash "past due"',
    'newer_than:365d -in:trash overdue',
    'newer_than:365d -in:trash subscription',
    'newer_than:365d -in:trash billing',
    'newer_than:365d -in:trash renewal',
    'newer_than:365d -in:trash "recurring payment"',
    'newer_than:365d -in:trash "auto-renew"',
    'newer_than:365d -in:trash invoice',
    'newer_than:365d -in:trash membership',
]
GMAIL_USER_ID = "me"
GMAIL_MESSAGE_FORMAT = "full"


# ============================================================
# Finansiniai nustatymai
# ============================================================

DEFAULT_CURRENCY = "USD"
DEFAULT_ESTIMATED_SAVINGS_PER_SUBSCRIPTION = 15

SUPPORTED_CURRENCIES = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
}


# ============================================================
# Produkto nustatymai
# ============================================================

SUPPORTED_LANGUAGES = ["English", "Lietuvių"]

DEFAULT_SETTINGS = {
    "language": "en",
    "timezone": "",
    "currency": DEFAULT_CURRENCY,
    "auto_scan": "off",
    "safe_mode": True,
    "max_dashboard_items": 3,
    "apply_rules_after_scan": False,
    # Default ON: once user puts a sender on the unwanted list, the
    # natural expectation is "FeeHunt will delete their stuff". User can
    # switch to "ask me first" in Sender Lists if they want safer review.
    "auto_apply_blacklist_after_scan": True,
    "ftue_completed": False,
    "adaptive_guidance_enabled": True,
}


# ============================================================
# Email kategorijos
# ============================================================

EMAIL_CATEGORIES = [
    {
        "id": "promotions",
        "label": "Reklaminiai laiškai",
        "icon": "📢",
        "description": "Akcijos, nuolaidos, specialūs pasiūlymai",
        "default_action": "ask",
        "protected": False,
    },
    {
        "id": "shops",
        "label": "Internetinių parduotuvių pasiūlymai",
        "icon": "🛒",
        "description": "Amazon, eBay, AliExpress ir kitos parduotuvės",
        "default_action": "ask",
        "protected": False,
    },
    {
        "id": "newsletters",
        "label": "Naujienlaiškiai",
        "icon": "📰",
        "description": "Reguliarūs informaciniai laiškai, tinklaraščiai",
        "default_action": "ask",
        "protected": False,
    },
    {
        "id": "subscriptions",
        "label": "Prenumeratos",
        "icon": "🔄",
        "description": "Pasikartojantys mokėjimai, paslaugų prenumeratos",
        "default_action": "notify",
        "protected": False,
    },
    {
        "id": "financial_risks",
        "label": "Finansinės grėsmės",
        "icon": "💳",
        "description": "Nepavykę mokėjimai, kortelių problemos, skolos",
        "default_action": "notify",
        "protected": True,
    },
]

# Galimi veiksmai
CATEGORY_ACTIONS = {
    "delete": "🗑 Automatiškai ištrinti",
    "archive": "📥 Automatiškai archyvuoti",
    "ask": "❓ Paklausti manęs",
    "notify": "🔔 Tik informuoti",
    "ignore": "👁 Ignoruoti",
}

PROTECTED_CATEGORY_ALLOWED_ACTIONS = ["notify"]


# ============================================================
# Numatytosios taisyklės
# ============================================================

DEFAULT_RULES = {
    "category_actions": {
        "promotions": "ask",
        "shops": "ask",
        "newsletters": "ask",
        "subscriptions": "notify",
        "financial_risks": "notify",
    },
    "whitelist": [],
    "blacklist": [],
    "custom_categories": [],
}


# ============================================================
# Raktažodžiai analizatoriui
# ============================================================

KEYWORDS = {
    "subscription": [
        "subscription", "billing", "payment", "invoice", "renewal",
        "charged", "charge", "trial", "plan", "membership",
        "recurring payment", "auto-renew", "auto renewal",
        "failed payment", "payment failed", "payment failed to process",
        "failed to process", "card declined", "insufficient funds",
        "insufficient funds on card", "past due", "overdue", "receipt", "statement",
        "prenumerata", "prenumeratos", "mokėjimas", "mokejimas",
        "sąskaita", "saskaita", "atnaujinimas",
        "nepavyko apmokėti", "kortelė atmesta", "kortele atmesta",
        "vėluojantis mokėjimas", "veluojantis mokejimas",
    ],
    "promotional": [
        "sale", "discount", "offer", "limited time", "deal",
        "promotion", "promo", "coupon", "save", "black friday",
        "cyber monday", "special offer", "newsletter", "unsubscribe",
        "marketing", "exclusive deal", "clearance",
        "reklama", "nuolaida", "pasiūlymas", "pasiulymas",
        "akcija", "išpardavimas", "ispardavimas",
        "naujienlaiškis", "atsisakyti prenumeratos",
    ],
    "shops": [
        "amazon", "ebay", "aliexpress", "etsy", "shopify",
        "your order", "order confirmation", "shipping confirmation",
        "your package", "delivery", "track your order",
        "jūsų užsakymas", "užsakymo patvirtinimas", "pristatymas",
    ],
    "newsletters": [
        "newsletter", "unsubscribe", "manage preferences",
        "email preferences", "you are receiving this",
        "naujienlaiškis", "atsisakyti", "prenumeruoti",
        "weekly digest", "monthly update", "roundup",
    ],
    "financial_risks": [
        "failed payment", "payment failed", "payment failed to process",
        "failed to process", "card declined", "insufficient funds",
        "insufficient funds on card", "past due", "overdue",
        "account suspended", "payment required", "action required",
        "nepavyko apmokėti", "kortelė atmesta", "kortele atmesta",
        "vėluojantis mokėjimas", "paskyra sustabdyta",
    ],
}

HIGH_CONFIDENCE_SUBSCRIPTION_KEYWORDS = [
    "recurring payment", "auto-renew", "auto renewal",
    "failed payment", "payment failed", "payment failed to process",
    "failed to process", "card declined", "insufficient funds",
    "insufficient funds on card", "past due", "overdue",
    "nepavyko apmokėti", "kortelė atmesta", "kortele atmesta",
    "vėluojantis mokėjimas", "veluojantis mokejimas",
]

HIGH_CONFIDENCE_PROMOTIONAL_KEYWORDS = [
    "black friday", "cyber monday", "special offer",
    "exclusive deal", "limited time", "newsletter", "naujienlaiškis",
]

HIGH_CONFIDENCE_SHOP_KEYWORDS = [
    "order confirmation", "shipping confirmation",
    "track your order", "your package", "užsakymo patvirtinimas",
]

HIGH_CONFIDENCE_FINANCIAL_KEYWORDS = [
    "failed payment", "payment failed", "payment failed to process",
    "failed to process", "card declined", "insufficient funds",
    "insufficient funds on card", "past due", "overdue", "account suspended",
    "nepavyko apmokėti", "kortelė atmesta", "paskyra sustabdyta",
]


# ============================================================
# Saugumo nustatymai
# ============================================================

SAFE_MODE_DEFAULT = True
ALLOW_BULK_DELETE = True
ALLOW_MARK_AS_SPAM = True
ALLOW_ARCHIVE = True
ALLOW_IMPORTANT_MARKING = True

CLEANUP_RULES = {
    "auto_archive_promotions": False,
    "auto_delete_promotions": False,
    "auto_mark_spam": False,
    "protect_important_senders": True,
}
