TRANSLATIONS = {
    "en": {
        "dashboard.title": "💸 Dashboard",
        "dashboard.subtitle": "See what FeeHunt found and choose what to do next.",
        "dashboard.plan_info": (
            "FeeHunt scans one Gmail account at a time and keeps your results on this computer. "
            "Use it to spot subscriptions, payment issues, and promotional noise."
        ),
        "dashboard.auto_cleanup_on": "⚡ **Automatic cleanup is on.** Your Cleanup Rules will run after each scan.",
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
            "⚠️ **credentials.json file not found.** "
            "This file is required so FeeHunt can connect to your Gmail account."
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
        "onboarding.file_not_found": "❌ File not found yet: {path}",
        "onboarding.footer": "Privacy-first • FeeHunt never stores your data in the cloud",
        "scan.progress_preparing": "Preparing to scan...",
        "scan.main_missing": "File not found: {path}",
        "app.brand_title": "💸 FeeHunt",
        "sidebar.caption": "1 plan = 1 email account",
        "sidebar.navigation": "Navigation",
        "sidebar.footer": "Privacy-first • Local data",
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
            "- **Financial Risks** are emails that may need attention, such as declined cards or suspended accounts.\n"
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
        "subscriptions.page_title": "📄 Subscriptions and Financial Risks",
        "subscriptions.no_scan": "📭 No scan has been run yet.",
        "subscriptions.no_scan_instruction": "Go to **Dashboard** and click **🔍 Scan Gmail**.",
        "subscriptions.heading": "🔄 Subscriptions",
        "subscriptions.found": "Found **{count}** subscription-related emails.",
        "subscriptions.none": "✅ No subscription alerts found.",
        "financial_risks.heading": "💳 Financial Risks",
        "financial_risks.warning": (
            "Found **{count}** emails that may need payment attention. "
            "Review them carefully before taking action."
        ),
        "financial_risks.none": "✅ No payment risk emails found.",
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
        "email.missing_message_id": "message_id not found.",
        "email.actions_label": "**Actions:**",
        "email.no_subject": "(no subject)",
        "actions.whitelist_help": "FeeHunt will never touch emails from this sender",
        "actions.blacklist_help": "FeeHunt will automatically delete emails from this sender",
        "bulk.caption": "Bulk actions:",
        "bulk.result": "{label}: {count} emails.",
        "bulk.errors": "Errors: {count}",
        "bulk.archived": "Archived",
        "bulk.deleted": "Deleted",
        "bulk.spam": "Marked as spam",
        "status.main_found": "main.py found",
        "status.main_missing": "main.py not found",
        "status.results_found": "last_scan_results.json found",
        "status.not_created": "Not created yet",
        "status.credentials_found": "credentials.json found",
        "status.credentials_missing": "credentials.json not found",
        "status.app_folder": "App folder: {path}",
        "rules.reason_whitelist": "Whitelist",
        "rules.reason_blacklist": "Blacklist",
        "rules.error": "Error: {error}",
        "rules.delete_error": "Delete error: {error}",
        "rules.archive_error": "Archive error: {error}",
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
        "cleanup.done": "✅ Done! Deleted: **{deleted}**, archived: **{archived}**.",
        "cleanup.review_waiting": "❓ Waiting for your decision: **{review}** emails (see **Cleanup results**).",
        "cleanup.scan_first": "Run a Gmail scan from the Dashboard first.",
        "cleanup.save_error": "Could not save settings.",
        "cleanup.whitelist_title": "✅ Whitelist",
        "cleanup.whitelist_caption": "FeeHunt will never touch emails from these senders, even if a rule says otherwise.",
        "cleanup.whitelist_input": "Add sender (email address or domain)",
        "cleanup.whitelist_placeholder": "e.g. bank@example.com or example.com",
        "cleanup.whitelist_add": "➕ Add to whitelist",
        "cleanup.whitelist_added": "✅ '{sender}' added.",
        "cleanup.whitelist_current": "**Currently in whitelist:**",
        "cleanup.whitelist_empty": "Whitelist is empty.",
        "cleanup.blacklist_title": "🚫 Blacklist",
        "cleanup.blacklist_caption": "Emails from these senders will always be deleted automatically without confirmation.",
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
        "category.financial_risks.label": "Financial risks",
        "category.financial_risks.description": "Failed payments, card problems, debts",
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
        "settings.apply_rules": "⚡ Apply Cleanup Rules after each scan",
        "settings.apply_rules_help": "When enabled, FeeHunt applies your saved cleanup rules after each Gmail scan.",
        "settings.safe_mode": "🔒 Safe mode",
        "settings.safe_mode_help": "Recommended while FeeHunt is in beta.",
        "settings.max_dashboard": "How many emails to show on the Dashboard page",
        "settings.save": "💾 Save settings",
        "settings.saved": "✅ Settings saved.",
        "settings.save_error": "Could not save settings.",
        "settings.technical_info": "🔧 Technical information",
        "gmail.credentials_missing": "credentials.json file not found: {path}",
        "subscription.opened_unsubscribe": "Opened unsubscribe page for {service_name}.",
        "subscription.opened_billing": "Opened billing page for {service_name}.",
        "subscription.opened_search": "Opened search results for {service_name}. Look for Billing or Subscription settings.",
        "runner.app_missing": "Error: File not found: {path}",
        "runner.check_internal": "Check whether app.py was included in the dist\\FeeHunt\\_internal folder.",
        "runner.press_enter": "Press Enter to close...",
    },
    "lt": {
        "dashboard.title": "💸 Dashboard",
        "dashboard.subtitle": "Peržiūrėkite, ką FeeHunt rado, ir pasirinkite kitą veiksmą.",
        "dashboard.plan_info": (
            "FeeHunt skenuoja vieną Gmail paskyrą vienu metu ir saugo rezultatus šiame kompiuteryje. "
            "Naudokite jį prenumeratoms, mokėjimų įspėjimams ir reklaminiam triukšmui rasti."
        ),
        "dashboard.auto_cleanup_on": "⚡ **Automatinis valymas įjungtas.** Cleanup Rules bus pritaikytos po kiekvieno skenavimo.",
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
            "- **Finansinės rizikos** yra laiškai, kuriems gali reikėti dėmesio, pvz. atmestos kortelės ar sustabdytos paskyros.\n"
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
        "financial_risks.heading": "💳 Finansinės grėsmės",
        "financial_risks.warning": (
            "Rasta **{count}** laiškų, kuriems gali reikėti mokėjimų dėmesio. "
            "Peržiūrėkite juos prieš imdamiesi veiksmų."
        ),
        "financial_risks.none": "✅ Mokėjimų rizikos laiškų nerasta.",
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
        "email.missing_message_id": "message_id nerastas.",
        "email.actions_label": "**Veiksmai:**",
        "email.no_subject": "(be temos)",
        "actions.whitelist_help": "FeeHunt niekada nelies šio siuntėjo laiškų",
        "actions.blacklist_help": "FeeHunt automatiškai trins šio siuntėjo laiškus",
        "bulk.caption": "Masiniai veiksmai:",
        "bulk.result": "{label}: {count} laiškų.",
        "bulk.errors": "Klaidos: {count}",
        "bulk.archived": "Archyvuota",
        "bulk.deleted": "Ištrinta",
        "bulk.spam": "Pažymėta šlamštu",
        "status.main_found": "main.py rastas",
        "status.main_missing": "main.py nerastas",
        "status.results_found": "last_scan_results.json rastas",
        "status.not_created": "Dar nesukurtas",
        "status.credentials_found": "credentials.json rastas",
        "status.credentials_missing": "credentials.json nerastas",
        "status.app_folder": "App folder: {path}",
        "rules.reason_whitelist": "Baltasis sąrašas",
        "rules.reason_blacklist": "Juodasis sąrašas",
        "rules.error": "Klaida: {error}",
        "rules.delete_error": "Klaida trinant: {error}",
        "rules.archive_error": "Klaida archyvuojant: {error}",
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
        "cleanup.done": "✅ Baigta! Ištrinta: **{deleted}**, archyvuota: **{archived}**.",
        "cleanup.review_waiting": "❓ Laukia jūsų sprendimo: **{review}** laiškų (žr. **Valymo rezultatai**).",
        "cleanup.scan_first": "Pirmiausia atlikite Gmail skenavimą Dashboard puslapyje.",
        "cleanup.save_error": "Nepavyko išsaugoti nustatymų.",
        "cleanup.whitelist_title": "✅ Baltasis sąrašas",
        "cleanup.whitelist_caption": "Šių siuntėjų laiškų FeeHunt niekada nelies – net jei taisyklė sako kitaip.",
        "cleanup.whitelist_input": "Pridėti siuntėją (el. pašto adresas arba domenas)",
        "cleanup.whitelist_placeholder": "pvz. bankas@seb.lt arba seb.lt",
        "cleanup.whitelist_add": "➕ Pridėti į baltąjį sąrašą",
        "cleanup.whitelist_added": "✅ '{sender}' pridėtas.",
        "cleanup.whitelist_current": "**Šiuo metu baltajame sąraše:**",
        "cleanup.whitelist_empty": "Baltasis sąrašas tuščias.",
        "cleanup.blacklist_title": "🚫 Juodasis sąrašas",
        "cleanup.blacklist_caption": "Šių siuntėjų laiškai bus automatiškai ištrinti – visada, be patvirtinimo.",
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
        "category.financial_risks.label": "Finansinės grėsmės",
        "category.financial_risks.description": "Nepavykę mokėjimai, kortelių problemos, skolos",
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
        "settings.apply_rules": "⚡ Pritaikyti Cleanup Rules po kiekvieno skenavimo",
        "settings.apply_rules_help": "Įjungus, FeeHunt pritaikys išsaugotas valymo taisykles po kiekvieno Gmail skenavimo.",
        "settings.safe_mode": "🔒 Saugus režimas",
        "settings.safe_mode_help": "Rekomenduojama palikti įjungtą, kol FeeHunt yra beta versijoje.",
        "settings.max_dashboard": "Kiek laiškų rodyti Dashboard puslapyje",
        "settings.save": "💾 Išsaugoti nustatymus",
        "settings.saved": "✅ Nustatymai išsaugoti.",
        "settings.save_error": "Nepavyko išsaugoti nustatymų.",
        "settings.technical_info": "🔧 Techninė informacija",
        "gmail.credentials_missing": "Nerastas credentials.json failas: {path}",
        "subscription.opened_unsubscribe": "Atidarytas {service_name} prenumeratos atsisakymo puslapis.",
        "subscription.opened_billing": "Atidarytas {service_name} mokėjimų puslapis.",
        "subscription.opened_search": "Atidaryti {service_name} paieškos rezultatai. Ieškokite Billing arba Subscription nustatymų.",
        "runner.app_missing": "Klaida: Nerastas failas: {path}",
        "runner.check_internal": "Patikrinkite, ar app.py pateko į dist\\FeeHunt\\_internal aplanką.",
        "runner.press_enter": "Paspauskite Enter, kad uždarytumėte...",
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
