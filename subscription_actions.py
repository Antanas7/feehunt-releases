import html as html_lib
import re
import webbrowser
from urllib.parse import quote_plus, urlparse

from translations import t

# Curated map of senders -> the exact page where THAT service is cancelled.
# Keys are matched as substrings of the normalized sender (display name + email),
# so short/common words use a domain fragment ("max.com") to avoid false hits.
# Prefer a real, stable billing/subscription page; when unsure, point at the
# account/billing root (right area, never a dead deep link).
SERVICE_CANCEL_URLS = {
    # AI tools
    "anthropic": "https://console.anthropic.com/settings/billing",
    "claude": "https://claude.ai/settings/billing",
    "use ai": "https://use.ai/help/articles/subscription-cancellation",
    "use.ai": "https://use.ai/help/articles/subscription-cancellation",
    "chatgpt": "https://chatgpt.com/settings/subscription",
    "openai": "https://chatgpt.com/settings/subscription",
    "grammarly": "https://account.grammarly.com/subscription",
    # Streaming / media
    "netflix": "https://www.netflix.com/CancelPlan",
    "spotify": "https://www.spotify.com/account/subscription/",
    "disney": "https://www.disneyplus.com/account/subscription",
    "hulu": "https://secure.hulu.com/account",
    "max.com": "https://play.max.com/account",
    "hbomax": "https://play.max.com/account",
    "paramount": "https://www.paramountplus.com/account/",
    "youtube": "https://www.youtube.com/paid_memberships",
    "audible": "https://www.audible.com/account/membership-details",
    "patreon": "https://www.patreon.com/settings/memberships",
    # Productivity / cloud
    "canva": "https://www.canva.com/settings/billing-and-plans",
    "adobe": "https://account.adobe.com/plans",
    "dropbox": "https://www.dropbox.com/account/plan",
    "google one": "https://one.google.com/settings",
    "linkedin": "https://www.linkedin.com/premium/manage/",
    "github": "https://github.com/settings/billing",
    # VPN / security
    "nordvpn": "https://my.nordaccount.com/billing/",
    "expressvpn": "https://www.expressvpn.com/subscriptions",
    # Web / hosting / domains
    "hostinger": "https://hpanel.hostinger.com/billing",
    "godaddy": "https://account.godaddy.com/subscriptions",
    "wix.com": "https://www.wix.com/account/subscriptions",
}

# Subscriptions billed THROUGH a platform (App Store, Google Play, PayPal, ...)
# share ONE exact cancellation hub no matter which app charged you. When the
# email comes from one of these billers, that hub is the most precise place to
# send the user - far better than the underlying app's own website. This is what
# covers the long tail of small, sneaky mobile/auto-pay subscriptions at once.
BILLING_INTERMEDIARIES = (
    {
        "name": "App Store",
        "url": "https://apps.apple.com/account/subscriptions",
        "markers": ("apple.com", "itunes.com"),
    },
    {
        "name": "Google Play",
        "url": "https://play.google.com/store/account/subscriptions",
        "markers": ("googleplay", "play.google.com"),
    },
    {
        "name": "PayPal",
        "url": "https://www.paypal.com/myaccount/autopay/",
        "markers": ("paypal.com", "paypal.lt"),
    },
    {
        "name": "Microsoft",
        "url": "https://account.microsoft.com/services",
        "markers": ("microsoft.com",),
    },
)


def billing_intermediary(sender):
    """If the email is billed through a known platform (App Store, Google Play,
    PayPal, Microsoft), return {"name", "url"} for that platform's exact
    cancellation hub, else None. Callers ensure the email is already a
    subscription/payment one, so the hub is always the right destination."""
    blob = (sender or "").lower()
    for platform in BILLING_INTERMEDIARIES:
        if any(marker in blob for marker in platform["markers"]):
            return {"name": platform["name"], "url": platform["url"]}
    return None


def _normalize_service_name(service_name):
    return " ".join((service_name or "").lower().replace("-", " ").split())


def _display_name(sender):
    """Human-friendly service name from a 'Name <a@b.com>' sender string."""
    name = (sender or "").split("<", 1)[0].strip()
    return name or (sender or "").strip()


# Generic mailbox providers — their root domain is not a place to cancel anything.
GENERIC_EMAIL_DOMAINS = {
    "gmail.com", "googlemail.com", "outlook.com", "hotmail.com", "live.com",
    "yahoo.com", "icloud.com", "me.com", "aol.com", "proton.me", "protonmail.com",
    "gmx.com", "mail.com", "yandex.com", "zoho.com",
}

# Second-level labels that mean the public suffix is two parts (e.g. example.co.uk).
_COMPOUND_SLDS = {"co", "com", "org", "net", "ac", "gov", "edu"}

_EMAIL_RE = re.compile(r"[\w.+-]+@([\w.-]+\.[a-z]{2,})", re.IGNORECASE)


def _registrable_domain(host):
    """Strip mail/marketing subdomains down to the registrable root, e.g.
    'support.porkbun.com' -> 'porkbun.com', 'email.netflix.com' -> 'netflix.com'."""
    labels = [part for part in host.lower().strip().strip(".").split(".") if part]
    if len(labels) <= 2:
        return ".".join(labels)
    if len(labels[-1]) == 2 and labels[-2] in _COMPOUND_SLDS:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def _sender_website(sender):
    """The sender's own root website, or None for generic mailbox providers."""
    match = _EMAIL_RE.search(sender or "")
    if not match:
        return None
    domain = _registrable_domain(match.group(1))
    if not domain or domain in GENERIC_EMAIL_DOMAINS:
        return None
    return domain


def sender_website_url(sender):
    """Public: the sender's own root website as an https URL, or None when the
    sender is a generic mailbox provider (gmail.com, ...) with no useful site."""
    domain = _sender_website(sender)
    return f"https://{domain}" if domain else None


def subscription_identity(sender):
    """A stable key identifying the SERVICE behind a sender, used to remember the
    user's cancellation decision across months and app restarts. Prefers the
    sender's registrable domain (e.g. 'netflix.com'); falls back to the normalized
    display name when the sender is a generic mailbox provider with no own domain.
    Two billing emails from the same service map to the same key."""
    domain = _sender_website(sender)
    if domain:
        return domain
    name = _normalize_service_name(_display_name(sender))
    return name or _normalize_service_name(sender) or "unknown-service"


def known_billing_url(sender):
    """The known billing/cancel page for this sender (Netflix, Spotify, ...),
    or None if the sender is not in the curated list."""
    service_key = _normalize_service_name(sender)
    for known_service, billing_url in SERVICE_CANCEL_URLS.items():
        if known_service in service_key:
            return billing_url
    return None


def cancel_subscription(sender, email_id):
    """Lead the user toward cancelling: a known billing page, else the sender's
    own website, else (last resort) a search. FeeHunt never cancels for them."""
    service_key = _normalize_service_name(sender)
    display = _display_name(sender)

    # Billed through a platform (App Store, Google Play, PayPal, ...)? That hub
    # is the single exact place to cancel, so it wins over everything else.
    intermediary = billing_intermediary(sender)
    if intermediary:
        webbrowser.open(intermediary["url"])
        return t("subscription.opened_billing").format(service_name=intermediary["name"])

    for known_service, billing_url in SERVICE_CANCEL_URLS.items():
        if known_service in service_key:
            webbrowser.open(billing_url)
            return t("subscription.opened_billing").format(service_name=display)

    domain = _sender_website(sender)
    if domain:
        webbrowser.open(f"https://{domain}")
        return t("subscription.opened_website").format(service_name=domain)

    search_url = (
        "https://www.google.com/search?q="
        + quote_plus(f"{display} billing subscription cancel account")
    )
    webbrowser.open(search_url)

    return t("subscription.opened_search").format(service_name=display)


# ============================================================
# Direct cancel / unsubscribe link extraction from email HTML
# ============================================================
#
# Goal: scan the email body for the link that goes STRAIGHT to where the user
# acts, and classify it by KIND, because the two are NOT the same thing:
#   - "cancel"      stops the paid plan / the charge,
#   - "unsubscribe" only stops the emails (it does NOT stop billing).
# Presenting an unsubscribe link as "Cancel now" is exactly the deception
# FeeHunt exists to stop, so we keep the two kinds strictly separate and only
# ever let a real cancel link be shown as a cancellation.

_ANCHOR_RE = re.compile(
    r'<a\b[^>]*?\bhref\s*=\s*(["\'])(?P<href>.*?)\1[^>]*>(?P<text>.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")

# Lithuanian diacritics -> ASCII, so "atšaukti" also matches "atsaukti".
_DIACRITIC_MAP = str.maketrans({
    "ą": "a", "č": "c", "ę": "e", "ė": "e", "į": "i",
    "š": "s", "ų": "u", "ū": "u", "ž": "z",
})


def _normalize(value: str) -> str:
    return _WS_RE.sub(" ", (value or "").lower().translate(_DIACRITIC_MAP)).strip()


def _classify_link(text: str, href: str) -> tuple[str | None, int]:
    """Classify a single link. Returns (kind, score):
        kind  = "cancel"      -> stops the paid plan / charge,
                "unsubscribe" -> only stops emails,
                None          -> not a relevant action link.
        score = confidence (higher wins within the same kind)."""
    blob = _normalize(f"{text} {href}")
    href_norm = _normalize(href)

    # Documentation / help / info pages are never where you actually click
    # "cancel" — they only describe billing. Leading the user there sends them
    # in circles (e.g. KlingAI's "Billing Info" docs), so reject them outright
    # and let the wizard fall back to the real account page.
    if any(marker in href_norm for marker in (
        "/docs", "docs.", "/doc/", "/help/", "/help-", "help-center", "helpcenter",
        "/support", "/faq", "/guide", "/articles", "/article/", "/knowledge",
        "/kb/", "/blog", "/learn", "release-notes", "/billing-info", "billing_info",
        "/developer", "/api/", "/api-",
    )):
        return (None, 0)

    # --- Unsubscribe FIRST: stops emails only, never a billing cancellation. ---
    # Checked before cancel so that ambiguous wording ("atsisakyti prenumeratos",
    # i.e. newsletter opt-out) lands on the weaker, safer claim.
    if "unsubscribe" in blob or "atsisakyti prenumeratos" in blob:
        return ("unsubscribe", 3)
    if any(token in href_norm for token in ("/unsubscribe", "optout", "opt-out",
                                            "/email-preferences", "/emailpreferences")):
        return ("unsubscribe", 3)
    if any(phrase in blob for phrase in ("email preferences", "manage preferences",
                                         "email settings", "notification settings")):
        return ("unsubscribe", 2)

    # --- Cancel: actually stops the subscription / the charge. ---
    sub_context = any(
        word in blob
        for word in ("subscription", "membership", "auto renew", "auto-renew",
                     "autorenew", "prenumerat", "plan")
    )
    # "cancel" is specific enough to pair with any subscription word loosely
    # (e.g. "Cancel" button text + "subscription" in the URL).
    if "cancel" in blob and any(
        word in blob for word in ("subscription", "plan", "membership", "trial",
                                  "auto renew", "auto-renew", "autorenew")
    ):
        return ("cancel", 3)
    # "end"/"stop"/"turn off" are loose substrings (sender, recommend, ...), so
    # only accept them as explicit, adjacent cancel phrases.
    if any(phrase in blob for phrase in (
        "end subscription", "end your subscription", "end membership",
        "stop subscription", "stop your subscription", "stop membership",
        "turn off auto renew", "turn off auto-renew", "turn off automatic renewal",
    )):
        return ("cancel", 3)
    if any(verb in blob for verb in ("atsaukti", "nutraukti")) and "prenumerat" in blob:
        return ("cancel", 3)
    # URL paths that are dedicated cancel endpoints.
    if any(token in href_norm for token in ("/cancelplan", "cancel-subscription",
                                            "cancelsubscription", "cancel_subscription",
                                            "cancelmembership", "cancel-membership",
                                            "stopsubscription", "end-subscription")):
        return ("cancel", 3)

    # "Manage subscription / billing" style: lands on the page where you cancel.
    if ("manage" in blob or "billing" in blob) and sub_context:
        return ("cancel", 2)
    if "tvarkyti" in blob and "prenumerat" in blob:
        return ("cancel", 2)
    if any(token in href_norm for token in ("manage-subscription", "managesubscription",
                                            "manage-plan", "/account/subscription",
                                            "/account/subscriptions", "/account/billing",
                                            "/billing/subscription", "/myaccount/autopay",
                                            "/subscription", "/subscriptions")):
        return ("cancel", 2)

    return (None, 0)


def classify_cancel_links(html_body: str) -> dict[str, str | None]:
    """Scan the email HTML and return the strongest link of each kind:
    {"cancel_url": <stops the charge> or None,
     "unsubscribe_url": <stops the emails> or None}."""
    best = {"cancel": (None, 0), "unsubscribe": (None, 0)}
    if not html_body:
        return {"cancel_url": None, "unsubscribe_url": None}

    for match in _ANCHOR_RE.finditer(html_body):
        href = html_lib.unescape(match.group("href").strip())
        parsed = urlparse(href)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            continue
        text = html_lib.unescape(_TAG_RE.sub(" ", match.group("text")))
        kind, score = _classify_link(text, href)
        if kind and score > best[kind][1]:
            best[kind] = (href, score)

    return {"cancel_url": best["cancel"][0], "unsubscribe_url": best["unsubscribe"][0]}


def extract_direct_cancel_url(html_body: str) -> str | None:
    """Return the strongest TRUE-cancel link (stops the charge) in the email,
    or None. Unsubscribe-only links are deliberately excluded — they belong to
    a separate, honestly-labelled 'stop the emails' action."""
    return classify_cancel_links(html_body)["cancel_url"]
