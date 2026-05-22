import sys
from pathlib import Path


# ============================================================
# FeeHunt produkto informacija
# ============================================================

APP_NAME = "FeeHunt"
APP_VERSION = "0.3.0-beta"
APP_STAGE = "Smart Cleanup MVP"
APP_TAGLINE = "Nebereikia bėgti nuo savo el. pašto. FeeHunt padeda susigrąžinti kontrolę."


# ============================================================
# Failų keliai
# ============================================================

def get_app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "_internal"
    return Path(__file__).resolve().parent


APP_DIR = get_app_dir()

GMAIL_CREDENTIALS_FILE = APP_DIR / "credentials.json"
GMAIL_TOKEN_FILE = APP_DIR / "token.json"
LAST_SCAN_RESULTS_FILE = APP_DIR / "last_scan_results.json"
SETTINGS_FILE = APP_DIR / "feehunt_settings.json"
RULES_FILE = APP_DIR / "feehunt_rules.json"


# ============================================================
# Gmail OAuth
# ============================================================

GMAIL_SCOPES = ["https://mail.google.com/"]


# ============================================================
# Gmail skenavimo nustatymai
# ============================================================

MAX_EMAILS_TO_SCAN = 200
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
    "currency": DEFAULT_CURRENCY,
    "auto_scan": "off",
    "safe_mode": True,
    "max_dashboard_items": 3,
    "apply_rules_after_scan": False,
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
        "failed payment", "payment failed", "card declined",
        "past due", "overdue", "receipt", "statement",
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
        "failed payment", "payment failed", "card declined",
        "past due", "overdue", "account suspended", "payment required",
        "nepavyko apmokėti", "kortelė atmesta", "kortele atmesta",
        "vėluojantis mokėjimas", "paskyra sustabdyta",
    ],
}

HIGH_CONFIDENCE_SUBSCRIPTION_KEYWORDS = [
    "recurring payment", "auto-renew", "auto renewal",
    "failed payment", "payment failed", "card declined",
    "past due", "overdue",
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
    "failed payment", "payment failed", "card declined",
    "past due", "overdue", "account suspended",
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
