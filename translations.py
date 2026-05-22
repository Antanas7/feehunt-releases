TRANSLATIONS = {
    "en": {
        "dashboard.title": "💸 Dashboard",
        "dashboard.subtitle": "See what FeeHunt found and choose what to do next.",
        "dashboard.plan_info": (
            "FeeHunt scans one Gmail account at a time and keeps your results on this computer. "
            "Use it to spot subscriptions, payment issues, and promotional noise."
        ),
        "dashboard.auto_cleanup_on": "⚡ **Cleanup preview is on.** FeeHunt will prepare a plan after each scan; you confirm before Gmail changes.",
        "dashboard.scan_button": "🔍 Scan Gmail",
        "dashboard.scan_success": "✅ Gmail scan complete.",
        "dashboard.apply_rules_spinner": "Applying rules...",
        "dashboard.auto_deleted": "🤖 Cleanup complete: **{deleted}** deleted, **{archived}** archived.",
        "dashboard.needs_review": "❓ **{review}** emails need your decision. Open **Cleanup Rules** to review them.",
        "dashboard.scan_error": "❌ The scan could not finish.",
        "dashboard.no_error_text": "No additional error details were returned.",
        "dashboard.results_heading": "📊 Scan Results",
        "dashboard.metric_subscriptions": "Subscriptions and risks",
        "dashboard.metric_promotions": "Promotional emails",
        "dashboard.metric_savings": "Estimated monthly savings",
        "dashboard.last_scan": "Last scan: {last_scan_at}",
        "dashboard.get_started": "### 👋 Start here",
        "dashboard.no_scan": "Run your first Gmail scan to find subscriptions, payment alerts, and promotional emails.",
        "dashboard.privacy": "🔒 **Private by design** - results stay on your computer.",
        "dashboard.fast": "⚡ **Quick scan** - review recent emails in moments.",
        "dashboard.footer": "Privacy-first • Data stays on your computer",
        "onboarding.title": "💸 Welcome to FeeHunt!",
        "onboarding.subtitle": "Before starting, one setup step is required",
        "onboarding.credentials_missing": (
            "FeeHunt needs its Gmail sign-in file before it can connect. "
            "Download FeeHunt again, extract the full ZIP, and open FeeHunt from that folder."
        ),
        "onboarding.how_to": "### 📋 How to get credentials.json?",
        "onboarding.open_console": "🔗 Open Google Cloud Console",
        "onboarding.steps": (
            "**1.** Create a new project → name it `FeeHunt`\n\n"
            "**2.** Enable Gmail API: **APIs & Services → Library → Gmail API → Enable**\n\n"
            "**3.** Create credentials: **Credentials → + Create Credentials → OAuth client ID → Desktop app**\n\n"
            "**4.** Download the JSON file, rename it to `credentials.json`, and place it in:"
        ),
        "onboarding.reload": "**5.** Reload this page",
        "onboarding.check_credentials": "🔄 Check if credentials.json has been added",
        "onboarding.credentials_found": "✅ credentials.json found! Reloading...",
        "onboarding.file_not_found": "FeeHunt cannot see the Gmail sign-in file yet.",
        "onboarding.footer": "Privacy-first • FeeHunt never stores your data in the cloud",
        "scan.progress_preparing": "Preparing to scan...",
        "scan.main_missing": "FeeHunt could not find the scan tool. Please reopen FeeHunt from the extracted app folder.",
        "app.brand_title": "💸 FeeHunt",
        "sidebar.caption": "1 plan = 1 email account",
        "sidebar.navigation": "Navigation",
        "sidebar.footer": "Privacy-first • Local data",
        "sidebar.license": "License",
        "sidebar.refresh_license": "Refresh license",
        "sidebar.deactivate_license": "Deactivate license",
        "page.dashboard": "Dashboard",
        "page.subscriptions": "Subscriptions",
        "page.cleanup_rules": "Cleanup Rules",
        "page.settings": "Settings",
        "page.how_to_use": "How to Use",
        "how_to.title": "📘 How to Use FeeHunt",
        "how_to.intro_heading": "What FeeHunt Does",
        "how_to.intro": (
            "FeeHunt helps you review Gmail for subscriptions, payment alerts, and promotional emails. "
            "You stay in control: FeeHunt shows what it found, and you decide what to archive, delete, cancel, or keep."
        ),
        "how_to.scan_heading": "1. Scan Gmail",
        "how_to.scan_steps": (
            "1. Open **Dashboard**.\n"
            "2. Click **🔍 Scan Gmail**.\n"
            "3. Wait for the scan to finish.\n"
            "4. FeeHunt saves the latest scan results locally on your computer."
        ),
        "how_to.results_heading": "2. Understand Results",
        "how_to.results_bullets": (
            "- **Subscriptions and risks** show recurring plans, invoices, failed payments, and billing alerts.\n"
            "- **Payment reminders** are emails that may be worth reviewing first, such as declined cards or suspended accounts.\n"
            "- **Promotional emails** include marketing, shop, and newsletter emails you may want to clean up.\n"
            "- **Estimated savings** is a simple estimate based on detected subscription-related emails."
        ),
        "how_to.cancel_heading": "3. Cancel Subscriptions",
        "how_to.cancel_steps": (
            "1. Open **Subscriptions**.\n"
            "2. Expand a subscription or financial risk email.\n"
            "3. Click **❌ Cancel Subscription**.\n"
            "4. FeeHunt opens the best available unsubscribe, billing, help, or search page in your browser.\n"
            "5. Finish the cancellation on the service provider's website."
        ),
        "how_to.delete_heading": "4. Delete Old Alerts After Cancelling",
        "how_to.delete_bullets": (
            "- FeeHunt detects subscriptions from emails that are still in Gmail.\n"
            "- After you cancel, an old email can still appear as a past subscription alert.\n"
            "- Delete that old email to remove the past alert from future FeeHunt scans.\n"
            "- New payment or subscription emails from the same service will still be detected."
        ),
        "how_to.privacy_heading": "5. Privacy and Local Processing",
        "how_to.privacy_bullets": (
            "- FeeHunt runs locally on your Windows computer.\n"
            "- Scan results and settings are saved locally.\n"
            "- FeeHunt does not store your Gmail data in the cloud.\n"
            "- Gmail actions only run when you click an action button."
        ),
        "how_to.tips_heading": "Useful Tips",
        "how_to.tips_bullets": (
            "- Use **Cleanup Rules** to decide how FeeHunt handles senders and categories.\n"
            "- Add trusted senders to the whitelist.\n"
            "- Add unwanted senders to the blacklist.\n"
            "- Scan again after changing rules or deleting old alerts."
        ),
        "feedback.message": "Did FeeHunt help you save money? We'd love your feedback.",
        "feedback.button": "💬 Send Feedback",
        "subscriptions.page_title": "📄 Subscriptions and Payment Reminders",
        "subscriptions.no_scan": "📭 No scan has been run yet.",
        "subscriptions.no_scan_instruction": "Go to **Dashboard** and click **🔍 Scan Gmail**.",
        "subscriptions.heading": "🔄 Subscriptions",
        "subscriptions.found": "Found **{count}** subscription-related emails.",
        "subscriptions.none": "✅ No subscription alerts found.",
        "financial_risks.heading": "💳 Payment Reminders",
        "financial_risks.warning": (
            "Found **{count}** emails worth reviewing first. "
            "Nothing changes without your approval."
        ),
        "financial_risks.none": "✅ No payment reminders need attention.",
        "promotions.heading": "📢 Promotional Emails",
        "actions.open_gmail": "📬 Open Gmail",
        "actions.archive": "📥 Archive",
        "actions.delete": "🗑 Delete",
        "actions.spam": "🚫 Spam",
        "actions.important": "⭐ Important",
        "actions.unsubscribe": "🚪 Unsubscribe",
        "actions.cancel_subscription": "❌ Cancel Subscription",
        "actions.whitelist": "✅ Add to whitelist",
        "actions.blacklist": "🚫 Add to blacklist",
        "actions.archived": "Archived.",
        "actions.deleted": "Moved to trash.",
        "actions.spam_marked": "Marked as spam.",
        "actions.important_marked": "Marked as important.",
        "actions.no_unsubscribe": "💡 No unsubscribe link was found in this email. You can still check the sender's website.",
        "actions.cancel_aftercare": (
            "After cancelling, delete this old email if you want to remove this past alert from future scans. "
            "FeeHunt will still detect new payment or subscription emails from this service."
        ),
        "actions.added_whitelist": "'{sender}' added to whitelist.",
        "actions.added_blacklist": "'{sender}' added to blacklist.",
        "email.unknown_sender": "Unknown sender",
        "email.sender_label": "Sender",
        "email.date_label": "Date",
        "email.detected_keywords": "Detected keywords",
        "email.missing_message_id": "FeeHunt cannot open actions for this email yet. Please open it in Gmail instead.",
        "email.actions_label": "**Actions:**",
        "email.no_subject": "(no subject)",
        "actions.whitelist_help": "FeeHunt will never touch emails from this sender",
        "actions.blacklist_help": "FeeHunt will automatically delete emails from this sender",
        "bulk.caption": "Bulk actions:",
        "bulk.result": "{label}: {count} emails.",
        "bulk.errors": "FeeHunt could not change {count} email(s).",
        "bulk.archived": "Archived",
        "bulk.deleted": "Deleted",
        "bulk.spam": "Marked as spam",
        "status.main_found": "main.py found",
        "status.main_missing": "Scan tool is missing",
        "status.results_found": "last_scan_results.json found",
        "status.not_created": "Not created yet",
        "status.credentials_found": "credentials.json found",
        "status.credentials_missing": "Gmail sign-in file is missing",
        "status.app_folder": "App folder: {path}",
        "rules.reason_whitelist": "Whitelist",
        "rules.reason_blacklist": "Blacklist",
        "rules.error": "FeeHunt needs your review before changing this email.",
        "rules.delete_error": "FeeHunt could not move this email to trash.",
        "rules.archive_error": "FeeHunt could not archive this email.",
        "cleanup.title": "🧹 Cleanup Rules",
        "cleanup.tab_unwanted": "🚫 My unwanted senders",
        "cleanup.tab_category_rules": "📋 Category rules",
        "cleanup.tab_whitelist": "✅ Whitelist",
        "cleanup.tab_blacklist": "🚫 Blacklist",
        "cleanup.tab_custom": "➕ My categories",
        "cleanup.tab_results": "📊 Cleanup results",
        "cleanup.unwanted_title": "🚫 My unwanted senders",
        "cleanup.unwanted_caption": "Choose senders you consider promotional or unwanted. FeeHunt will help you review them safely.",
        "cleanup.control_info": (
            "✅ You control the rules. Checked senders are treated as unwanted. "
            "Uncheck a sender and save to stop using this rule."
        ),
        "cleanup.mark_unwanted": "### Mark unwanted senders",
        "cleanup.no_detected_senders": "No senders found yet. Run a Gmail scan from the Dashboard first.",
        "cleanup.save_unwanted": "💾 Save unwanted senders",
        "cleanup.unwanted_saved": "✅ Unwanted sender list saved.",
        "cleanup.rescan_caption": "Run a new Gmail scan so FeeHunt can apply these rules.",
        "cleanup.add_sender_heading": "### Add sender manually",
        "cleanup.sender_input": "Sender, domain, or keyword in sender address",
        "cleanup.sender_placeholder": "e.g. etoro, pinterest, producthunt.com, recommendations@discover.pinterest.com",
        "cleanup.add_sender": "➕ Add sender",
        "cleanup.enter_sender": "Enter a sender or domain.",
        "cleanup.sender_added": "✅ '{sender}' added as an unwanted sender.",
        "cleanup.keywords_heading": "### Additional promotional keywords",
        "cleanup.keywords_caption": "Use keywords carefully. Sender rules are safer and more precise.",
        "cleanup.keyword_input": "Add promotional keyword",
        "cleanup.keyword_placeholder": "e.g. newsletter",
        "cleanup.add_keyword": "➕ Add keyword",
        "cleanup.enter_keyword": "Enter a keyword.",
        "cleanup.keyword_added": "✅ Keyword '{keyword}' added.",
        "cleanup.current_keywords": "**Current promotional keywords:**",
        "cleanup.save_keywords": "💾 Save keywords",
        "cleanup.keywords_saved": "✅ Keywords saved.",
        "cleanup.no_keywords": "No additional promotional keywords yet.",
        "cleanup.how_heading": "### How it works",
        "cleanup.how_text": (
            "1. Mark or enter an unwanted sender.\n"
            "2. FeeHunt saves it to feehunt_settings.json.\n"
            "3. During the next scan, emails from this sender will be treated as promotional.\n"
            "4. If you change your mind, uncheck it and save."
        ),
        "cleanup.category_title": "Choose actions by category",
        "cleanup.category_caption": "If automatic cleanup is enabled, FeeHunt applies these rules after each scan.",
        "cleanup.protected": "🔒 Protected category - always notify only",
        "cleanup.action_label": "Action",
        "cleanup.save_rules": "💾 Save rules",
        "cleanup.rules_saved": "✅ Rules saved!",
        "cleanup.apply_now": "⚡ Apply rules now",
        "cleanup.preview_now": "Preview cleanup",
        "cleanup.preview_ready": "Cleanup preview is ready. Review it before anything changes in Gmail.",
        "cleanup.preview_title": "Cleanup preview",
        "cleanup.preview_caption": "FeeHunt has not changed Gmail yet. Review what would happen, then confirm if it looks right.",
        "cleanup.preview_more": "+ {count} more email(s)",
        "cleanup.preview_no_changes": "No automatic Gmail changes are planned. Protected or notify-only emails stay for review.",
        "cleanup.confirm_apply": "Apply these changes",
        "cleanup.metric_protected": "Protected",
        "cleanup.done": "✅ Done! Deleted: **{deleted}**, archived: **{archived}**.",
        "cleanup.review_waiting": "❓ Waiting for your decision: **{review}** emails (see **Cleanup results**).",
        "cleanup.scan_first": "Run a Gmail scan from the Dashboard first.",
        "cleanup.save_error": "FeeHunt could not save this yet. Please try again.",
        "cleanup.whitelist_title": "✅ Whitelist",
        "cleanup.whitelist_caption": "FeeHunt will never touch emails from these senders, even if a rule says otherwise.",
        "cleanup.whitelist_input": "Add sender (email address or domain)",
        "cleanup.whitelist_placeholder": "e.g. bank@example.com or example.com",
        "cleanup.whitelist_add": "➕ Add to whitelist",
        "cleanup.whitelist_added": "✅ '{sender}' added.",
        "cleanup.whitelist_current": "**Currently in whitelist:**",
        "cleanup.whitelist_empty": "Whitelist is empty.",
        "cleanup.blacklist_title": "🚫 Blacklist",
        "cleanup.blacklist_caption": "Emails from these senders are proposed for cleanup first. Protected payment, receipt, invoice, and security emails are never auto-deleted.",
        "cleanup.blacklist_input": "Add sender",
        "cleanup.blacklist_placeholder": "e.g. spam@newsletter.com",
        "cleanup.blacklist_add": "➕ Add to blacklist",
        "cleanup.blacklist_added": "🚫 '{sender}' added.",
        "cleanup.blacklist_current": "**Currently in blacklist:**",
        "cleanup.blacklist_empty": "Blacklist is empty.",
        "cleanup.custom_title": "➕ My categories",
        "cleanup.custom_caption": "Create simple custom categories using keywords you choose.",
        "cleanup.custom_name": "Category name",
        "cleanup.custom_keywords": "Keywords (comma-separated)",
        "cleanup.custom_name_placeholder": "e.g. LinkedIn",
        "cleanup.custom_keywords_placeholder": "e.g. linkedin, jobs, hiring",
        "cleanup.custom_create": "➕ Create category",
        "cleanup.custom_created": "✅ Category '{name}' created!",
        "cleanup.custom_current": "**Your categories:**",
        "cleanup.custom_keyword_label": "Keywords: {keywords}",
        "cleanup.custom_empty": "You do not have any categories yet.",
        "cleanup.results_title": "📊 Latest cleanup results",
        "cleanup.no_results": "No cleanup has run yet. Click **⚡ Apply rules now** or enable automatic cleanup in Settings.",
        "cleanup.metric_deleted": "🗑 Deleted",
        "cleanup.metric_archived": "📥 Archived",
        "cleanup.metric_review": "❓ Waiting for decision",
        "cleanup.metric_notified": "🔔 Notified",
        "cleanup.waiting_title": "❓ Waiting for your decision",
        "cleanup.waiting_caption": "These emails are in the **'Ask me'** category - you decide.",
        "cleanup.deleted_expander": "🗑 Deleted ({count})",
        "cleanup.archived_expander": "📥 Archived ({count})",
        "actions.remove": "❌",
        "category.promotions.label": "Promotional emails",
        "category.promotions.description": "Promotions, discounts, special offers",
        "category.shops.label": "Online shop offers",
        "category.shops.description": "Amazon, eBay, AliExpress, and other shops",
        "category.newsletters.label": "Newsletters",
        "category.newsletters.description": "Regular informational emails and blogs",
        "category.subscriptions.label": "Subscriptions",
        "category.subscriptions.description": "Recurring payments and service subscriptions",
        "category.financial_risks.label": "Payment reminders",
        "category.financial_risks.description": "Failed payments, card problems, and account notes",
        "category_action.delete": "🗑 Automatically delete",
        "category_action.archive": "📥 Automatically archive",
        "category_action.ask": "❓ Ask me",
        "category_action.notify": "🔔 Notify only",
        "category_action.ignore": "👁 Ignore",
        "settings.title": "⚙️ Settings",
        "language.english": "English",
        "language.lithuanian": "Lithuanian",
        "settings.language": "Language",
        "settings.currency": "Currency",
        "settings.auto_scan": "Automatic scan",
        "settings.auto_scan_off": "Off",
        "settings.auto_scan_hourly": "Hourly",
        "settings.auto_scan_daily": "Daily",
        "settings.apply_rules": "⚡ Prepare Cleanup Rules preview after each scan",
        "settings.apply_rules_help": "When enabled, FeeHunt prepares a cleanup preview after each scan. Gmail changes still need your confirmation.",
        "settings.safe_mode": "🔒 Safe mode",
        "settings.safe_mode_help": "Recommended while FeeHunt is in beta.",
        "settings.max_dashboard": "How many emails to show on the Dashboard page",
        "settings.save": "💾 Save settings",
        "settings.saved": "✅ Settings saved.",
        "settings.save_error": "FeeHunt could not save this yet. Please try again.",
        "settings.technical_info": "🔧 Technical information",
        "gmail.credentials_missing": "FeeHunt could not find the Gmail sign-in file.",
        "subscription.opened_unsubscribe": "Opened unsubscribe page for {service_name}.",
        "subscription.opened_billing": "Opened billing page for {service_name}.",
        "subscription.opened_search": "Opened search results for {service_name}. Look for Billing or Subscription settings.",
        "runner.app_missing": "FeeHunt could not find one of its app files.",
        "runner.check_internal": "Please reinstall FeeHunt from a fresh download.",
        "runner.press_enter": "Press Enter to close...",
    },
    "lt": {
        "dashboard.title": "💸 Dashboard",
        "dashboard.subtitle": "Peržiūrėkite, ką FeeHunt rado, ir pasirinkite kitą veiksmą.",
        "dashboard.plan_info": (
            "FeeHunt skenuoja vieną Gmail paskyrą vienu metu ir saugo rezultatus šiame kompiuteryje. "
            "Naudokite jį prenumeratoms, mokėjimų įspėjimams ir reklaminiam triukšmui rasti."
        ),
        "dashboard.auto_cleanup_on": "⚡ **Valymo peržiūra įjungta.** FeeHunt paruoš planą po skenavimo; Gmail keitimai vyks tik po patvirtinimo.",
        "dashboard.scan_button": "🔍 Skenuoti Gmail",
        "dashboard.scan_success": "✅ Gmail skenavimas baigtas.",
        "dashboard.apply_rules_spinner": "Pritaikomos taisyklės...",
        "dashboard.auto_deleted": "🤖 Valymas baigtas: ištrinta **{deleted}**, archyvuota **{archived}**.",
        "dashboard.needs_review": "❓ **{review}** laiškų laukia jūsų sprendimo. Atidarykite **Cleanup Rules**.",
        "dashboard.scan_error": "❌ Skenavimo nepavyko užbaigti.",
        "dashboard.no_error_text": "Papildomos klaidos informacijos negauta.",
        "dashboard.results_heading": "📊 Skenavimo rezultatai",
        "dashboard.metric_subscriptions": "Prenumeratos ir rizikos",
        "dashboard.metric_promotions": "Reklaminiai laiškai",
        "dashboard.metric_savings": "Numatomas sutaupymas per mėn.",
        "dashboard.last_scan": "Paskutinis skenavimas: {last_scan_at}",
        "dashboard.get_started": "### 👋 Pradėkite čia",
        "dashboard.no_scan": "Atlikite pirmą Gmail skenavimą, kad rastumėte prenumeratas, mokėjimų įspėjimus ir reklaminius laiškus.",
        "dashboard.privacy": "🔒 **Privatu pagal dizainą** – rezultatai lieka jūsų kompiuteryje.",
        "dashboard.fast": "⚡ **Greitas skenavimas** – naujausius laiškus peržiūrėsite per kelias akimirkas.",
        "dashboard.footer": "Privacy-first • Duomenys lieka jūsų kompiuteryje",
        "onboarding.title": "💸 Sveiki atvykę į FeeHunt!",
        "onboarding.subtitle": "Prieš pradedant – reikalingas vienas nustatymo žingsnis",
        "onboarding.credentials_missing": (
            "⚠️ **credentials.json failas nerastas.** "
            "Šis failas reikalingas, kad FeeHunt galėtų prisijungti prie jūsų Gmail paskyros."
        ),
        "onboarding.how_to": "### 📋 Kaip gauti credentials.json?",
        "onboarding.open_console": "🔗 Atidaryti Google Cloud Console",
        "onboarding.steps": (
            "**1.** Sukurkite naują projektą → pavadinkite `FeeHunt`\n\n"
            "**2.** Įjunkite Gmail API: **APIs & Services → Library → Gmail API → Enable**\n\n"
            "**3.** Sukurkite kredencialus: **Credentials → + Create Credentials → OAuth client ID → Desktop app**\n\n"
            "**4.** Atsisiųskite JSON failą, pervadinkite į `credentials.json` ir įkelkite į:"
        ),
        "onboarding.reload": "**5.** Perkraukite šį puslapį",
        "onboarding.check_credentials": "🔄 Patikrinti – ar credentials.json jau įkeltas?",
        "onboarding.credentials_found": "✅ credentials.json rastas! Perkraunama...",
        "onboarding.file_not_found": "❌ Failas dar nerastas: {path}",
        "onboarding.footer": "Privacy-first • FeeHunt niekada nesaugo jūsų duomenų debesyje",
        "scan.progress_preparing": "Ruošiamasi skenuoti...",
        "scan.main_missing": "Nerastas failas: {path}",
        "app.brand_title": "💸 FeeHunt",
        "sidebar.caption": "1 planas = 1 el. pašto paskyra",
        "sidebar.navigation": "Navigacija",
        "sidebar.footer": "Privacy-first • Local data",
        "sidebar.license": "Licencija",
        "sidebar.refresh_license": "Atnaujinti licenciją",
        "sidebar.deactivate_license": "Išjungti licenciją",
        "page.dashboard": "Dashboard",
        "page.subscriptions": "Prenumeratos",
        "page.cleanup_rules": "Cleanup Rules",
        "page.settings": "Nustatymai",
        "page.how_to_use": "Kaip naudotis",
        "how_to.title": "📘 Kaip naudotis FeeHunt",
        "how_to.intro_heading": "Ką daro FeeHunt",
        "how_to.intro": (
            "FeeHunt padeda peržiūrėti Gmail laiškus ir rasti prenumeratas, mokėjimų įspėjimus bei reklaminius laiškus. "
            "Jūs valdote sprendimus: FeeHunt parodo radinius, o jūs pasirenkate, ką archyvuoti, ištrinti, atšaukti ar palikti."
        ),
        "how_to.scan_heading": "1. Nuskenuokite Gmail",
        "how_to.scan_steps": (
            "1. Atidarykite **Dashboard**.\n"
            "2. Paspauskite **🔍 Skenuoti Gmail**.\n"
            "3. Palaukite, kol skenavimas baigsis.\n"
            "4. FeeHunt išsaugos naujausius rezultatus šiame kompiuteryje."
        ),
        "how_to.results_heading": "2. Supraskite rezultatus",
        "how_to.results_bullets": (
            "- **Prenumeratos ir rizikos** rodo pasikartojančius planus, sąskaitas, nepavykusius mokėjimus ir apmokėjimo laiškus.\n"
            "- **Mokėjimų priminimai** yra laiškai, kuriuos verta peržiūrėti pirmiausia, pvz. atmestos kortelės ar sustabdytos paskyros.\n"
            "- **Reklaminiai laiškai** apima marketingo, parduotuvių ir naujienlaiškių laiškus.\n"
            "- **Numatomas sutaupymas** yra paprastas įvertinimas pagal rastus prenumeratų laiškus."
        ),
        "how_to.cancel_heading": "3. Atšaukite prenumeratas",
        "how_to.cancel_steps": (
            "1. Atidarykite **Prenumeratos**.\n"
            "2. Išskleiskite prenumeratos arba finansinės rizikos laišką.\n"
            "3. Paspauskite **❌ Cancel Subscription**.\n"
            "4. FeeHunt naršyklėje atidarys tinkamiausią atsisakymo, apmokėjimo, pagalbos arba paieškos puslapį.\n"
            "5. Užbaikite atšaukimą paslaugos teikėjo svetainėje."
        ),
        "how_to.delete_heading": "4. Ištrinkite senus įspėjimus po atšaukimo",
        "how_to.delete_bullets": (
            "- FeeHunt aptinka prenumeratas pagal laiškus, kurie vis dar yra Gmail.\n"
            "- Po atšaukimo senas laiškas gali vis dar atrodyti kaip praeities prenumeratos įspėjimas.\n"
            "- Ištrinkite seną laišką, jei norite pašalinti šį įspėjimą iš būsimų skenavimų.\n"
            "- Nauji tos pačios paslaugos mokėjimų ar prenumeratų laiškai vis tiek bus aptikti."
        ),
        "how_to.privacy_heading": "5. Privatumas ir lokalus apdorojimas",
        "how_to.privacy_bullets": (
            "- FeeHunt veikia lokaliai jūsų Windows kompiuteryje.\n"
            "- Skenavimo rezultatai ir nustatymai saugomi lokaliai.\n"
            "- FeeHunt nesaugo jūsų Gmail duomenų debesyje.\n"
            "- Gmail veiksmai atliekami tik tada, kai paspaudžiate atitinkamą mygtuką."
        ),
        "how_to.tips_heading": "Naudingi patarimai",
        "how_to.tips_bullets": (
            "- Naudokite **Cleanup Rules**, kad valdytumėte siuntėjus ir kategorijas.\n"
            "- Patikimus siuntėjus pridėkite į baltąjį sąrašą.\n"
            "- Nepageidaujamus siuntėjus pridėkite į juodąjį sąrašą.\n"
            "- Po taisyklių keitimo ar senų įspėjimų ištrynimo nuskenuokite Gmail dar kartą."
        ),
        "feedback.message": "Ar FeeHunt padėjo sutaupyti? Labai laukiame jūsų atsiliepimo.",
        "feedback.button": "💬 Siųsti atsiliepimą",
        "subscriptions.page_title": "📄 Prenumeratos ir finansinės rizikos",
        "subscriptions.no_scan": "📭 Dar neatliktas skenavimas.",
        "subscriptions.no_scan_instruction": "Eikite į **Dashboard** ir paspauskite **🔍 Skenuoti Gmail**.",
        "subscriptions.heading": "🔄 Prenumeratos",
        "subscriptions.found": "Rasta **{count}** prenumeratų susijusių laiškų.",
        "subscriptions.none": "✅ Prenumeratų įspėjimų nerasta.",
        "financial_risks.heading": "💳 Mokėjimų priminimai",
        "financial_risks.warning": (
            "Rasta **{count}** laiškų, kuriuos verta peržiūrėti pirmiausia. "
            "Nieko nekeičiama be jūsų patvirtinimo."
        ),
        "financial_risks.none": "✅ Mokėjimų priminimų, kuriems reikia dėmesio, nerasta.",
        "promotions.heading": "📢 Reklaminiai laiškai",
        "actions.open_gmail": "📬 Atidaryti Gmail",
        "actions.archive": "📥 Archyvuoti",
        "actions.delete": "🗑 Ištrinti",
        "actions.spam": "🚫 Šlamštas",
        "actions.important": "⭐ Svarbus",
        "actions.unsubscribe": "🚪 Atsisakyti prenumeratos",
        "actions.cancel_subscription": "❌ Cancel Subscription",
        "actions.whitelist": "✅ Į baltąjį sąrašą",
        "actions.blacklist": "🚫 Į juodąjį sąrašą",
        "actions.archived": "Archyvuota.",
        "actions.deleted": "Perkelta į šiukšlinę.",
        "actions.spam_marked": "Pažymėta kaip šlamštas.",
        "actions.important_marked": "Pažymėta kaip svarbus.",
        "actions.no_unsubscribe": "💡 Šiame laiške atsisakymo nuorodos nerasta. Vis dar galite patikrinti siuntėjo svetainę.",
        "actions.cancel_aftercare": (
            "Po atšaukimo ištrinkite šį seną laišką, jei norite pašalinti praeities įspėjimą iš būsimų skenavimų. "
            "Nauji šios paslaugos mokėjimų ar prenumeratų laiškai vis tiek bus aptikti."
        ),
        "actions.added_whitelist": "'{sender}' pridėtas į baltąjį sąrašą.",
        "actions.added_blacklist": "'{sender}' pridėtas į juodąjį sąrašą.",
        "email.unknown_sender": "Nežinomas siuntėjas",
        "email.sender_label": "Siuntėjas",
        "email.date_label": "Data",
        "email.detected_keywords": "Aptikti raktažodžiai",
        "email.missing_message_id": "FeeHunt kol kas negali atlikti veiksmų su šiuo laišku. Atidarykite jį Gmail.",
        "email.actions_label": "**Veiksmai:**",
        "email.no_subject": "(be temos)",
        "actions.whitelist_help": "FeeHunt niekada nelies šio siuntėjo laiškų",
        "actions.blacklist_help": "FeeHunt automatiškai trins šio siuntėjo laiškus",
        "bulk.caption": "Masiniai veiksmai:",
        "bulk.result": "{label}: {count} laiškų.",
        "bulk.errors": "Kelių laiškų nepavyko pakeisti: {count}",
        "bulk.archived": "Archyvuota",
        "bulk.deleted": "Ištrinta",
        "bulk.spam": "Pažymėta šlamštu",
        "status.main_found": "main.py rastas",
        "status.main_missing": "Skenavimo įrankis nerastas",
        "status.results_found": "last_scan_results.json rastas",
        "status.not_created": "Dar nesukurtas",
        "status.credentials_found": "credentials.json rastas",
        "status.credentials_missing": "Gmail prisijungimo failas nerastas",
        "status.app_folder": "App folder: {path}",
        "rules.reason_whitelist": "Baltasis sąrašas",
        "rules.reason_blacklist": "Juodasis sąrašas",
        "rules.error": "FeeHunt paliko šį laišką jūsų peržiūrai.",
        "rules.delete_error": "FeeHunt nepavyko perkelti šio laiško į šiukšlinę.",
        "rules.archive_error": "FeeHunt nepavyko archyvuoti šio laiško.",
        "cleanup.title": "🧹 Valymo taisyklės",
        "cleanup.tab_unwanted": "🚫 Mano nepageidaujami siuntėjai",
        "cleanup.tab_category_rules": "📋 Kategorijų taisyklės",
        "cleanup.tab_whitelist": "✅ Baltasis sąrašas",
        "cleanup.tab_blacklist": "🚫 Juodasis sąrašas",
        "cleanup.tab_custom": "➕ Mano kategorijos",
        "cleanup.tab_results": "📊 Valymo rezultatai",
        "cleanup.unwanted_title": "🚫 Mano nepageidaujami siuntėjai",
        "cleanup.unwanted_caption": "Pasirinkite siuntėjus, kuriuos laikote reklaminiais ar nepageidaujamais. FeeHunt padės juos saugiai peržiūrėti.",
        "cleanup.control_info": (
            "✅ Jūs valdote taisykles. Pažymėti siuntėjai laikomi nepageidaujamais. "
            "Nuimkite varnelę ir išsaugokite, kad taisyklė jiems nebebūtų taikoma."
        ),
        "cleanup.mark_unwanted": "### Pažymėkite nepageidaujamus siuntėjus",
        "cleanup.no_detected_senders": "Siuntėjų dar nerasta. Pirmiausia atlikite Gmail skenavimą Dashboard puslapyje.",
        "cleanup.save_unwanted": "💾 Išsaugoti nepageidaujamus siuntėjus",
        "cleanup.unwanted_saved": "✅ Nepageidaujamų siuntėjų sąrašas išsaugotas.",
        "cleanup.rescan_caption": "Paleiskite naują Gmail skenavimą, kad FeeHunt pritaikytų šias taisykles.",
        "cleanup.add_sender_heading": "### Pridėti siuntėją rankiniu būdu",
        "cleanup.sender_input": "Siuntėjas, domenas arba raktažodis siuntėjo adrese",
        "cleanup.sender_placeholder": "pvz. etoro, pinterest, producthunt.com, recommendations@discover.pinterest.com",
        "cleanup.add_sender": "➕ Pridėti siuntėją",
        "cleanup.enter_sender": "Įrašykite siuntėją arba domeną.",
        "cleanup.sender_added": "✅ '{sender}' pridėtas kaip nepageidaujamas siuntėjas.",
        "cleanup.keywords_heading": "### Papildomi reklaminiai raktažodžiai",
        "cleanup.keywords_caption": "Raktažodžius naudokite atsargiai. Siuntėjo taisyklės paprastai yra tikslesnės.",
        "cleanup.keyword_input": "Pridėti reklaminį raktažodį",
        "cleanup.keyword_placeholder": "pvz. newsletter",
        "cleanup.add_keyword": "➕ Pridėti raktažodį",
        "cleanup.enter_keyword": "Įrašykite raktažodį.",
        "cleanup.keyword_added": "✅ Raktažodis '{keyword}' pridėtas.",
        "cleanup.current_keywords": "**Dabartiniai reklaminiai raktažodžiai:**",
        "cleanup.save_keywords": "💾 Išsaugoti raktažodžius",
        "cleanup.keywords_saved": "✅ Raktažodžiai išsaugoti.",
        "cleanup.no_keywords": "Papildomų reklaminių raktažodžių dar nėra.",
        "cleanup.how_heading": "### Kaip tai veikia?",
        "cleanup.how_text": (
            "1. Pažymite arba įvedate nepageidaujamą siuntėją.\n"
            "2. FeeHunt išsaugo jį į feehunt_settings.json.\n"
            "3. Kito skenavimo metu šio siuntėjo laiškai bus laikomi reklaminiais.\n"
            "4. Jei persigalvosite – nuimkite varnelę ir išsaugokite."
        ),
        "cleanup.category_title": "Pasirinkite veiksmus pagal kategoriją",
        "cleanup.category_caption": "Jei automatinis valymas įjungtas, FeeHunt pritaikys šias taisykles po kiekvieno skenavimo.",
        "cleanup.protected": "🔒 Apsaugota kategorija – visada tik informuojama",
        "cleanup.action_label": "Veiksmas",
        "cleanup.save_rules": "💾 Išsaugoti taisykles",
        "cleanup.rules_saved": "✅ Taisyklės išsaugotos!",
        "cleanup.apply_now": "⚡ Pritaikyti taisykles dabar",
        "cleanup.preview_now": "Peržiūrėti valymo planą",
        "cleanup.preview_ready": "Valymo planas paruoštas. Peržiūrėkite jį prieš keičiant Gmail.",
        "cleanup.preview_title": "Valymo peržiūra",
        "cleanup.preview_caption": "FeeHunt dar nieko nepakeitė Gmail. Peržiūrėkite, kas įvyktų, ir patvirtinkite tik jei viskas aišku.",
        "cleanup.preview_more": "+ dar {count} laiškų",
        "cleanup.preview_no_changes": "Automatinių Gmail pakeitimų neplanuojama. Apsaugoti arba tik informavimo laiškai lieka peržiūrai.",
        "cleanup.confirm_apply": "Pritaikyti šiuos pakeitimus",
        "cleanup.metric_protected": "Apsaugota",
        "cleanup.done": "✅ Baigta! Ištrinta: **{deleted}**, archyvuota: **{archived}**.",
        "cleanup.review_waiting": "❓ Laukia jūsų sprendimo: **{review}** laiškų (žr. **Valymo rezultatai**).",
        "cleanup.scan_first": "Pirmiausia atlikite Gmail skenavimą Dashboard puslapyje.",
        "cleanup.save_error": "FeeHunt kol kas nepavyko išsaugoti. Pabandykite dar kartą.",
        "cleanup.whitelist_title": "✅ Baltasis sąrašas",
        "cleanup.whitelist_caption": "Šių siuntėjų laiškų FeeHunt niekada nelies – net jei taisyklė sako kitaip.",
        "cleanup.whitelist_input": "Pridėti siuntėją (el. pašto adresas arba domenas)",
        "cleanup.whitelist_placeholder": "pvz. bankas@seb.lt arba seb.lt",
        "cleanup.whitelist_add": "➕ Pridėti į baltąjį sąrašą",
        "cleanup.whitelist_added": "✅ '{sender}' pridėtas.",
        "cleanup.whitelist_current": "**Šiuo metu baltajame sąraše:**",
        "cleanup.whitelist_empty": "Baltasis sąrašas tuščias.",
        "cleanup.blacklist_title": "🚫 Juodasis sąrašas",
        "cleanup.blacklist_caption": "Šių siuntėjų laiškai pirmiausia patenka į valymo planą. Mokėjimų, kvitų, sąskaitų ir saugumo laiškai niekada netrinami automatiškai.",
        "cleanup.blacklist_input": "Pridėti siuntėją",
        "cleanup.blacklist_placeholder": "pvz. spam@newsletter.com",
        "cleanup.blacklist_add": "➕ Pridėti į juodąjį sąrašą",
        "cleanup.blacklist_added": "🚫 '{sender}' pridėtas.",
        "cleanup.blacklist_current": "**Šiuo metu juodajame sąraše:**",
        "cleanup.blacklist_empty": "Juodasis sąrašas tuščias.",
        "cleanup.custom_title": "➕ Mano kategorijos",
        "cleanup.custom_caption": "Sukurkite paprastas kategorijas pagal pasirinktus raktažodžius.",
        "cleanup.custom_name": "Kategorijos pavadinimas",
        "cleanup.custom_keywords": "Raktažodžiai (atskirti kableliu)",
        "cleanup.custom_name_placeholder": "pvz. LinkedIn",
        "cleanup.custom_keywords_placeholder": "pvz. linkedin, jobs, hiring",
        "cleanup.custom_create": "➕ Sukurti kategoriją",
        "cleanup.custom_created": "✅ Kategorija '{name}' sukurta!",
        "cleanup.custom_current": "**Jūsų kategorijos:**",
        "cleanup.custom_keyword_label": "Raktažodžiai: {keywords}",
        "cleanup.custom_empty": "Dar nėra jūsų kategorijų.",
        "cleanup.results_title": "📊 Paskutinio valymo rezultatai",
        "cleanup.no_results": "Valymas dar nebuvo atliktas. Paspauskite **⚡ Pritaikyti taisykles dabar** arba įjunkite automatinį valymą Nustatymuose.",
        "cleanup.metric_deleted": "🗑 Ištrinta",
        "cleanup.metric_archived": "📥 Archyvuota",
        "cleanup.metric_review": "❓ Laukia sprendimo",
        "cleanup.metric_notified": "🔔 Informuota",
        "cleanup.waiting_title": "❓ Laukia jūsų sprendimo",
        "cleanup.waiting_caption": "Šie laiškai patenka į **'Paklausti manęs'** kategoriją – jūs nusprendžiate.",
        "cleanup.deleted_expander": "🗑 Ištrinta ({count})",
        "cleanup.archived_expander": "📥 Archyvuota ({count})",
        "actions.remove": "❌",
        "category.promotions.label": "Reklaminiai laiškai",
        "category.promotions.description": "Akcijos, nuolaidos, specialūs pasiūlymai",
        "category.shops.label": "Internetinių parduotuvių pasiūlymai",
        "category.shops.description": "Amazon, eBay, AliExpress ir kitos parduotuvės",
        "category.newsletters.label": "Naujienlaiškiai",
        "category.newsletters.description": "Reguliarūs informaciniai laiškai, tinklaraščiai",
        "category.subscriptions.label": "Prenumeratos",
        "category.subscriptions.description": "Pasikartojantys mokėjimai, paslaugų prenumeratos",
        "category.financial_risks.label": "Mokėjimų priminimai",
        "category.financial_risks.description": "Nepavykę mokėjimai, kortelių problemos ir paskyrų pranešimai",
        "category_action.delete": "🗑 Automatiškai ištrinti",
        "category_action.archive": "📥 Automatiškai archyvuoti",
        "category_action.ask": "❓ Paklausti manęs",
        "category_action.notify": "🔔 Tik informuoti",
        "category_action.ignore": "👁 Ignoruoti",
        "settings.title": "⚙️ Nustatymai",
        "language.english": "Anglų",
        "language.lithuanian": "Lietuvių",
        "settings.language": "Kalba",
        "settings.currency": "Valiuta",
        "settings.auto_scan": "Automatinis skenavimas",
        "settings.auto_scan_off": "Išjungtas",
        "settings.auto_scan_hourly": "Kas valandą",
        "settings.auto_scan_daily": "Kartą per dieną",
        "settings.apply_rules": "⚡ Paruošti Cleanup Rules peržiūrą po kiekvieno skenavimo",
        "settings.apply_rules_help": "Įjungus, FeeHunt paruoš valymo planą po kiekvieno skenavimo. Gmail pakeitimams vis tiek reikės jūsų patvirtinimo.",
        "settings.safe_mode": "🔒 Saugus režimas",
        "settings.safe_mode_help": "Rekomenduojama palikti įjungtą, kol FeeHunt yra beta versijoje.",
        "settings.max_dashboard": "Kiek laiškų rodyti Dashboard puslapyje",
        "settings.save": "💾 Išsaugoti nustatymus",
        "settings.saved": "✅ Nustatymai išsaugoti.",
        "settings.save_error": "FeeHunt kol kas nepavyko išsaugoti. Pabandykite dar kartą.",
        "settings.technical_info": "🔧 Techninė informacija",
        "gmail.credentials_missing": "FeeHunt nerado Gmail prisijungimo failo.",
        "subscription.opened_unsubscribe": "Atidarytas {service_name} prenumeratos atsisakymo puslapis.",
        "subscription.opened_billing": "Atidarytas {service_name} mokėjimų puslapis.",
        "subscription.opened_search": "Atidaryti {service_name} paieškos rezultatai. Ieškokite Billing arba Subscription nustatymų.",
        "runner.app_missing": "FeeHunt nerado vieno iš programos failų.",
        "runner.check_internal": "Įdiekite FeeHunt iš naujai atsisiųsto failo.",
        "runner.press_enter": "Paspauskite Enter, kad uždarytumėte...",
    },
}


LICENSE_TRANSLATIONS = {
    "en": {
        "license.title": "License Activation",
        "license.beta_note": (
            "Licensing is being prepared for public launch. "
            "Beta functionality remains available without activation."
        ),
        "license.key_input": "License Key",
        "license.key_placeholder": "Enter your license key",
        "license.save_button": "Save License Key",
        "license.current_status": "Current License Status",
        "license.trial_status": "Trial Status",
        "license.status_missing": "No license key entered",
        "license.status_saved": "License key saved locally",
        "license.saved": "License key saved locally.",
        "license.save_error": "Enter a license key before saving.",
        "license.status.trial": "Status: trial",
        "license.status.active": "Status: active",
        "license.status.expired": "Status: expired",
        "license.status.invalid": "Status: invalid",
        "license.trial_status.trial": "Trial is active. Beta features remain available.",
        "license.trial_status.active": "License is active. Beta features remain available.",
        "license.trial_status.expired": "Trial has expired locally. Beta features remain available.",
        "license.trial_status.invalid": "No valid local license status yet. Beta features remain available.",
        "license.trial_status.unknown": "Trial status is not available yet.",
        "license.metric.status": "License Status",
        "license.metric.trial_days": "Trial Days Remaining",
        "license.metric.plan": "Plan Name",
        "license.metric.allowed_accounts": "Allowed Gmail Accounts",
        "license.metric.connected_accounts": "Connected Gmail Accounts",
        "license.status_value.trial": "Trial",
        "license.status_value.active": "Active",
        "license.status_value.expired": "Expired",
        "license.status_value.invalid": "Invalid",
        "license.plan.basic": "Basic Plan",
        "license.plan.personal": "Basic Plan",
        "license.plan.family": "Family Plan",
        "license.plan.pro": "Pro Plan",
        "license.connected_accounts_empty": "No Gmail accounts are connected to this license yet.",
        "license.connected_accounts_list": "Connected accounts: {accounts}",
        "license.plan_limit_exceeded": (
            "You have connected more Gmail accounts than your current plan allows. "
            "Please upgrade your plan before public launch enforcement is enabled."
        ),
        "license.plan_limit_ok": "Your current plan matches your connected Gmail account usage.",
        "license.upgrade_button": "Upgrade Plan (Coming Soon)",
        "license.upgrade_note": "Plan upgrades will be available at public launch. No payment is processed in this beta.",
        "license.message.trial": "Trial is active. {days} day(s) remaining. Beta features remain available.",
        "license.message.active": "{plan} is active. Beta features remain available.",
        "license.message.expired": "Your local trial has expired. You will be able to choose a plan before public launch. Beta features remain available.",
        "license.message.invalid": "No valid license is active locally. Beta features remain available.",
    },
    "lt": {
        "license.title": "Licencijos aktyvavimas",
        "license.beta_note": (
            "Licencijavimo sistema ruosiama viesam paleidimui. "
            "Beta funkcionalumas lieka pasiekiamas be aktyvavimo."
        ),
        "license.key_input": "Licencijos raktas",
        "license.key_placeholder": "Iveskite licencijos rakta",
        "license.save_button": "Issaugoti licencijos rakta",
        "license.current_status": "Dabartine licencijos busena",
        "license.trial_status": "Trial busena",
        "license.status_missing": "Licencijos raktas neivestas",
        "license.status_saved": "Licencijos raktas issaugotas lokaliai",
        "license.saved": "Licencijos raktas issaugotas lokaliai.",
        "license.save_error": "Pries issaugodami iveskite licencijos rakta.",
        "license.status.trial": "Busena: trial",
        "license.status.active": "Busena: active",
        "license.status.expired": "Busena: expired",
        "license.status.invalid": "Busena: invalid",
        "license.trial_status.trial": "Trial aktyvus. Beta funkcijos lieka pasiekiamos.",
        "license.trial_status.active": "Licencija aktyvi. Beta funkcijos lieka pasiekiamos.",
        "license.trial_status.expired": "Trial lokaliai pasibaiges. Beta funkcijos lieka pasiekiamos.",
        "license.trial_status.invalid": "Kol kas nera galiojancios lokalios licencijos busenos. Beta funkcijos lieka pasiekiamos.",
        "license.trial_status.unknown": "Trial busena kol kas nepasiekiama.",
        "license.metric.status": "Licencijos busena",
        "license.metric.trial_days": "Likusios trial dienos",
        "license.metric.plan": "Plano pavadinimas",
        "license.metric.allowed_accounts": "Leidziamos Gmail paskyros",
        "license.metric.connected_accounts": "Prijungtos Gmail paskyros",
        "license.status_value.trial": "Trial",
        "license.status_value.active": "Active",
        "license.status_value.expired": "Expired",
        "license.status_value.invalid": "Invalid",
        "license.plan.basic": "Basic Plan",
        "license.plan.personal": "Basic Plan",
        "license.plan.family": "Family Plan",
        "license.plan.pro": "Pro Plan",
        "license.connected_accounts_empty": "Prie sios licencijos dar neprijungta Gmail paskyru.",
        "license.connected_accounts_list": "Prijungtos paskyros: {accounts}",
        "license.plan_limit_exceeded": (
            "Prijungta daugiau Gmail paskyru, nei leidzia dabartinis planas. "
            "Rekomenduojama atnaujinti plana pries ijungiant vieso paleidimo apribojimus."
        ),
        "license.plan_limit_ok": "Dabartinis planas atitinka prijungtu Gmail paskyru naudojima.",
        "license.upgrade_button": "Atnaujinti plana (netrukus)",
        "license.upgrade_note": "Plano atnaujinimas bus pasiekiamas vieso paleidimo metu. Sioje beta versijoje mokejimai nevykdomi.",
        "license.message.trial": "Trial aktyvus. Liko {days} d. Beta funkcijos lieka pasiekiamos.",
        "license.message.active": "{plan} aktyvus. Beta funkcijos lieka pasiekiamos.",
        "license.message.expired": "Lokalus trial pasibaige. Pries viesa paleidima bus galima pasirinkti plana. Beta funkcijos lieka pasiekiamos.",
        "license.message.invalid": "Lokaliai nera aktyvios galiojancios licencijos. Beta funkcijos lieka pasiekiamos.",
    },
}

for language, values in LICENSE_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


FTUE_TRANSLATIONS = {
    "en": {
        "ftue.title": "Find what is costing you money in Gmail.",
        "ftue.subtitle": "Connect Gmail, scan once, and FeeHunt shows subscriptions, savings, and noisy emails.",
        "ftue.step_connect.title": "1. Connect Gmail",
        "ftue.step_connect.body": "Sign in once. Your results stay on this computer.",
        "ftue.step_scan.title": "2. Scan Gmail",
        "ftue.step_scan.body": "FeeHunt looks for subscriptions, payment alerts, and promotions.",
        "ftue.step_review.title": "3. Review savings",
        "ftue.step_review.body": "See what to cancel, keep, or clean up.",
        "ftue.connect_cta": "Connect Gmail",
        "ftue.scan_cta": "Scan Gmail now",
        "ftue.review_cta": "Review my results",
        "ftue.skip": "Show full dashboard",
        "ftue.connected": "Gmail is connected. You are ready to scan.",
        "ftue.aha_title": "Nice. FeeHunt found your first money signals.",
        "ftue.aha_subtitle": "Here is the quick picture from your Gmail scan.",
        "ftue.aha_subscriptions": "Subscriptions found",
        "ftue.aha_savings": "Estimated monthly savings",
        "ftue.aha_promotions": "Promotional emails",
        "ftue.aha_next": "Open Subscriptions",
        "ftue.aha_done": "Continue to dashboard",
        "ftue.privacy_note": "FeeHunt scans on this computer. You stay in control.",
    },
    "lt": {
        "ftue.title": "Raskite, kas Gmail laiškuose kainuoja pinigus.",
        "ftue.subtitle": "Prisijunkite prie Gmail, paleiskite skenavimą, ir FeeHunt parodys prenumeratas, taupymą bei reklaminius laiškus.",
        "ftue.step_connect.title": "1. Prijunkite Gmail",
        "ftue.step_connect.body": "Prisijunkite vieną kartą. Rezultatai lieka šiame kompiuteryje.",
        "ftue.step_scan.title": "2. Nuskenuokite Gmail",
        "ftue.step_scan.body": "FeeHunt ieško prenumeratų, mokėjimų įspėjimų ir reklamų.",
        "ftue.step_review.title": "3. Peržiūrėkite taupymą",
        "ftue.step_review.body": "Matykite, ką atšaukti, pasilikti ar sutvarkyti.",
        "ftue.connect_cta": "Prijungti Gmail",
        "ftue.scan_cta": "Skenuoti Gmail dabar",
        "ftue.review_cta": "Peržiūrėti rezultatus",
        "ftue.skip": "Rodyti visą Dashboard",
        "ftue.connected": "Gmail prijungtas. Galite skenuoti.",
        "ftue.aha_title": "Puiku. FeeHunt rado pirmuosius pinigų signalus.",
        "ftue.aha_subtitle": "Štai trumpas jūsų Gmail skenavimo vaizdas.",
        "ftue.aha_subscriptions": "Rastos prenumeratos",
        "ftue.aha_savings": "Galimas mėnesio taupymas",
        "ftue.aha_promotions": "Reklaminiai laiškai",
        "ftue.aha_next": "Atidaryti prenumeratas",
        "ftue.aha_done": "Tęsti į Dashboard",
        "ftue.privacy_note": "FeeHunt skenuoja šiame kompiuteryje. Jūs liekate valdyti.",
    },
}

for language, values in FTUE_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


TRUST_TRANSLATIONS = {
    "en": {
        "trust.data_private": "Your data stays private",
        "trust.works_locally": "FeeHunt works locally",
        "trust.no_sell": "We do not sell your data",
        "trust.connect_note": "Google sign-in is used only so FeeHunt can scan your Gmail on this computer.",
        "trust.scan_note": "Your scan results stay on this device. You choose what to open, keep, or clean up.",
        "trust.results_note": "These numbers help you decide what deserves attention first.",
        "trust.control": "You stay in control",
    },
    "lt": {
        "trust.data_private": "Jūsų duomenys lieka privatūs",
        "trust.works_locally": "FeeHunt veikia lokaliai",
        "trust.no_sell": "Mes neparduodame jūsų duomenų",
        "trust.connect_note": "Google prisijungimas naudojamas tik tam, kad FeeHunt galėtų skenuoti Gmail šiame kompiuteryje.",
        "trust.scan_note": "Skenavimo rezultatai lieka šiame įrenginyje. Jūs renkatės, ką atidaryti, pasilikti ar sutvarkyti.",
        "trust.results_note": "Šie skaičiai padeda nuspręsti, kam pirmiausia verta skirti dėmesį.",
        "trust.control": "Jūs liekate valdyti",
    },
}

for language, values in TRUST_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


AI_GUIDANCE_TRANSLATIONS = {
    "en": {
        "ai_guidance.title": "Gentle guidance",
        "ai_guidance.subtitle": "FeeHunt noticed a few things that may help you decide what to do next.",
        "ai_guidance.savings": "You may save about {amount}/month.",
        "ai_guidance.subscriptions_many": "I found several subscriptions you may no longer use.",
        "ai_guidance.subscriptions_some": "I found a few subscriptions worth reviewing.",
        "ai_guidance.promotions_many": "Your inbox contains many promotional emails.",
        "ai_guidance.promotions_some": "Some promotional emails may be easy to clean up.",
        "ai_guidance.risk_one": "One payment may need attention soon.",
        "ai_guidance.risk_many": "A few payment alerts may need attention.",
        "ai_guidance.all_clear": "Nothing urgent stands out right now.",
        "ai_guidance.action.review": "Review",
        "ai_guidance.action.unsubscribe": "Unsubscribe",
        "ai_guidance.action.archive_promotions": "Archive promotions",
        "ai_guidance.action.none": "Keep scanning",
        "ai_guidance.cta.review_subscriptions": "Review Subscriptions",
        "ai_guidance.cta.review_financial_risks": "Review payment reminders",
        "ai_guidance.cta.archive_promotions": "Archive Promotions",
        "ai_guidance.cta.open_unsubscribe_options": "Open Unsubscribe Options",
        "ai_guidance.cta.no_action": "No action needed",
        "ai_guidance.archived_promotions": "Done - archived {count} promotional email(s). Your important emails were not touched.",
        "ai_guidance.undo_promotions": "Undo archive promotions",
        "ai_guidance.undo_promotions_done": "Undone - promotional emails were returned to your inbox.",
        "ai_guidance.archive_none": "No promotional emails are ready to archive right now.",
        "ai_guidance.calm_title": "Everything looks calm right now.",
        "ai_guidance.calm_body": "No urgent action is needed. You can come back anytime and scan again.",
        "ai_guidance.why.savings": "Shown because FeeHunt found subscription-related emails with estimated costs.",
        "ai_guidance.why.subscriptions": "Shown because FeeHunt found subscriptions worth reviewing.",
        "ai_guidance.why.promotions": "Shown because promotional senders appear often in this scan.",
        "ai_guidance.why.risk": "Shown because FeeHunt found payment or account alerts.",
        "ai_guidance.happens.review": "This opens the review page. Nothing changes in Gmail.",
        "ai_guidance.happens.unsubscribe": "This opens emails with unsubscribe options. You choose what to open.",
        "ai_guidance.happens.archive_promotions": "This will only archive emails FeeHunt marked as promotional.",
        "ai_guidance.safe_delete": "FeeHunt never deletes emails without confirmation.",
        "ai_guidance.confirm_archive": "Yes, archive promotional emails",
        "ai_guidance.cancel_action": "Not now",
        "safe_action.explain.archive": "Archive moves this email out of your inbox. It will not be deleted.",
        "safe_action.explain.delete": "Delete moves this email to trash. It is not permanently deleted.",
        "safe_action.explain.spam": "Spam moves this email to Gmail spam. Other emails are not touched.",
        "safe_action.explain.unsubscribe": "Unsubscribe opens the sender's page. FeeHunt will not unsubscribe for you.",
        "safe_action.confirm.archive": "Yes, archive this email",
        "safe_action.confirm.delete": "Yes, move to trash",
        "safe_action.confirm.spam": "Yes, mark as spam",
        "safe_action.open_unsubscribe": "Open unsubscribe page",
        "safe_action.cancel": "Cancel",
        "safe_action.done_archive": "Done - archived this email. Your other emails were not touched.",
        "safe_action.done_delete": "Done - moved this email to trash. It was not permanently deleted.",
        "safe_action.done_spam": "Done - marked this email as spam. Your other emails were not touched.",
        "safe_action.done_unsubscribe": "Opened unsubscribe page. You stay in control.",
        "safe_action.undo": "Undo",
        "safe_action.undo_done": "Undone. The email was restored.",
        "safe_action.failed": "FeeHunt could not finish that action. Please check Gmail or try again in a moment.",
    },
    "lt": {
        "ai_guidance.title": "Ramus patarimas",
        "ai_guidance.subtitle": "FeeHunt pastebėjo kelis dalykus, kurie gali padėti nuspręsti, ką daryti toliau.",
        "ai_guidance.savings": "Galite sutaupyti apie {amount}/mėn.",
        "ai_guidance.subscriptions_many": "Radau kelias prenumeratas, kurių galbūt nebenaudojate.",
        "ai_guidance.subscriptions_some": "Radau kelias prenumeratas, kurias verta peržiūrėti.",
        "ai_guidance.promotions_many": "Gautuosiuose yra daug reklaminių laiškų.",
        "ai_guidance.promotions_some": "Kai kuriuos reklaminius laiškus gali būti lengva sutvarkyti.",
        "ai_guidance.risk_one": "Vienam mokėjimui gali greitai reikėti dėmesio.",
        "ai_guidance.risk_many": "Keli mokėjimų įspėjimai gali reikėti dėmesio.",
        "ai_guidance.all_clear": "Šiuo metu nieko skubaus nematyti.",
        "ai_guidance.action.review": "Peržiūrėti",
        "ai_guidance.action.unsubscribe": "Atsisakyti",
        "ai_guidance.action.archive_promotions": "Archyvuoti reklamas",
        "ai_guidance.action.none": "Skenuoti vėliau",
        "ai_guidance.cta.review_subscriptions": "Peržiūrėti prenumeratas",
        "ai_guidance.cta.review_financial_risks": "Peržiūrėti mokėjimų priminimus",
        "ai_guidance.cta.archive_promotions": "Archyvuoti reklamas",
        "ai_guidance.cta.open_unsubscribe_options": "Atidaryti atsisakymo galimybes",
        "ai_guidance.cta.no_action": "Veiksmų nereikia",
        "ai_guidance.archived_promotions": "Atlikta - archyvuota reklaminių laiškų: {count}. Svarbūs laiškai nebuvo paliesti.",
        "ai_guidance.undo_promotions": "Atšaukti reklamų archyvavimą",
        "ai_guidance.undo_promotions_done": "Atšaukta - reklaminiai laiškai grąžinti į gautuosius.",
        "ai_guidance.archive_none": "Šiuo metu nėra reklaminių laiškų, paruoštų archyvavimui.",
        "ai_guidance.calm_title": "Šiuo metu viskas atrodo ramiai.",
        "ai_guidance.calm_body": "Skubių veiksmų nereikia. Galite bet kada grįžti ir nuskenuoti dar kartą.",
        "ai_guidance.why.savings": "Rodoma, nes FeeHunt rado prenumeratų laiškų su galimomis išlaidomis.",
        "ai_guidance.why.subscriptions": "Rodoma, nes FeeHunt rado prenumeratų, kurias verta peržiūrėti.",
        "ai_guidance.why.promotions": "Rodoma, nes šiame skenavime dažnai kartojasi reklaminiai siuntėjai.",
        "ai_guidance.why.risk": "Rodoma, nes FeeHunt rado mokėjimų ar paskyrų įspėjimų.",
        "ai_guidance.happens.review": "Bus atidarytas peržiūros puslapis. Gmail niekas nepasikeis.",
        "ai_guidance.happens.unsubscribe": "Bus atidaryti laiškai su atsisakymo galimybėmis. Jūs renkatės, ką atidaryti.",
        "ai_guidance.happens.archive_promotions": "Bus archyvuoti tik tie laiškai, kuriuos FeeHunt pažymėjo kaip reklaminius.",
        "ai_guidance.safe_delete": "FeeHunt niekada netrina laiškų be patvirtinimo.",
        "ai_guidance.confirm_archive": "Taip, archyvuoti reklaminius laiškus",
        "ai_guidance.cancel_action": "Ne dabar",
        "safe_action.explain.archive": "Archyvavimas pašalina šį laišką iš gautųjų. Jis nebus ištrintas.",
        "safe_action.explain.delete": "Trinimas perkelia šį laišką į šiukšlinę. Jis nebus ištrintas visam laikui.",
        "safe_action.explain.spam": "Spam veiksmas perkelia šį laišką į Gmail šlamštą. Kiti laiškai neliečiami.",
        "safe_action.explain.unsubscribe": "Atsisakymas atidaro siuntėjo puslapį. FeeHunt neatšaukia prenumeratos už jus.",
        "safe_action.confirm.archive": "Taip, archyvuoti šį laišką",
        "safe_action.confirm.delete": "Taip, perkelti į šiukšlinę",
        "safe_action.confirm.spam": "Taip, pažymėti kaip spam",
        "safe_action.open_unsubscribe": "Atidaryti atsisakymo puslapį",
        "safe_action.cancel": "Atšaukti",
        "safe_action.done_archive": "Atlikta - laiškas archyvuotas. Kiti laiškai nebuvo paliesti.",
        "safe_action.done_delete": "Atlikta - laiškas perkeltas į šiukšlinę. Jis neištrintas visam laikui.",
        "safe_action.done_spam": "Atlikta - laiškas pažymėtas kaip spam. Kiti laiškai nebuvo paliesti.",
        "safe_action.done_unsubscribe": "Atsisakymo puslapis atidarytas. Jūs liekate valdyti.",
        "safe_action.undo": "Atšaukti veiksmą",
        "safe_action.undo_done": "Atšaukta. Laiškas atkurtas.",
        "safe_action.failed": "FeeHunt nepavyko atlikti veiksmo. Patikrinkite Gmail arba pabandykite dar kartą.",
    },
}

for language, values in AI_GUIDANCE_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


PROGRESS_TRANSLATIONS = {
    "en": {
        "progress.title": "This month FeeHunt helped you...",
        "progress.subtitle": "Small steps toward a calmer inbox and clearer spending.",
        "progress.reviewed_subscriptions": "Subscriptions to review",
        "progress.archived_promotions": "Promotions archived",
        "progress.potential_savings": "Potential savings",
        "progress.resolved_risks": "Payment reminders to review",
        "progress.calm_inbox": "Your inbox looks calmer than last week.",
        "progress.no_urgent_risks": "No payment reminders need attention.",
        "progress.reduced_clutter": "You reduced promotional clutter.",
        "progress.keep_going": "You are building more control, one scan at a time.",
        "progress.no_scan": "Run a scan to start seeing your progress here.",
    },
    "lt": {
        "progress.title": "Šį mėnesį FeeHunt jums padėjo...",
        "progress.subtitle": "Maži žingsniai ramesniam paštui ir aiškesnėms išlaidoms.",
        "progress.reviewed_subscriptions": "Prenumeratos peržiūrai",
        "progress.archived_promotions": "Archyvuotos reklamos",
        "progress.potential_savings": "Galimas taupymas",
        "progress.resolved_risks": "Mokėjimų priminimai peržiūrai",
        "progress.calm_inbox": "Jūsų paštas atrodo ramesnis nei praėjusią savaitę.",
        "progress.no_urgent_risks": "Mokėjimų priminimų, kuriems reikia dėmesio, nerasta.",
        "progress.reduced_clutter": "Sumažinote reklaminį triukšmą.",
        "progress.keep_going": "Kiekvienas skenavimas suteikia daugiau kontrolės.",
        "progress.no_scan": "Paleiskite skenavimą, kad čia matytumėte progresą.",
    },
}

for language, values in PROGRESS_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


DAILY_INSIGHT_TRANSLATIONS = {
    "en": {
        "daily_insight.label": "Daily insight",
        "daily_insight.no_urgent": "No urgent actions needed today.",
        "daily_insight.calmer_week": "Your inbox looks calmer this week.",
        "daily_insight.subscription_cost": "One subscription may be worth checking today.",
        "daily_insight.promotions_down": "Promotional clutter decreased recently.",
        "daily_insight.promotions_attention": "A few promotions may be easy to clear later.",
        "daily_insight.risk_review": "One payment note may be worth a quick look.",
        "daily_insight.savings_review": "A small review may help protect {amount}/month.",
    },
    "lt": {
        "daily_insight.label": "Dienos įžvalga",
        "daily_insight.no_urgent": "Šiandien skubių veiksmų nereikia.",
        "daily_insight.calmer_week": "Šią savaitę paštas atrodo ramesnis.",
        "daily_insight.subscription_cost": "Vieną prenumeratą šiandien verta patikrinti.",
        "daily_insight.promotions_down": "Reklaminio triukšmo pastaruoju metu mažiau.",
        "daily_insight.promotions_attention": "Kelias reklamas vėliau gali būti lengva sutvarkyti.",
        "daily_insight.risk_review": "Vieną mokėjimo pranešimą verta trumpai peržiūrėti.",
        "daily_insight.savings_review": "Trumpa peržiūra gali padėti apsaugoti {amount}/mėn.",
    },
}

for language, values in DAILY_INSIGHT_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


TIME_TRANSLATIONS = {
    "en": {
        "greeting.morning": "Good morning.",
        "greeting.afternoon": "Good afternoon.",
        "greeting.evening": "Good evening.",
        "greeting.late": "Welcome back.",
        "greeting.context": "FeeHunt is ready when you are.",
        "settings.timezone": "Timezone",
        "settings.timezone_help": "Used for greetings, daily insights, trial timing, and future reminders.",
    },
    "lt": {
        "greeting.morning": "Labas rytas.",
        "greeting.afternoon": "Laba diena.",
        "greeting.evening": "Labas vakaras.",
        "greeting.late": "Sveiki sugrįžę.",
        "greeting.context": "FeeHunt pasiruošęs, kai būsite pasiruošę jūs.",
        "settings.timezone": "Laiko zona",
        "settings.timezone_help": "Naudojama pasisveikinimams, dienos įžvalgoms, trial laikui ir būsimiems priminimams.",
    },
}

for language, values in TIME_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


ADAPTIVE_UX_TRANSLATIONS = {
    "en": {
        "adaptive.new": "I will keep the first steps simple.",
        "adaptive.overwhelmed": "There is a lot here, so FeeHunt will suggest one calm next step at a time.",
        "adaptive.calm": "Things look calm. FeeHunt will stay quiet unless something useful appears.",
        "adaptive.returning": "Welcome back. FeeHunt will show only what changed and what matters most.",
        "adaptive.steady": "FeeHunt found a few useful signals and will keep the guidance light.",
    },
    "lt": {
        "adaptive.new": "Pirmus žingsnius rodysiu kuo paprasčiau.",
        "adaptive.overwhelmed": "Čia yra nemažai informacijos, todėl FeeHunt siūlys po vieną ramų kitą žingsnį.",
        "adaptive.calm": "Viskas atrodo ramiai. FeeHunt netrukdys, kol neatsiras naudingas signalas.",
        "adaptive.returning": "Sveiki sugrįžę. FeeHunt rodys tik tai, kas pasikeitė ir kas svarbiausia.",
        "adaptive.steady": "FeeHunt rado kelis naudingus signalus ir pagalbą rodys lengvai.",
    },
}

for language, values in ADAPTIVE_UX_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


MEMORY_TRANSLATIONS = {
    "en": {
        "memory.trust.local": "Stored locally on your device",
        "memory.trust.private": "FeeHunt remembers your progress privately",
        "memory.settings_title": "Local memory",
        "memory.settings_note": "Progress history stays on this computer and is not sent to the cloud.",
        "memory.clear_history": "Clear progress history",
        "memory.reset_onboarding": "Reset onboarding",
        "memory.disable_adaptive": "Disable adaptive guidance",
        "memory.enabled_adaptive": "Use gentle adaptive guidance",
        "memory.cleared": "Progress history cleared locally.",
        "memory.onboarding_reset": "Onboarding will show again next time.",
        "memory.saved": "Memory settings saved.",
        "control.title": "Main controls",
        "control.subtitle": "Start with one calm action. FeeHunt will explain what happens next.",
        "control.subtitle.new": "Start with Gmail. FeeHunt will keep the first step simple and private.",
        "control.subtitle.overwhelmed": "Choose one small next step. FeeHunt will help you reduce the noise slowly.",
        "control.subtitle.calm": "Everything looks calm. Scan again only when you want a fresh check.",
        "control.subtitle.returning": "Welcome back. Start with a fresh scan when you are ready.",
        "control.subtitle.steady": "FeeHunt is ready for a light check when you need it.",
        "control.connected": "Gmail connected",
        "control.not_connected": "Gmail not connected yet",
        "control.scan_ready": "Ready to scan when you are.",
    },
    "lt": {
        "memory.trust.local": "Saugoma lokaliai šiame įrenginyje",
        "memory.trust.private": "FeeHunt privačiai prisimena jūsų progresą",
        "memory.settings_title": "Lokali atmintis",
        "memory.settings_note": "Progreso istorija lieka šiame kompiuteryje ir nesiunčiama į cloud.",
        "memory.clear_history": "Išvalyti progreso istoriją",
        "memory.reset_onboarding": "Iš naujo rodyti onboarding",
        "memory.disable_adaptive": "Išjungti prisitaikančią pagalbą",
        "memory.enabled_adaptive": "Naudoti švelnią prisitaikančią pagalbą",
        "memory.cleared": "Progreso istorija išvalyta lokaliai.",
        "memory.onboarding_reset": "Onboarding bus parodytas dar kartą.",
        "memory.saved": "Atminties nustatymai išsaugoti.",
        "control.title": "Pagrindinis valdymas",
        "control.subtitle": "Pradėkite nuo vieno ramaus veiksmo. FeeHunt paaiškins, kas vyks toliau.",
        "control.subtitle.new": "Pradėkite nuo Gmail. FeeHunt pirmą žingsnį paliks paprastą ir privatų.",
        "control.subtitle.overwhelmed": "Pasirinkite vieną mažą kitą žingsnį. FeeHunt padės triukšmą mažinti ramiai.",
        "control.subtitle.calm": "Viskas atrodo ramiai. Skenuokite dar kartą, kai norėsite šviežio patikrinimo.",
        "control.subtitle.returning": "Sveiki sugrįžę. Pradėkite nuo naujo skenavimo, kai būsite pasiruošę.",
        "control.subtitle.steady": "FeeHunt pasiruošęs lengvam patikrinimui, kai jo prireiks.",
        "control.connected": "Gmail prijungtas",
        "control.not_connected": "Gmail dar neprijungtas",
        "control.scan_ready": "Galite skenuoti, kai būsite pasiruošę.",
    },
}

for language, values in MEMORY_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


REINFORCEMENT_TRANSLATIONS = {
    "en": {
        "reinforcement.inbox_easier": "Your inbox is becoming easier to manage.",
        "reinforcement.promotions_down": "Nice work - promotional clutter decreased.",
        "reinforcement.subscriptions_reviewed": "You reviewed several subscriptions recently.",
        "reinforcement.control": "You are building more control, one calm step at a time.",
        "reinforcement.quiet_progress": "Small progress counts. FeeHunt will keep this simple.",
    },
    "lt": {
        "reinforcement.inbox_easier": "Jūsų paštą darosi lengviau valdyti.",
        "reinforcement.promotions_down": "Puiku - reklaminio triukšmo sumažėjo.",
        "reinforcement.subscriptions_reviewed": "Pastaruoju metu peržiūrėjote kelias prenumeratas.",
        "reinforcement.control": "Kuriate daugiau kontrolės - po vieną ramų žingsnį.",
        "reinforcement.quiet_progress": "Mažas progresas svarbus. FeeHunt išlaikys viską paprastai.",
    },
}

for language, values in REINFORCEMENT_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


WELCOME_TRANSLATIONS = {
    "en": {
        "welcome.language_label": "Choose language",
        "welcome.kicker": "Safe Gmail control",
        "welcome.title": "Your Gmail. Back under control.",
        "welcome.subtitle": (
            "FeeHunt helps you find subscriptions, payment notes, and promotional noise "
            "without making your inbox feel harder to manage."
        ),
        "welcome.trust.local": "Works locally",
        "welcome.trust.private": "Your data stays private",
        "welcome.trust.control": "Gmail access stays under your control",
        "welcome.principle": "FeeHunt works for you. You stay in control.",
        "welcome.preview.title": "Manage calmly",
        "welcome.preview.subscriptions": "Subscriptions",
        "welcome.preview.payments": "Paid apps",
        "welcome.preview.promotions": "Promotions",
        "welcome.first_step": "First simple step",
        "welcome.activation_note": "Paste the FeeHunt key from your email. After this, you can connect Gmail safely.",
        "welcome.license_label": "FeeHunt license key",
        "welcome.activate_button": "Continue",
        "welcome.empty_key": "Paste your FeeHunt key first. You can find it in your email.",
        "welcome.activated": "FeeHunt is ready. Next, you can connect Gmail safely.",
        "welcome.secondary_intro": "Need a key or returning to your account?",
        "welcome.get_key": "Get your FeeHunt key",
        "welcome.returning_prompt": "Already started?",
        "welcome.start_trial": "Start free trial",
        "welcome.resend_key": "Resend key",
        "welcome.preview_dashboard": "Preview Dashboard",
        "welcome.preview_note": "Explore FeeHunt with sample results. Gmail will not be touched.",
        "preview.banner": "Preview mode - sample results only. No Gmail action will run.",
        "preview.exit": "Exit preview",
        "preview.status": "Preview mode",
        "preview.status_caption": "Sample data is loaded so you can see the controls safely.",
        "preview.action_disabled": "This is preview mode. Real Gmail actions are disabled.",
    },
    "lt": {
        "welcome.language_label": "Pasirinkite kalbą",
        "welcome.kicker": "Saugi Gmail kontrolė",
        "welcome.title": "Jūsų Gmail. Vėl jūsų kontrolėje.",
        "welcome.subtitle": (
            "FeeHunt padeda rasti prenumeratas, mokėjimų pranešimus ir reklaminį triukšmą "
            "neapsunkindamas jūsų pašto."
        ),
        "welcome.trust.local": "Veikia lokaliai",
        "welcome.trust.private": "Jūsų duomenys lieka privatūs",
        "welcome.trust.control": "Gmail prieiga lieka jūsų kontrolėje",
        "welcome.principle": "FeeHunt dirba už jus. Jūs valdote.",
        "welcome.preview.title": "Valdykite ramiau",
        "welcome.preview.subscriptions": "Prenumeratos",
        "welcome.preview.payments": "Mokamos programos",
        "welcome.preview.promotions": "Reklamos",
        "welcome.first_step": "Pirmas paprastas žingsnis",
        "welcome.activation_note": "Įklijuokite FeeHunt raktą iš el. laiško. Po to galėsite saugiai prijungti Gmail.",
        "welcome.license_label": "FeeHunt licencijos raktas",
        "welcome.activate_button": "Tęsti",
        "welcome.empty_key": "Pirmiausia įklijuokite FeeHunt raktą. Jį rasite savo el. pašte.",
        "welcome.activated": "FeeHunt paruoštas. Toliau galėsite saugiai prijungti Gmail.",
        "welcome.secondary_intro": "Reikia rakto arba norite grįžti į paskyrą?",
        "welcome.get_key": "Gauti FeeHunt raktą",
        "welcome.returning_prompt": "Jau pradėjote?",
        "welcome.start_trial": "Pradėti nemokamą bandymą",
        "welcome.resend_key": "Atsiųsti raktą dar kartą",
        "welcome.preview_dashboard": "Peržiūrėti Dashboard",
        "welcome.preview_note": "Apžiūrėkite FeeHunt su pavyzdiniais rezultatais. Gmail nebus paliestas.",
        "preview.banner": "Peržiūros režimas - rodomi tik pavyzdiniai rezultatai. Gmail veiksmai nevykdomi.",
        "preview.exit": "Išeiti iš peržiūros",
        "preview.status": "Peržiūros režimas",
        "preview.status_caption": "Įkelti pavyzdiniai duomenys, kad saugiai matytumėte valdymą.",
        "preview.action_disabled": "Tai peržiūros režimas. Tikri Gmail veiksmai išjungti.",
    },
}

for language, values in WELCOME_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


READINESS_TRANSLATIONS = {
    "en": {
        "onboarding.app_file_title": "FeeHunt needs one app file before Gmail sign-in can open.",
        "onboarding.app_file_fix": (
            "Please download FeeHunt again, extract the full ZIP, and open FeeHunt from the extracted folder. "
            "Your Gmail data is not changed."
        ),
        "onboarding.zip_tip": "Tip: do not run FeeHunt directly from inside the ZIP file.",
        "gmail.connected_success": "Gmail connected. Your data stays on this computer.",
        "license.banner_active": "{plan} plan active. {days} day(s) remaining.",
        "license.banner_inactive": "Your FeeHunt trial has expired or could not be verified.",
        "license.upgrade_now": "Upgrade FeeHunt",
        "license.account_heading": "FeeHunt Account",
        "license.key_display": "License key: {key}",
        "license.check_now": "Check license now",
        "license.deactivate": "Deactivate FeeHunt license",
        "scan.loading.reviewing": "Reviewing your Gmail...",
        "scan.loading.looking": "Looking for subscriptions and payment reminders...",
        "scan.loading.organizing": "Organizing recent email activity...",
        "scan.loading.preparing": "FeeHunt is preparing your overview...",
        "scan.loading.recent": "Reviewing recent email activity...",
        "scan.loading.reassurance_approval": "Nothing changes without your approval.",
        "scan.loading.reassurance_control": "Your Gmail stays under your control.",
        "scan.loading.reassurance_device": "Your data stays on this device.",
        "scan.loading.complete": "Your Gmail overview is ready.",
        "scan.loading.not_complete": "FeeHunt could not finish this scan.",
        "scan.loading.progress_detail": "{current} of {total} recent emails reviewed.",
    },
    "lt": {
        "onboarding.app_file_title": "FeeHunt reikia vieno programos failo, kad galėtų atidaryti Gmail prisijungimą.",
        "onboarding.app_file_fix": (
            "Atsisiųskite FeeHunt dar kartą, išskleiskite visą ZIP ir paleiskite programą iš išskleisto aplanko. "
            "Jūsų Gmail duomenys nebus pakeisti."
        ),
        "onboarding.zip_tip": "Patarimas: nepaleiskite FeeHunt tiesiai iš ZIP failo.",
        "gmail.connected_success": "Gmail prijungtas. Jūsų duomenys lieka šiame kompiuteryje.",
        "license.banner_active": "{plan} planas aktyvus. Liko {days} d.",
        "license.banner_inactive": "FeeHunt trial pasibaigė arba licencijos nepavyko patikrinti.",
        "license.upgrade_now": "Atnaujinti FeeHunt",
        "license.account_heading": "FeeHunt paskyra",
        "license.key_display": "Licencijos raktas: {key}",
        "license.check_now": "Patikrinti licenciją dabar",
        "license.deactivate": "Išjungti FeeHunt licenciją",
        "scan.loading.reviewing": "Peržiūrime jūsų Gmail...",
        "scan.loading.looking": "Ieškome prenumeratų ir mokėjimų priminimų...",
        "scan.loading.organizing": "Tvarkome naujausią el. pašto veiklą...",
        "scan.loading.preparing": "FeeHunt ruošia jūsų apžvalgą...",
        "scan.loading.recent": "Peržiūrime naujausius laiškus...",
        "scan.loading.reassurance_approval": "Niekas nekeičiama be jūsų patvirtinimo.",
        "scan.loading.reassurance_control": "Jūsų Gmail lieka jūsų kontrolėje.",
        "scan.loading.reassurance_device": "Jūsų duomenys lieka šiame įrenginyje.",
        "scan.loading.complete": "Jūsų Gmail apžvalga paruošta.",
        "scan.loading.not_complete": "FeeHunt nepavyko užbaigti skenavimo.",
        "scan.loading.progress_detail": "Peržiūrėta {current} iš {total} naujausių laiškų.",
    },
}

for language, values in READINESS_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(language, {}).update(values)


CONTEXTUAL_HELP = {
    "en": {
        "connect_gmail": "Connect once so FeeHunt can read your Gmail safely on this computer.",
        "scan_gmail": "Look through recent Gmail messages and show what may need attention.",
        "estimated_savings": "A simple monthly estimate from subscriptions FeeHunt found.",
        "financial_risks": "Payment or account emails worth checking soon.",
        "promotions": "Marketing emails you may want to clean up.",
        "unsubscribe": "Open the sender's unsubscribe page when FeeHunt can find one.",
        "license_activation": "Paste your FeeHunt key once to unlock your account.",
        "trial_status": "See how many trial days are left.",
    },
    "lt": {
        "connect_gmail": "Prisijunkite vieną kartą, kad FeeHunt galėtų saugiai peržiūrėti Gmail šiame kompiuteryje.",
        "scan_gmail": "Peržiūrėti naujausius Gmail laiškus ir parodyti, kam verta skirti dėmesį.",
        "estimated_savings": "Paprastas mėnesio įvertis pagal rastas prenumeratas.",
        "financial_risks": "Mokėjimų ar paskyrų laiškai, kuriuos verta greitai patikrinti.",
        "promotions": "Reklaminiai laiškai, kuriuos galbūt norėsite sutvarkyti.",
        "unsubscribe": "Atidaryti prenumeratos atsisakymo puslapį, jei FeeHunt jį randa.",
        "license_activation": "Vieną kartą įklijuokite FeeHunt raktą, kad aktyvuotumėte paskyrą.",
        "trial_status": "Pažiūrėkite, kiek trial dienų dar liko.",
    },
}


LANGUAGE_ALIASES = {
    "english": "en",
    "en": "en",
    "lietuvių": "lt",
    "lietuviu": "lt",
    "lt": "lt",
}

AUTO_SCAN_ALIASES = {
    "išjungtas": "off",
    "isjungtas": "off",
    "off": "off",
    "kas valandą": "hourly",
    "kas valanda": "hourly",
    "hourly": "hourly",
    "kartą per dieną": "daily",
    "karta per diena": "daily",
    "daily": "daily",
}


def normalize_language(lang="en"):
    return LANGUAGE_ALIASES.get(str(lang or "en").strip().lower(), "en")


def normalize_auto_scan(value="off"):
    return AUTO_SCAN_ALIASES.get(str(value or "off").strip().lower(), "off")


def t(key, lang="en"):
    language = normalize_language(lang)
    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(
        key,
        TRANSLATIONS["en"].get(key, key),
    )


def help_text(key, lang="en"):
    language = normalize_language(lang)
    return CONTEXTUAL_HELP.get(language, CONTEXTUAL_HELP["en"]).get(
        key,
        CONTEXTUAL_HELP["en"].get(key, key),
    )
