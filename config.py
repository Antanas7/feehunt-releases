import os
import sys
from pathlib import Path


# ============================================================
# FeeHunt produkto informacija
# ============================================================

APP_NAME = "FeeHunt"
APP_VERSION = "1.12.3"
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

# Tester accounts: when one of these Gmail addresses is the connected inbox, the
# trial scan-quota and trial-date limits are lifted locally (in memory only, never
# written to disk) so the maker can test repeatedly without burning scan credits.
# Comma-separated emails in FEEHUNT_TESTER_EMAILS are merged in at runtime.
TESTER_EMAILS = {
    "lofotendreamss@gmail.com",
    "rasyte7777a@gmail.com",
}


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
    # Block-senders feature removed (Gmail already blocks senders; FeeHunt's
    # value is recurring detect → show → assisted cleanup). Kept as False so
    # any stale reference never auto-trashes by sender.
    "auto_apply_blacklist_after_scan": False,
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
    # Senders the user marks as unwanted: the scan RECOGNISES their mail as
    # promotional (categorises it as junk) so the user can clean it normally.
    # Never blocks delivery, never auto-deletes by sender. (The old "blacklist"
    # key is kept dead for back-compat and is no longer read by the scanner.)
    "unwanted_senders": [],
    "blacklist": [],
    "custom_categories": [],
}


# ============================================================
# Raktažodžiai analizatoriui
# ============================================================

KEYWORDS = {
    "subscription": [
        # English
        "subscription", "billing", "payment", "invoice", "renewal",
        "charged", "charge", "trial", "plan", "membership",
        "recurring payment", "auto-renew", "auto renewal", "auto-renews",
        "renews on", "renews soon", "your plan", "monthly plan", "annual plan",
        "next billing", "billing cycle", "receipt", "statement",
        "thank you for subscribing", "your subscription",
        # Failure signals (also flagged as financial_risks)
        "failed payment", "payment failed", "payment failed to process",
        "failed to process", "card declined", "insufficient funds",
        "insufficient funds on card", "past due", "overdue",
        # Lithuanian
        "prenumerata", "prenumeratos", "prenumeratą", "prenumeratos atnaujinimas",
        "mokėjimas", "mokejimas", "sąskaita", "saskaita", "atnaujinimas",
        "narystė", "naryste", "metinis planas", "mėnesinis planas", "menesinis planas",
        "nepavyko apmokėti", "nepavyko apmoketi",
        "kortelė atmesta", "kortele atmesta",
        "vėluojantis mokėjimas", "veluojantis mokejimas",
        "kvitas",
    ],
    "promotional": [
        # English - sales/discount
        "sale", "discount", "offer", "limited time", "limited offer",
        "deal", "deals", "promotion", "promo", "coupon", "coupon code",
        "save", "save up to", "black friday", "cyber monday",
        "special offer", "exclusive deal", "exclusive offer", "members only",
        "clearance", "buy 1 get", "buy one get", "free shipping",
        # English - lifestyle marketing patterns
        "shop now", "shop the", "shop our", "new arrivals", "new in",
        "back in stock", "best price", "for you", "you deserve",
        "your weekly", "weekly picks", "trending", "treat yourself",
        "view in browser", "view online", "view this email", "view email",
        "weekly briefing", "weekly digest", "weekly newsletter",
        "the frontier", "live weekly", "join us", "polly wants",
        "make a", "obsessed", "inspo", "for your inbox",
        # CTA hints often seen in marketing
        "browse the", "shop the look", "shop this", "see more", "see all",
        "explore the", "explore our",
        # Newsletter wrappers
        "newsletter", "unsubscribe", "marketing", "preferences",
        # Lithuanian
        "reklama", "reklaminis", "nuolaida", "nuolaidos",
        "pasiūlymas", "pasiulymas", "pasiulymai", "pasiūlymai",
        "akcija", "akcijos", "išpardavimas", "ispardavimas", "išparduotuvė",
        "naujienlaiškis", "naujienlaiskis", "atsisakyti prenumeratos",
        "specialus pasiūlymas", "specialus pasiulymas",
        "tik šiandien", "tik siandien", "išskirtinis", "isskirtinis",
        "nemokamas pristatymas", "naujausi", "populiariausi",
        "tau", "tavo", "perziurėk", "perziureti narsykleje",
    ],
    "shops": [
        # English - storefronts
        "amazon", "ebay", "aliexpress", "etsy", "shopify",
        "wayfair", "ikea", "asos", "zalando", "temu", "shein",
        # English - order lifecycle
        "your order", "order confirmation", "order shipped",
        "order delivered", "shipping confirmation", "your package",
        "your shipment", "out for delivery", "delivery confirmation",
        "track your order", "tracking number", "your cart",
        "items in your cart", "left in your cart", "complete your purchase",
        "wishlist", "back in stock alert",
        # Norwegian (user inbox has Tonerweb, Starlink emails)
        "din bestilling", "ordrebekreftelse", "bestillingen er bekreftet",
        "leveranse", "pakke", "sporing",
        # Lithuanian
        "jūsų užsakymas", "jusu uzsakymas", "užsakymas",
        "užsakymo patvirtinimas", "uzsakymo patvirtinimas",
        "pristatymas", "siunta", "krepšelis", "krepselis",
        "prekė", "preke", "parduotuvė", "parduotuve",
    ],
    "newsletters": [
        # English
        "newsletter", "unsubscribe", "manage preferences", "manage your preferences",
        "email preferences", "update your preferences",
        "you are receiving this", "you're receiving this", "youre receiving this",
        "you received this", "this email was sent",
        "weekly digest", "monthly update", "monthly newsletter",
        "weekly briefing", "weekly roundup", "monthly roundup", "roundup",
        "today's headlines", "the leaderboard", "this week", "this month in",
        "the daily", "daily digest", "daily newsletter",
        # Lithuanian
        "naujienlaiškis", "naujienlaiskis", "atsisakyti",
        "prenumeruoti", "valdyti prenumerata", "valdyti prenumeratą",
        "savaitės naujienos", "savaites naujienos", "mėnesio apžvalga",
        "kassavaitinis", "kasdieninis",
    ],
    "financial_risks": [
        # English - failed payments
        "failed payment", "payment failed", "payment failed to process",
        "failed to process", "card declined", "insufficient funds",
        "insufficient funds on card", "past due", "overdue",
        "account suspended", "subscription paused",
        "payment required", "payment method needs", "update your payment",
        # English - account/identity verification (phishing-adjacent)
        "action required", "verify your identity", "verify your account",
        "confirm your identity", "confirm your account",
        "biometric verification", "set up biometric",
        "security alert", "unusual sign-in", "suspicious sign-in",
        "suspicious activity", "unauthorized access", "unauthorized sign",
        "account locked", "your account has been locked",
        "regulatory compliance", "kyc verification", "identity verification",
        "click here to verify", "verify now", "verification required",
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
    # English
    "black friday", "cyber monday", "special offer", "exclusive offer",
    "exclusive deal", "limited time", "limited offer", "newsletter",
    "view in browser", "view online", "shop now", "shop the",
    "weekly briefing", "view this email", "you deserve",
    "treat yourself", "back in stock", "new arrivals", "hot picks",
    "this week's hot", "this week’s hot", "hot deals",
    "% off", "% rabatt", "30% off", "50% off",
    # Norwegian / Danish / Swedish (Skandinavian promos)
    "tilbud", "rabatt", "opptil", "kampanje", "tilbudet", "spar penger",
    "se tilbudet", "kjøp nå", "kjop na", "kun i dag",
    "se vårt utvalg", "se vart utvalg",
    # Lithuanian
    "naujienlaiškis", "specialus pasiūlymas",
]

HIGH_CONFIDENCE_SHOP_KEYWORDS = [
    "order confirmation", "shipping confirmation", "tracking number",
    "track your order", "your package", "your shipment",
    "out for delivery", "ordrebekreftelse", "ordren er bekreftet",
    "din ordre", "din bestilling", "užsakymo patvirtinimas",
]

HIGH_CONFIDENCE_FINANCIAL_KEYWORDS = [
    "failed payment", "payment failed", "payment failed to process",
    "failed to process", "card declined", "insufficient funds",
    "insufficient funds on card", "past due", "overdue", "account suspended",
    "action required", "verify your identity", "verify your account",
    "biometric verification", "security alert", "suspicious activity",
    "unauthorized access", "account locked", "regulatory compliance",
    "kyc verification",
    "nepavyko apmokėti", "kortelė atmesta", "paskyra sustabdyta",
    "patvirtinkite tapatybę", "saugumo įspėjimas", "įtartina veikla",
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
