import streamlit as st
from gmail_actions import delete_email


def _extract_message_id(item):
    """
    Bando ištraukti Gmail message ID iš įvairių galimų struktūrų.
    """
    if isinstance(item, str):
        return item

    if isinstance(item, dict):
        for key in ("message_id", "id", "gmail_id"):
            value = item.get(key)
            if value:
                return value

    return None


def render_smart_action_center(results: dict):
    if not results:
        return

    st.markdown("---")
    st.header("⚡ Smart Action Center")
    st.caption(
        "Peržiūrėkite rekomenduojamus veiksmus ir pasirinkite, ką FeeHunt gali atlikti už jus."
    )

    financial_risks = results.get("financial_risks", []) or []
    promotional_emails = results.get("promotional_emails", []) or []
    estimated_savings = results.get("estimated_savings", "$0/month")

    st.subheader("✅ Rekomenduojami veiksmai")

    delete_promos = st.checkbox(
        f"Ištrinti reklaminius laiškus ({len(promotional_emails)})",
        value=False,
        key="sac_delete_promos",
    )

    archive_promos = st.checkbox(
        f"Archyvuoti reklaminius laiškus ({len(promotional_emails)})",
        value=False,
        key="sac_archive_promos",
    )

    mark_spam = st.checkbox(
        f"Pažymėti reklaminius laiškus kaip spam ({len(promotional_emails)})",
        value=False,
        key="sac_mark_spam",
    )

    review_risks = st.checkbox(
        f"Peržiūrėti finansines rizikas ({len(financial_risks)})",
        value=True,
        key="sac_review_risks",
    )

    unsubscribe = st.checkbox(
        "Bandykite atsisakyti reklaminių naujienlaiškių",
        value=False,
        key="sac_unsubscribe",
    )

    st.subheader("📊 Galima nauda")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Reklaminiai laiškai", len(promotional_emails))

    with col2:
        st.metric("Finansinės rizikos", len(financial_risks))

    with col3:
        st.metric("Galimas sutaupymas", estimated_savings)

    selected_actions = {
        "delete_promos": delete_promos,
        "archive_promos": archive_promos,
        "mark_spam": mark_spam,
        "review_risks": review_risks,
        "unsubscribe": unsubscribe,
    }

    selected_count = sum(1 for value in selected_actions.values() if value)

    if selected_count == 0:
        st.info("Pasirinkite bent vieną veiksmą.")
        return

    with st.expander("👀 Preview Actions", expanded=False):
        if delete_promos:
            st.write(f"🗑️ Bus ištrinta reklaminių laiškų: {len(promotional_emails)}")
        if archive_promos:
            st.write("📦 Archive funkciją prijungsime kitame etape.")
        if mark_spam:
            st.write("🚫 Mark as Spam funkciją prijungsime kitame etape.")
        if review_risks:
            st.write(f"⚠️ Bus parodytos finansinės rizikos: {len(financial_risks)}")
        if unsubscribe:
            st.write("📭 Unsubscribe funkciją prijungsime kitame etape.")

    st.warning(
        "Saugumo režimas: laiškai perkeliami į Gmail šiukšliadėžę ir gali būti atkurti per 30 dienų."
    )

    if st.button("⚡ Fix Everything", type="primary"):
        if delete_promos and promotional_emails:
            st.info("🗑️ Perkeliami reklaminiai laiškai į Gmail šiukšliadėžę...")

            success_count = 0
            failed_count = 0
            failed_items = []

            for item in promotional_emails:
                message_id = _extract_message_id(item)

                if not message_id:
                    failed_count += 1
                    failed_items.append("Nerastas message_id")
                    continue

                try:
                    delete_email(message_id)
                    success_count += 1
                except Exception as e:
                    failed_count += 1
                    failed_items.append(str(e))

            if success_count > 0:
                st.success(
                    f"✅ Sėkmingai perkelta į Gmail šiukšliadėžę: {success_count} laiškų."
                )

            if failed_count > 0:
                st.warning(f"⚠️ Nepavyko apdoroti laiškų: {failed_count}")

                with st.expander("Rodyti klaidas"):
                    for error in failed_items:
                        st.write(f"- {error}")

        else:
            st.info("Nepasirinktas nė vienas vykdomas veiksmas.")

        if archive_promos:
            st.info("📦 Archive funkciją prijungsime kitame etape.")

        if mark_spam:
            st.info("🚫 Mark as Spam funkciją prijungsime kitame etape.")

        if unsubscribe:
            st.info("📭 Unsubscribe funkciją prijungsime kitame etape.")

