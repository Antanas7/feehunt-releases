"""Local, privacy-safe phishing detection for FeeHunt.

Phase 1 of FeeHunt v2.0: every check here runs 100% on the user's computer.
Nothing is sent to any external service. The goal is a small set of
*high-precision* signals — a false "this is phishing" alarm on a legit email
erodes trust, so we prefer to miss a borderline case over crying wolf.

Each detected signal is returned as a language-agnostic reason
``{"code": str, "params": dict}`` so the UI/translation layer can render it in
the user's own language ("the sender's name says PayPal, but it was sent from
xyz.ru").
"""

from __future__ import annotations

import re
from email.utils import parseaddr
from urllib.parse import urlparse


# ------------------------------------------------------------------
# Known brands → their legitimate domains
# ------------------------------------------------------------------
# Used for: (a) display-name vs domain mismatch, (b) brand name hidden inside a
# non-legit domain. Only reasonably distinctive brand tokens belong here —
# generic English words ("apple" aside) would cause false positives.

BRAND_DOMAINS: dict[str, set[str]] = {
    "paypal": {"paypal.com"},
    "google": {"google.com", "gmail.com", "googlemail.com", "youtube.com"},
    "microsoft": {"microsoft.com", "outlook.com", "live.com", "hotmail.com",
                  "office.com", "microsoftonline.com"},
    "apple": {"apple.com", "icloud.com"},
    "amazon": {"amazon.com", "amazon.co.uk", "amazon.de", "amazon.lt", "amazonses.com"},
    "netflix": {"netflix.com"},
    "facebook": {"facebook.com", "facebookmail.com", "fb.com"},
    "instagram": {"instagram.com", "mail.instagram.com"},
    "whatsapp": {"whatsapp.com"},
    "linkedin": {"linkedin.com"},
    "binance": {"binance.com"},
    "coinbase": {"coinbase.com"},
    "revolut": {"revolut.com"},
    "spotify": {"spotify.com"},
    "swedbank": {"swedbank.lt", "swedbank.com"},
    "luminor": {"luminor.lt"},
    "paysera": {"paysera.com", "paysera.lt"},
}

# Every legitimate domain, flattened, for the lookalike comparison.
ALL_LEGIT_DOMAINS: set[str] = {domain for domains in BRAND_DOMAINS.values() for domain in domains}

# Display labels for brands whose casing differs from a plain capitalize().
BRAND_LABELS = {"paypal": "PayPal", "linkedin": "LinkedIn", "whatsapp": "WhatsApp"}


def _brand_label(brand: str) -> str:
    return BRAND_LABELS.get(brand, brand.capitalize())

# Common homoglyph / leetspeak substitutions used by typosquatters.
HOMOGLYPHS = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "8": "b"})

URGENCY_PHRASES = [
    # English
    "act now", "action required", "immediately", "within 24 hours", "within 24h",
    "account suspended", "account locked", "account blocked", "account will be",
    "final notice", "last warning", "urgent", "verify now", "respond now",
    "limited time", "your access will be", "avoid suspension",
    # Lithuanian
    "veikite dabar", "neatidėliotinas veiksmas", "neatideliotinas veiksmas",
    "nedelsiant", "per 24 valandas", "skubu", "skubiai",
    "paskyra užblokuota", "paskyra uzblokuota", "paskyra sustabdyta",
    "paskutinis įspėjimas", "paskutinis ispejimas", "patvirtinkite dabar",
]

CREDENTIAL_PHRASES = [
    # English
    "verify your account", "verify your identity", "confirm your identity",
    "confirm your account", "confirm your password", "enter your password",
    "update your payment", "update your billing", "confirm your details",
    "log in to", "sign in to", "click here to verify", "validate your account",
    # Lithuanian
    "patvirtinkite tapatybę", "patvirtinkite tapatybe",
    "patvirtinkite paskyrą", "patvirtinkite paskyra",
    "patvirtinkite duomenis", "įveskite slaptažodį", "iveskite slaptazodi",
    "atnaujinkite mokėjimą", "atnaujinkite mokejima", "prisijunkite",
]

_LINK_RE = re.compile(
    r'<a\s[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
_TAG_RE = re.compile(r"<[^>]+>")
_DOMAIN_IN_TEXT_RE = re.compile(r"([a-z0-9][a-z0-9.-]*\.[a-z]{2,})")

STRONG_CODES = {"name_domain_mismatch", "lookalike_domain", "hidden_link"}


# ------------------------------------------------------------------
# Small helpers
# ------------------------------------------------------------------

def extract_sender_parts(raw_from: str) -> tuple[str, str, str]:
    """Return (display_name, email, host) parsed from a raw From header."""
    name, email = parseaddr(raw_from or "")
    email = email.strip().lower()
    host = email.split("@", 1)[1] if "@" in email else ""
    return name.strip(), email, host


def _host_matches(host: str, legit: str) -> bool:
    return host == legit or host.endswith("." + legit)


def _is_legit_host(host: str) -> bool:
    return any(_host_matches(host, legit) for legit in ALL_LEGIT_DOMAINS)


def _same_site(a: str, b: str) -> bool:
    if not a or not b:
        return True
    return a == b or a.endswith("." + b) or b.endswith("." + a)


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            current.append(min(
                previous[j] + 1,
                current[j - 1] + 1,
                previous[j - 1] + (ca != cb),
            ))
        previous = current
    return previous[-1]


def _word_in(token: str, text: str) -> bool:
    return re.search(rf"\b{re.escape(token)}\b", text) is not None


# ------------------------------------------------------------------
# Individual checks
# ------------------------------------------------------------------

def _check_name_domain_mismatch(name: str, host: str) -> dict | None:
    """STRONG: display name claims a brand, but the email is not from that brand."""
    if not name or not host:
        return None
    name_lower = name.lower()
    for brand, domains in BRAND_DOMAINS.items():
        if not _word_in(brand, name_lower):
            continue
        if any(_host_matches(host, legit) for legit in domains):
            return None  # name brand matches a legit domain → genuine
        return {"code": "name_domain_mismatch", "params": {"brand": _brand_label(brand), "domain": host}}
    return None


def _check_lookalike_domain(host: str) -> dict | None:
    """STRONG: the sending domain imitates a real brand domain (paypa1.com)."""
    if not host or _is_legit_host(host):
        return None
    normalized = host.translate(HOMOGLYPHS)
    for legit in ALL_LEGIT_DOMAINS:
        if normalized == legit.translate(HOMOGLYPHS) and host != legit:
            return {"code": "lookalike_domain", "params": {"domain": host, "legit": legit}}
        label = legit.split(".", 1)[0]
        if len(label) >= 6 and _levenshtein(host, legit) <= 1:
            return {"code": "lookalike_domain", "params": {"domain": host, "legit": legit}}
    return None


def _check_brand_in_domain(host: str) -> dict | None:
    """WEAK: a brand name is buried in a non-legit domain (paypal-secure.com)."""
    if not host or _is_legit_host(host):
        return None
    for brand, domains in BRAND_DOMAINS.items():
        if len(brand) < 6:
            continue  # too short → risk of coincidental matches
        if not _word_in(brand, host):
            continue
        if any(_host_matches(host, legit) for legit in domains):
            return None
        return {"code": "brand_in_domain", "params": {"brand": _brand_label(brand), "domain": host}}
    return None


def _check_hidden_links(html_body: str) -> dict | None:
    """STRONG: a link's visible text shows one domain but it leads to another."""
    if not html_body:
        return None
    for href, inner in _LINK_RE.findall(html_body):
        href = href.strip()
        if not href.lower().startswith(("http://", "https://")):
            continue
        shown_text = _TAG_RE.sub("", inner).strip().lower()
        match = _DOMAIN_IN_TEXT_RE.search(shown_text)
        if not match:
            continue
        shown_host = match.group(1).rstrip(".")
        actual_host = urlparse(href).netloc.lower().split(":", 1)[0]
        if actual_host.startswith("www."):
            actual_host = actual_host[4:]
        if shown_host.startswith("www."):
            shown_host = shown_host[4:]
        if actual_host and not _same_site(shown_host, actual_host):
            return {"code": "hidden_link", "params": {"shown": shown_host, "actual": actual_host}}
    return None


def _check_urgency_credentials(text: str) -> dict | None:
    """WEAK: pressure to act fast AND a request for credentials/payment."""
    has_urgency = any(phrase in text for phrase in URGENCY_PHRASES)
    asks_credentials = any(phrase in text for phrase in CREDENTIAL_PHRASES)
    if has_urgency and asks_credentials:
        return {"code": "urgency_credentials", "params": {}}
    return None


# ------------------------------------------------------------------
# Public entry point
# ------------------------------------------------------------------

def analyze_phishing(
    sender_raw: str,
    subject: str = "",
    body_text: str = "",
    html_body: str = "",
) -> dict:
    """Return {"is_phishing_risk": bool, "reasons": [{"code", "params"}, ...]}.

    Risk is flagged when at least one STRONG signal fires, or at least two
    independent WEAK signals do. Reasons are deduplicated by code.
    """
    name, _email, host = extract_sender_parts(sender_raw)
    text = f"{subject}\n{body_text}".lower()

    candidates = [
        _check_name_domain_mismatch(name, host),
        _check_lookalike_domain(host),
        _check_hidden_links(html_body),
        _check_brand_in_domain(host),
        _check_urgency_credentials(text),
    ]

    reasons: list[dict] = []
    seen_codes: set[str] = set()
    for reason in candidates:
        if reason and reason["code"] not in seen_codes:
            seen_codes.add(reason["code"])
            reasons.append(reason)

    strong = [r for r in reasons if r["code"] in STRONG_CODES]
    weak = [r for r in reasons if r["code"] not in STRONG_CODES]
    is_risk = bool(strong) or len(weak) >= 2

    return {"is_phishing_risk": is_risk, "reasons": reasons if is_risk else []}
