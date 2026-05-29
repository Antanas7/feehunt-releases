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


def cancel_subscription(service_name, email_id):
    service_key = _normalize_service_name(service_name)

    for known_service, billing_url in SERVICE_CANCEL_URLS.items():
        if known_service in service_key:
            webbrowser.open(billing_url)
            return t("subscription.opened_billing").format(service_name=service_name)

    search_url = (
        "https://www.google.com/search?q="
        + quote_plus(f"{service_name} billing subscription cancel account")
    )
    webbrowser.open(search_url)

    return t("subscription.opened_search").format(service_name=service_name)


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
