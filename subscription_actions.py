import webbrowser
from urllib.parse import quote_plus

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
