import html as html_lib
import re
import webbrowser
from urllib.parse import quote_plus, urlparse

from translations import t

SERVICE_CANCEL_URLS = {
    "anthropic": "https://console.anthropic.com/settings/billing",
    "claude": "https://claude.ai/settings/billing",
    "use ai": "https://use.ai/help/articles/subscription-cancellation",
    "use.ai": "https://use.ai/help/articles/subscription-cancellation",
    "chatgpt": "https://chatgpt.com/settings/subscription",
    "netflix": "https://www.netflix.com/CancelPlan",
    "spotify": "https://www.spotify.com/account/subscription/",
    "canva": "https://www.canva.com/settings/billing-and-plans",
    "hostinger": "https://hpanel.hostinger.com/billing",
}


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


def cancel_subscription(sender, email_id):
    """Lead the user toward cancelling: a known billing page, else the sender's
    own website, else (last resort) a search. FeeHunt never cancels for them."""
    service_key = _normalize_service_name(sender)
    display = _display_name(sender)

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
# Goal: instead of only leading the user to a billing help page or a
# Google search, scan the email body for a link that goes STRAIGHT to the
# cancellation / unsubscribe page, and surface it as one "Cancel now" button.
# The button opens immediately, so precision matters: we only accept links
# whose visible text or URL clearly express cancel-a-subscription intent.

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


def _score_link(text: str, href: str) -> int:
    """Higher = more clearly a 'cancel this subscription' link. 0 = reject."""
    blob = _normalize(f"{text} {href}")
    href_norm = _normalize(href)

    sub_context = any(
        word in blob
        for word in ("subscription", "membership", "auto renew", "auto-renew",
                     "autorenew", "prenumerat")
    )

    # Tier 3 (score 3) — unambiguous: the link text/URL says "unsubscribe"
    # or "cancel <subscription/plan/membership/trial>".
    if "unsubscribe" in blob or "atsisakyti prenumeratos" in blob:
        return 3
    if "cancel" in blob and any(
        word in blob for word in ("subscription", "plan", "membership", "trial",
                                  "auto renew", "auto-renew", "autorenew")
    ):
        return 3
    if any(verb in blob for verb in ("atsaukti", "atsisakyti", "nutraukti")) and "prenumerat" in blob:
        return 3
    # URL paths that are dedicated cancel endpoints.
    if any(token in href_norm for token in ("/cancelplan", "cancel-subscription",
                                            "cancelsubscription", "/unsubscribe", "optout",
                                            "opt-out")):
        return 3

    # Tier 2 (score 2) — "manage subscription" style: lands on the page where
    # the user cancels, even if it doesn't say "cancel" outright.
    if "manage" in blob and sub_context:
        return 2
    if "tvarkyti" in blob and "prenumerat" in blob:
        return 2
    if any(token in href_norm for token in ("manage-subscription", "managesubscription",
                                            "/account/subscription", "/subscription")):
        return 2

    return 0


def extract_direct_cancel_url(html_body: str) -> str | None:
    """Return the http(s) URL of the strongest cancel/unsubscribe link in the
    email HTML, or None if no confident match is found."""
    if not html_body:
        return None

    best_url = None
    best_score = 0

    for match in _ANCHOR_RE.finditer(html_body):
        href = html_lib.unescape(match.group("href").strip())
        parsed = urlparse(href)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            continue

        text = html_lib.unescape(_TAG_RE.sub(" ", match.group("text")))
        score = _score_link(text, href)
        if score > best_score:
            best_score = score
            best_url = href
            if score == 3:
                # Strongest possible; keep the first (usually the primary CTA).
                break

    return best_url
