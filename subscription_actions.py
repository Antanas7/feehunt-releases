import webbrowser
from gmail_actions import get_unsubscribe_link
from translations import t

SERVICE_CANCEL_URLS = {
    "use ai": "https://use.ai/help/articles/subscription-cancellation",
    "use.ai": "https://use.ai/help/articles/subscription-cancellation",
    "chatgpt": "https://chatgpt.com/settings/subscription",
    "netflix": "https://www.netflix.com/CancelPlan",
    "spotify": "https://www.spotify.com/account/subscription/",
    "canva": "https://www.canva.com/settings/billing-and-plans",
}

def cancel_subscription(service_name, email_id):
    # 1. Try List-Unsubscribe header
    unsubscribe_url = get_unsubscribe_link(email_id)

    if unsubscribe_url:
        webbrowser.open(unsubscribe_url)
        return t("subscription.opened_unsubscribe").format(service_name=service_name)

    # 2. Known service mapping
    service_key = service_name.lower().strip()

    if service_key in SERVICE_CANCEL_URLS:
        webbrowser.open(SERVICE_CANCEL_URLS[service_key])
        return t("subscription.opened_billing").format(service_name=service_name)

    # 3. Fallback to Google search
    search_url = (
        f"https://www.google.com/search?q={service_name}+cancel+subscription"
    )
    webbrowser.open(search_url)

    return t("subscription.opened_search").format(service_name=service_name)
