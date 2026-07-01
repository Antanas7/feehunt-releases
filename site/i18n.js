const FH_I18N_KEY = "feehunt_site_language";
const FH_LANGUAGES = {
  en: "English",
  lt: "Lietuvių",
  no: "Norsk",
  es: "Español",
  de: "Deutsch",
  fr: "Français",
};

const FH_I18N = {
  en: {
    common: {
      nav: ["Home", "Pricing", "Download", "FAQ", "Privacy", "Terms", "Contact", "Log in"],
      navExtra: { "signup.html": "Start Trial" },
      download: "Download",
      downloadBeta: "Download FeeHunt",
      startTrial: "Start Trial",
      footer: ["Privacy Policy", "Terms of Service", "Contact"],
      menu: "Menu",
    },
    home: {
      title: "FeeHunt | Hidden Subscription Finder and Gmail Inbox Cleaner",
      description: "Find hidden subscriptions, recurring payments, payment control alerts, promotional emails, and phishing signals in Gmail with privacy-first local analysis.",
      heroEyebrow: "Privacy-first subscription control",
      heroHeading: "Find Hidden Subscriptions, Recurring Payments, and Gmail Clutter.",
      heroLead: "FeeHunt helps you detect forgotten subscriptions, recurring payment control emails, promotional inbox clutter, and phishing email signals - privately and locally on your computer.",
      heroButtons: ["Start Free Trial", "Download FeeHunt"],
      heroScanCards: [["Recurring subscription detected", "Renewal and billing signals found"], ["Payment issue detected", "Failed charge or card update email"], ["Suspicious billing email", "Review before clicking any link"], ["Promotional clutter", "Newsletter and shop messages grouped"]],
      principle: "FeeHunt works for you. You stay in control.",
      badges: ["7-Day Free Trial", "Cancel Anytime", "Privacy-First", "Works Locally"],
      badgeDetails: ["Local processing", "On your device", "No data collected"],
      securityStrip: [["Privacy-first design", "Email analysis stays local"], ["Minimal server data", "You stay in control."], ["Calm Gmail protection", "Signals before surprises"]],
      socialProof: "Take control of Gmail and subscriptions with privacy-first local analysis.",
      why: ["Why FeeHunt", "Hidden subscriptions and payment warnings are easy to miss.", "Recurring payments, trial renewals, failed payment warnings, receipts, and unsubscribe links often hide between newsletters and promotions. FeeHunt helps you review what matters, reduce Gmail noise, and stay ahead of unwanted charges.", "FeeHunt reviews signals locally on your computer and asks before Gmail-changing actions."],
      visualToolbar: "FeeHunt Local Dashboard",
      visualPill: "Private on your computer",
      visualRows: [["Subscription access paused", "Payment issue detected from a billing email", "Payment control"], ["Newsletter and promotion cleanup", "Review senders before archive or delete actions", "Inbox cleanup"], ["Cancel subscription", "Open the best available billing or unsubscribe path", "Action ready"]],
      featuresHeading: ["Features", "Built for subscription clarity and inbox control."],
      features: [["Hidden Subscription Detection", "Identify recurring payments, renewals, invoices, trials, and billing messages that are easy to overlook."], ["Payment Control Alerts", "Highlight failed payments, declined cards, overdue invoices, account pauses, and suspended subscription warnings."], ["Unsubscribe and Cancel Tools", "Open the best available unsubscribe, billing, account, or cancellation page without changing Gmail automatically."], ["Gmail Cleanup and Inbox Cleaner", "Review promotional emails, newsletters, shop messages, and inbox clutter with practical cleanup actions."], ["Phishing Email Detection Signals", "Future versions will help flag suspicious billing, login, and phishing-style email patterns in your inbox."]],
      pricingHeading: ["Pricing preview", "Simple monthly plans with a 7-day free trial."],
      plans: [["Basic", "For one Gmail account.", ["1 Gmail account", "1 license key", "7-day free trial", "Cancel anytime"], "Choose Basic"], ["Family", "For up to three Gmail accounts.", ["Up to 3 Gmail accounts", "1 license key", "7-day free trial", "Cancel anytime"], "Choose Family"]],
      pricePeriod: "/month",
      pricingNotice: "No hidden fees. Cancel anytime with one click.",
      faqHeading: ["FAQ", "Questions about hidden subscriptions and Gmail cleanup."],
      faq: [["Can FeeHunt find hidden subscriptions in Gmail?", "FeeHunt looks for subscription emails, renewal notices, invoices, trial reminders, and recurring payment signals so you can review forgotten services before they cost you more."], ["Does FeeHunt work as a Gmail cleanup tool?", "Yes. FeeHunt helps you review newsletters, promotional emails, shop messages, and other inbox clutter. It keeps Gmail-changing actions under your control."], ["Can FeeHunt warn about financial risk emails?", "FeeHunt highlights failed payment messages, overdue invoices, declined card notices, paused subscriptions, and other billing emails that may need attention."], ["Is FeeHunt private?", "FeeHunt is designed for privacy-first local analysis. Gmail review happens on your computer, and FeeHunt asks before actions that archive, delete, or change messages."], ["Does FeeHunt detect phishing emails?", "FeeHunt focuses on subscription and billing signals today. Security-oriented detection for suspicious payment, login, and phishing-style emails is part of the product direction."]],
      start: ["Start now", "Start your free trial and take control of your subscriptions and inbox.", "Start Free Trial", "Download FeeHunt"],
    },
    pricing: {
      title: "Pricing | FeeHunt",
      description: "Simple FeeHunt pricing with Basic and Family plans.",
      hero: ["Pricing", "Simple Pricing for a Cleaner Inbox and Fewer Forgotten Subscriptions.", "Start with a 7-day free trial. Choose the plan that matches how many Gmail accounts you want to connect. Cancel anytime.", "You stay in control: start with a trial, review the plan, and cancel before public billing enforcement begins.", "Start Free Trial", "Upgrade Plan"],
      plans: [["Basic Plan", "Best for individuals who want to review one Gmail account and reduce recurring subscription waste.", ["7-day free trial", "1 Gmail account", "1 license key", "Subscription detection", "Payment control alerts", "Promotional inbox cleanup", "Local processing", "Cancel anytime"], "Start Basic Trial", "Manage / Cancel Plan"], ["Family Plan", "Best for households, couples, and families who want to manage multiple Gmail accounts under one license.", ["7-day free trial", "Up to 3 Gmail accounts", "1 license key", "Subscription detection", "Payment control alerts", "Promotional inbox cleanup", "Local processing", "Cancel anytime"], "Start Family Trial", "Manage / Cancel Plan"]],
      pricePeriod: "/month",
      faqHeading: ["Billing FAQ", "Honest pricing, clear cancellation."],
      faq: [["Is there a free trial?", "Yes. Both Basic and Family plans include a 7-day free trial."], ["When will I be charged?", "After the 7-day trial ends, your selected plan becomes active unless you cancel before the trial ends."], ["Can I cancel anytime?", "Yes. FeeHunt provides a clear subscription management path through Stripe Billing Portal."], ["Are there hidden fees?", "No. FeeHunt uses simple monthly pricing with no hidden fees."], ["Can I change plans later?", "Yes. Plan upgrades and billing self-service are handled through the customer portal."]],
    },
    signup: {
      title: "Start Free Trial | FeeHunt",
      description: "Create your FeeHunt account and start a 7-day free trial. No credit card required.",
      hero: {
        eyebrow: "7-day free trial",
        title: "Get your FeeHunt key.",
        lead: "Enter your email — we will send your FeeHunt key so you can activate the Windows app. No credit card required.",
      },
      form: {
        email: "Gmail or email address",
        plan: "Plan",
        planTrial: "7-day free trial - 1 Gmail account",
        planBasic: "Basic - 1 Gmail account",
        planFamily: "Family - up to 3 Gmail accounts",
        submit: "Send my FeeHunt key",
        note: "No credit card required. FeeHunt never stores Gmail email content on the licensing server.",
      },
      footer: { haveKey: "Already have a key? <a class=\"text-link\" href=\"login.html\">Activate it on the login page</a>." },
    },
    login: {
      title: "Activate FeeHunt | FeeHunt",
      description: "Paste your FeeHunt license key. We will verify it and tell you exactly what to do next.",
      hero: {
        eyebrow: "Activate FeeHunt",
        title: "Paste your FeeHunt key.",
        lead: "FeeHunt is a Windows desktop app. Paste your key below — we will verify it and show you exactly what to do next.",
      },
      form: {
        label: "FeeHunt license key",
        submit: "Verify my key",
        hint: "Key format: FHUNT-XXXX-XXXX-XXXX-XXXX (you received it by email after signup).",
      },
      help: {
        installed: "<strong>Already installed FeeHunt?</strong> Open FeeHunt from the Windows Start menu and paste your key inside the app. To use another key on the same computer, choose <em>Use another license key</em> in FeeHunt. You do not need to download or install the program again.",
        title: "Where can I get stuck?",
        windows: "<strong>FeeHunt is a Windows desktop app.</strong> This website only verifies your key and handles billing. Subscription scans happen in the FeeHunt app on your computer.",
        email: "<strong>Did not get the key by email?</strong> Check spam, promotions and updates folders. Resend it below.",
        expired: "<strong>Trial ended?</strong> Upgrade to Basic or Family on the <a href=\"pricing.html\">Pricing</a> page.",
        devices: "<strong>Device limit reached?</strong> Each plan allows a limited number of devices. Contact <a href=\"mailto:support@feehunt.pro\">support@feehunt.pro</a> to free a slot.",
      },
      resend: {
        kicker: "Forgot your key?",
        title: "Send my key by email",
        label: "Email",
        submit: "Send my key",
      },
      footer: { signup: "New to FeeHunt? <a class=\"text-link\" href=\"signup.html\">Start a free 7-day trial</a>." },
    },
    success: {
      title: "Payment Successful | FeeHunt",
      description: "Your FeeHunt payment was successful.",
      hero: ["Payment successful", "Your FeeHunt plan is being activated.", "Stripe confirmed your payment. FeeHunt will send your license key to the email used during checkout.", "If the email does not arrive in a few minutes, use Log in / Resend key with the same email address.", "Download FeeHunt", "Resend key"],
      cards: [["What happens next", ["Check your email for the FeeHunt license key.", "Download or open FeeHunt on Windows.", "Paste the key in the desktop app.", "Connect Gmail only when you are ready."]], ["Next steps", ["Check the email address used for Stripe payment.", "Download or open the FeeHunt Windows app.", "Paste the license key in the app.", "Connect Gmail only when you are ready."]]],
    },
    account: {
      title: "Manage Subscription | FeeHunt",
      description: "Manage or cancel your FeeHunt subscription.",
      hero: ["Account", "Manage your FeeHunt subscription.", "Paste your FeeHunt license key to securely open Stripe Billing Portal. FeeHunt will never ask for your card details here.", "Cancellation and billing changes are handled by Stripe. Your Gmail data stays on your computer."],
      form: ["FeeHunt license key", "Manage / Cancel Subscription", "Need your key again?", "Resend license key"],
    },
  },
};

FH_I18N.lt = {
    common: {
    nav: ["Pradzia", "Kainodara", "Atsisiusti", "DUK", "Privatumas", "Salygos", "Kontaktai", "Prisijungti"],
    navExtra: { "signup.html": "Pradėti bandymą" },
    download: "Atsisiusti",
    downloadBeta: "Atsisiusti Beta",
    startTrial: "Pradeti bandyma",
    footer: ["Privatumo politika", "Naudojimo salygos", "Kontaktai"],
    menu: "Meniu",
  },
  home: {
    title: "FeeHunt | Raskite pamirstas prenumeratas",
    description: "Raskite pamirstas prenumeratas, taupykite pinigus ir apsaugokite savo pasta su FeeHunt.",
    heroEyebrow: "Privatumu paremta prenumeratu kontrole",
    heroHeading: "Raskite pamirstas prenumeratas, taupykite pinigus ir apsaugokite savo pasta.",
    heroLead: "FeeHunt padeda aptikti prenumeratas, mokejimu kontroles signalus, reklamini triuksma ir galimas sukciavimo gresmes - privaciai jusu kompiuteryje.",
    heroButtons: ["Pradeti nemokama bandyma", "Atsisiusti Beta"],
    heroScanCards: [["Aptikta pasikartojanti prenumerata", "Rasti atnaujinimo ir apmokejimo signalai"], ["Aptikta mokejimo problema", "Nepavykes mokestis arba korteles atnaujinimo laiskas"], ["Itartinas atsiskaitymo laiskas", "Perziurekite pries spausdami nuoroda"], ["Reklaminis triuksmas", "Naujienlaiskiai ir parduotuviu zinutes sugrupuotos"]],
    principle: "FeeHunt dirba jums. Kontrole lieka jusu rankose.",
    badges: ["7 dienu bandymas", "Galima atsaukti bet kada", "Privatumas pirmiausia", "Veikia lokaliai"],
    badgeDetails: ["Vietinis apdorojimas", "Jusu irenginyje", "Duomenys nerenkami"],
    securityStrip: [["Banko lygio saugumas", "Vietinis ir uzsifruotas"], ["Be serveriu. Be sekimo.", "Jus isliekate kontroleje."], ["Rami Gmail apsauga", "Signalai pries netiketumus"]],
    socialProof: "Prisijunkite prie 1 000+ vartotoju, valdanciu Gmail ir finansus.",
    why: ["Kodel FeeHunt", "Prenumeratas lengva pradeti ir lengva pamirsti.", "Mokejimu pranesimai pasimeta tarp naujienlaiskiu, reklamu, kvitu ir iprastu laisku. FeeHunt padeda perziureti tai, kas svarbu.", "FeeHunt analizuoja signalus jusu kompiuteryje ir klausia pries Gmail keiciancius veiksmus."],
    visualToolbar: "FeeHunt vietinis valdymo skydas",
    visualPill: "Privatu jusu kompiuteryje",
    visualRows: [["Prenumeratos prieiga sustabdyta", "Aptikta mokejimo problema", "Mokejimu kontrole"], ["Reklamu ir naujienlaiskiu tvarkymas", "Perziurekite siuntejus pries archyvavima ar trynima", "Pasto tvarkymas"], ["Atsaukti prenumerata", "Atidaryti tinkamiausia atsisakymo ar paskyros kelia", "Veiksmas paruostas"]],
    featuresHeading: ["Funkcijos", "Sukurta prenumeratu aiskumui ir pasto kontrolei."],
    features: [["Prenumeratu aptikimas", "Aptinka pasikartojancius mokejimus, atnaujinimus, saskaitas ir bandymus."], ["Mokejimu kontrole", "Pazymi nepavykusius mokejimus, atmestas korteles ir sustabdytas paskyras."], ["Prenumeratos atsaukimas", "Atidaro tinkamiausia atsisakymo, paskyros ar apmokejimo puslapi."], ["Pasto tvarkymas", "Padeda perziureti reklaminius laiskus, naujienlaiskius ir parduotuviu zinutes."], ["Saugumo skydas", "Ateities versijos pades aptikti sukciavimo rizikas."]],
    pricingHeading: ["Kainu perziura", "Paprasti menesiniai planai su 7 dienu bandymu."],
    plans: [["Basic", "Vienai Gmail paskyrai.", ["1 Gmail paskyra", "1 licencijos raktas", "7 dienu bandymas", "Galima atsaukti bet kada"], "Pasirinkti Basic"], ["Family", "Iki triju Gmail paskyru.", ["Iki 3 Gmail paskyru", "1 licencijos raktas", "7 dienu bandymas", "Galima atsaukti bet kada"], "Pasirinkti Family"]],
    pricingNotice: "Jokiu pasleptu mokesciu. Atsaukti galima bet kada.",
    start: ["Pradekite dabar", "Pradekite bandyma ir susigrazinkite prenumeratu bei pasto kontrole.", "Pradeti nemokama bandyma", "Atsisiusti Beta"],
  },
  pricing: {
    title: "Kainodara | FeeHunt",
    description: "Paprasta FeeHunt kainodara su Basic ir Family planais.",
    hero: ["Kainodara", "Paprasta kaina svaresnei pasto dezutei ir maziau pamirstu prenumeratu.", "Pradekite nuo 7 dienu bandymo. Pasirinkite plana pagal Gmail paskyru skaiciu. Atsaukti galite bet kada.", "Kontrole lieka jums: pradekite nuo bandymo, perziurekite plana ir atsaukite pries mokama laikotarpi.", "Pradeti bandyma", "Atnaujinti plana"],
    plans: [["Basic planas", "Tinka vienam zmogui, norinciam perziureti viena Gmail paskyra.", ["7 dienu bandymas", "1 Gmail paskyra", "1 licencijos raktas", "Prenumeratu aptikimas", "Mokejimu kontrole", "Reklaminio pasto tvarkymas", "Vietinis apdorojimas", "Galima atsaukti bet kada"], "Pradeti Basic bandyma", "Valdyti / atsaukti plana"], ["Family planas", "Tinka seimai ar kelioms Gmail paskyroms su viena licencija.", ["7 dienu bandymas", "Iki 3 Gmail paskyru", "1 licencijos raktas", "Prenumeratu aptikimas", "Mokejimu kontrole", "Reklaminio pasto tvarkymas", "Vietinis apdorojimas", "Galima atsaukti bet kada"], "Pradeti Family bandyma", "Valdyti / atsaukti plana"]],
    faqHeading: ["Atsiskaitymo DUK", "Aiski kaina ir aiskus atsaukimas."],
    faq: [["Ar yra nemokamas bandymas?", "Taip. Basic ir Family planai turi 7 dienu bandyma."], ["Kada busiu apmokestintas?", "Po 7 dienu bandymo pasirinktas planas taps aktyvus, nebent atsauksite pries pabaiga."], ["Ar galiu atsaukti bet kada?", "Taip. Prenumerata valdoma per Stripe Billing Portal."], ["Ar yra pasleptu mokesciu?", "Ne. FeeHunt naudoja paprasta menesine kainodara."], ["Ar galesiu keisti plana?", "Taip. Plano keitimas ir atsiskaitymo savitarna vyksta klientu portale."]],
  },
  signup: {
    title: "Pradėti bandymą | FeeHunt",
    description: "Sukurkite FeeHunt paskyrą ir pradėkite 7 dienų bandymą.",
    hero: {
      eyebrow: "7 dienų nemokamas bandymas",
      title: "Gaukite FeeHunt raktą.",
      lead: "Įveskite el. paštą — atsiųsime jūsų FeeHunt raktą, kad galėtumėte aktyvuoti Windows programą. Kortelės nereikia.",
    },
    form: {
      email: "Gmail arba el. pašto adresas",
      plan: "Planas",
      planTrial: "7 dienų nemokamas bandymas - 1 Gmail paskyra",
      planBasic: "Basic - 1 Gmail paskyra",
      planFamily: "Family - iki 3 Gmail paskyrų",
      submit: "Atsiųsti FeeHunt raktą",
      note: "Kortelės nereikia. FeeHunt licencijų serveryje nesaugo Gmail laiškų turinio.",
    },
    footer: { haveKey: "Jau turite raktą? <a class=\"text-link\" href=\"login.html\">Aktyvuokite jį prisijungimo puslapyje</a>." },
  },
  login: {
    title: "Aktyvuoti FeeHunt | FeeHunt",
    description: "Įklijuokite FeeHunt licencijos raktą. Patikrinsime ir parodysime, ką daryti toliau.",
    hero: {
      eyebrow: "Aktyvuoti FeeHunt",
      title: "Įklijuokite FeeHunt raktą.",
      lead: "FeeHunt yra Windows darbalaukio programa. Įklijuokite raktą žemiau — patikrinsime ar jis galioja ir tiksliai parodysime, ką daryti toliau.",
    },
    form: {
      label: "FeeHunt licencijos raktas",
      submit: "Tikrinti raktą",
      hint: "Rakto formatas: FHUNT-XXXX-XXXX-XXXX-XXXX (gavote jį el. paštu po registracijos).",
    },
    help: {
      installed: "<strong>FeeHunt jau įdiegta?</strong> Atidarykite FeeHunt iš Windows Start meniu ir įklijuokite raktą pačioje programoje. Norėdami tame pačiame kompiuteryje naudoti kitą raktą, FeeHunt programoje pasirinkite <em>Prisijungti su kitu raktu</em>. Programos siųstis ir diegti iš naujo nereikia.",
      title: "Kur galiu užstrigti?",
      windows: "<strong>FeeHunt yra Windows darbalaukio programa.</strong> Ši svetainė tik patikrina raktą ir tvarko mokėjimus. Prenumeratų skenavimas vyksta FeeHunt programoje jūsų kompiuteryje.",
      email: "<strong>Negavote rakto į el. paštą?</strong> Patikrinkite šlamšto, reklamos ir naujienų aplankus. Galite atsiųsti dar kartą žemiau.",
      expired: "<strong>Bandymas pasibaigė?</strong> Atnaujinkite į Basic arba Family <a href=\"pricing.html\">kainodaros puslapyje</a>.",
      devices: "<strong>Pasiektas įrenginių limitas?</strong> Kiekvienas planas leidžia tik tam tikrą įrenginių skaičių. Susisiekite: <a href=\"mailto:support@feehunt.pro\">support@feehunt.pro</a>, atlaisvinsime vietą.",
    },
    resend: {
      kicker: "Pamiršote raktą?",
      title: "Atsiųsti raktą paštu",
      label: "El. paštas",
      submit: "Atsiųsti raktą",
    },
    footer: { signup: "Naujas FeeHunt vartotojas? <a class=\"text-link\" href=\"signup.html\">Pradėkite nemokamą 7 dienų bandymą</a>." },
  },
  success: {
    title: "Mokejimas sekmingas | FeeHunt",
    description: "FeeHunt mokejimas sekmingas.",
    hero: ["Mokejimas sekmingas", "Jusu FeeHunt planas aktyvuojamas.", "Stripe patvirtino mokejima. FeeHunt atsius licencijos rakta i el. pasta, naudota mokejimui.", "Jei laiskas neateina per kelias minutes, naudokite Prisijungti / Siusti rakta dar karta.", "Atsisiusti FeeHunt", "Siusti rakta dar karta"],
    cards: [["Kas toliau", ["Patikrinkite el. pasta del FeeHunt licencijos rakto.", "Atsisiuskite arba atidarykite FeeHunt Windows programoje.", "Iklijuokite rakta programoje.", "Gmail prijunkite tik tada, kai busite pasiruose."]], ["Next steps", ["Check the email used for Stripe payment.", "Download or open FeeHunt for Windows.", "Paste the license key in the app.", "Connect Gmail only when ready."]]],
  },
  account: {
    title: "Valdyti prenumerata | FeeHunt",
    description: "Valdykite arba atsaukite FeeHunt prenumerata.",
    hero: ["Paskyra", "Valdykite FeeHunt prenumerata.", "Iklijuokite FeeHunt licencijos rakta, kad saugiai atidarytumete Stripe Billing Portal. FeeHunt cia nepraso korteles duomenu.", "Atsaukimas ir atsiskaitymo keitimai vyksta per Stripe. Gmail duomenys lieka jusu kompiuteryje."],
    form: ["FeeHunt licencijos raktas", "Valdyti / atsaukti prenumerata", "Reikia rakto dar karta?", "Siusti licencijos rakta dar karta"],
  },
};

const derivedLanguages = {
  no: {
    common: { nav: ["Hjem", "Priser", "Last ned", "FAQ", "Personvern", "Vilkår", "Kontakt", "Logg inn"], navExtra: { "signup.html": "Start prøveperiode" }, download: "Last ned", downloadBeta: "Last ned Beta", startTrial: "Start prøveperiode", footer: ["Personvern", "Vilkår", "Kontakt"], menu: "Meny" },
    terms: ["gratis prøveperiode", "konto", "abonnement", "Administrer / avbryt abonnement", "lisensnøkkel"],
  },
  es: {
    common: { nav: ["Inicio", "Precios", "Descargar", "FAQ", "Privacidad", "Terminos", "Contacto", "Iniciar sesion"], navExtra: { "signup.html": "Iniciar prueba" }, download: "Descargar", downloadBeta: "Descargar Beta", startTrial: "Iniciar prueba", footer: ["Privacidad", "Terminos", "Contacto"], menu: "Menu" },
    terms: ["prueba gratis", "cuenta", "suscripcion", "Gestionar / cancelar suscripcion", "clave de licencia"],
  },
  de: {
    common: { nav: ["Start", "Preise", "Download", "FAQ", "Datenschutz", "Bedingungen", "Kontakt", "Einloggen"], navExtra: { "signup.html": "Test starten" }, download: "Download", downloadBeta: "Beta herunterladen", startTrial: "Test starten", footer: ["Datenschutz", "Bedingungen", "Kontakt"], menu: "Menü" },
    terms: ["kostenlose Testphase", "Konto", "Abonnement", "Abonnement verwalten / kündigen", "Lizenzschlüssel"],
  },
  fr: {
    common: { nav: ["Accueil", "Tarifs", "Telecharger", "FAQ", "Confidentialite", "Conditions", "Contact", "Connexion"], navExtra: { "signup.html": "Démarrer l'essai" }, download: "Telecharger", downloadBeta: "Telecharger Beta", startTrial: "Demarrer l'essai", footer: ["Confidentialite", "Conditions", "Contact"], menu: "Menu" },
    terms: ["essai gratuit", "compte", "abonnement", "Gerer / annuler l'abonnement", "cle de licence"],
  },
};

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function buildDerivedLanguage(code) {
  const base = clone(FH_I18N.en);
  const data = derivedLanguages[code];
  base.common = { ...base.common, ...data.common };
  const trial = data.terms[0];
  const account = data.terms[1];
  const subscription = data.terms[2];
  const manage = data.terms[3];
  const key = data.terms[4];
  base.home.heroButtons[0] = base.common.startTrial;
  base.home.heroButtons[1] = base.common.downloadBeta;
  base.home.pricingHeading[1] = `Simple monthly plans with a 7-day ${trial}.`;
  base.home.plans[0][2][2] = `7-day ${trial}`;
  base.home.plans[1][2][2] = `7-day ${trial}`;
  base.home.start[2] = base.common.startTrial;
  base.home.start[3] = base.common.downloadBeta;
  base.pricing.hero[4] = base.common.startTrial;
  base.pricing.plans[0][3] = base.common.startTrial;
  base.pricing.plans[0][4] = manage;
  base.pricing.plans[1][3] = base.common.startTrial;
  base.pricing.plans[1][4] = manage;
  base.signup.hero.eyebrow = `7-day ${trial}`;
  base.signup.form.email = `Gmail or email ${account}`;
  base.signup.form.submit = `Send my FeeHunt ${key}`;
  base.login.form.label = `FeeHunt ${key}`;
  base.success.hero[4] = base.common.download;
  base.account.hero[0] = "Account";
  base.account.hero[1] = `Manage your FeeHunt ${subscription}.`;
  base.account.form[0] = `FeeHunt ${key}`;
  base.account.form[1] = manage;
  return base;
}

["no", "es", "de", "fr"].forEach((code) => {
  FH_I18N[code] = buildDerivedLanguage(code);
});

const FH_LANGUAGE_OVERRIDES = {
  no: {
    home: {
      title: "FeeHunt | Finn glemte abonnementer",
      description: "Finn glemte abonnementer, spar penger og beskytt innboksen med FeeHunt.",
      heroEyebrow: "Abonnementskontroll med personvern først",
      heroHeading: "Finn glemte abonnementer, spar penger og beskytt innboksen.",
      heroLead: "FeeHunt hjelper deg med å finne abonnementer, betalingskontroll, reklamepost og mulige svindelvarsler - privat og lokalt på datamaskinen.",
      principle: "FeeHunt jobber for deg. Du beholder kontrollen.",
      badges: ["7 dagers prøveperiode", "Avbryt når som helst", "Personvern først", "Kjører lokalt"],
      badgeDetails: ["Lokal behandling", "På enheten din", "Ingen data samlet inn"],
      why: ["Hvorfor FeeHunt", "Abonnementer er lette å starte og lette å glemme.", "Betalingsvarsler forsvinner mellom nyhetsbrev, kampanjer, kvitteringer og vanlige varsler. FeeHunt hjelper deg å se det som betyr noe.", "FeeHunt analyserer signaler lokalt og spør før Gmail-handlinger som endrer e-posten."],
      pricingHeading: ["Prisoversikt", "Enkle månedsplaner med 7 dagers prøveperiode."],
      pricingNotice: "Ingen skjulte gebyrer. Avbryt når som helst.",
    },
    pricing: {
      title: "Priser | FeeHunt",
      description: "Enkle FeeHunt-priser med Basic- og Family-plan.",
      hero: ["Priser", "Enkle priser for en ryddigere innboks og færre glemte abonnementer.", "Start med en 7 dagers prøveperiode. Velg planen som passer antall Gmail-kontoer. Avbryt når som helst.", "Du beholder kontrollen: start med prøveperiode, se planen og avbryt før betalt periode starter.", "Start prøveperiode", "Oppgrader plan"],
      plans: [["Basic-plan", "For én person som vil gå gjennom én Gmail-konto.", ["7 dagers prøveperiode", "1 Gmail-konto", "1 lisensnøkkel", "Abonnementssøk", "Betalingskontroll", "Opprydding i reklamepost", "Lokal behandling", "Avbryt når som helst"], "Start Basic-prøve", "Administrer / avbryt plan"], ["Family-plan", "For familier eller flere Gmail-kontoer med én lisens.", ["7 dagers prøveperiode", "Opptil 3 Gmail-kontoer", "1 lisensnøkkel", "Abonnementssøk", "Betalingskontroll", "Opprydding i reklamepost", "Lokal behandling", "Avbryt når som helst"], "Start Family-prøve", "Administrer / avbryt plan"]],
      faqHeading: ["Faktura-FAQ", "Tydelige priser og enkel avbestilling."],
      faq: [["Finnes det gratis prøveperiode?", "Ja. Basic og Family inkluderer 7 dagers prøveperiode."], ["Når blir jeg belastet?", "Etter prøveperioden blir valgt plan aktiv med mindre du avbryter før den slutter."], ["Kan jeg avbryte når som helst?", "Ja. Abonnementet kan administreres via Stripe Billing Portal."], ["Finnes det skjulte gebyrer?", "Nei. FeeHunt bruker enkel månedspris."], ["Kan jeg endre plan senere?", "Ja. Planendringer og fakturaadministrasjon håndteres i kundeportalen."]],
    },
    signup: {
      title: "Start prøveperiode | FeeHunt",
      description: "Opprett FeeHunt-konto og start 7 dagers prøveperiode.",
      hero: { eyebrow: "7 dagers prøveperiode", title: "Få FeeHunt-nøkkelen din.", lead: "Skriv inn e-posten — vi sender FeeHunt-nøkkelen så du kan aktivere Windows-appen. Ingen kort kreves." },
      form: { email: "Gmail- eller e-postadresse", plan: "Plan", planTrial: "7 dagers prøveperiode - 1 Gmail-konto", planBasic: "Basic - 1 Gmail-konto", planFamily: "Family - opptil 3 Gmail-kontoer", submit: "Send FeeHunt-nøkkelen", note: "Ingen kort kreves. FeeHunt lagrer ikke Gmail-innhold på lisensserveren." },
      footer: { haveKey: "Har du allerede en nøkkel? <a class=\"text-link\" href=\"login.html\">Aktiver den på innloggingssiden</a>." },
    },
    success: {
      title: "Betaling vellykket | FeeHunt",
      description: "FeeHunt-betalingen var vellykket.",
      hero: ["Betaling vellykket", "FeeHunt-planen din aktiveres.", "Stripe bekreftet betalingen. FeeHunt sender lisensnøkkelen til e-posten som ble brukt i checkout.", "Hvis e-posten ikke kommer innen få minutter, bruk Logg inn / Send nøkkel på nytt med samme e-postadresse.", "Last ned FeeHunt", "Send nøkkel på nytt"],
      cards: [["Hva skjer videre", ["Sjekk e-posten for FeeHunt-lisensnøkkelen.", "Last ned eller åpne FeeHunt på Windows.", "Lim inn nøkkelen i skrivebordsappen.", "Koble til Gmail bare når du er klar."]], ["Neste steg", ["Sjekk e-posten som ble brukt for Stripe-betalingen.", "Åpne FeeHunt for Windows.", "Lim inn lisensnøkkelen i appen.", "Koble til Gmail når du er klar."]]],
    },
    account: {
      title: "Administrer abonnement | FeeHunt",
      description: "Administrer eller avbryt FeeHunt-abonnementet.",
      hero: ["Konto", "Administrer FeeHunt-abonnementet.", "Lim inn FeeHunt-lisensnøkkelen for å åpne Stripe Billing Portal trygt. FeeHunt ber aldri om kortdetaljer her.", "Avbestilling og fakturaendringer håndteres av Stripe. Gmail-dataene dine blir på datamaskinen."],
      form: ["FeeHunt-lisensnøkkel", "Administrer / avbryt abonnement", "Trenger du nøkkelen igjen?", "Send lisensnøkkel på nytt"],
    },
  },
  es: {
    home: {
      title: "FeeHunt | Encuentra suscripciones olvidadas",
      description: "Encuentra suscripciones olvidadas, ahorra dinero y protege tu bandeja de entrada con FeeHunt.",
      heroEyebrow: "Control de suscripciones con privacidad",
      heroHeading: "Encuentra suscripciones olvidadas, ahorra dinero y protege tu bandeja de entrada.",
      heroLead: "FeeHunt te ayuda a detectar suscripciones, control de pagos, correos promocionales y posibles amenazas de phishing de forma privada y local.",
      principle: "FeeHunt trabaja para ti. Tú mantienes el control.",
      badges: ["Prueba de 7 días", "Cancela cuando quieras", "Privacidad primero", "Funciona localmente"],
      badgeDetails: ["Procesamiento local", "En tu dispositivo", "No se recopilan datos"],
      why: ["Por qué FeeHunt", "Las suscripciones son fáciles de iniciar y fáciles de olvidar.", "Los avisos de pago se pierden entre boletines, promociones, recibos y notificaciones. FeeHunt te ayuda a revisar lo importante.", "FeeHunt analiza señales en tu ordenador y pide confirmación antes de acciones que cambian Gmail."],
      pricingHeading: ["Vista de precios", "Planes mensuales simples con prueba de 7 días."],
      pricingNotice: "Sin cargos ocultos. Cancela cuando quieras.",
    },
    pricing: {
      title: "Precios | FeeHunt",
      description: "Precios simples de FeeHunt con planes Basic y Family.",
      hero: ["Precios", "Precios simples para una bandeja más limpia y menos suscripciones olvidadas.", "Empieza con una prueba de 7 días. Elige el plan según cuántas cuentas Gmail quieres conectar. Cancela cuando quieras.", "Tú mantienes el control: empieza con una prueba, revisa el plan y cancela antes del periodo de pago.", "Iniciar prueba", "Mejorar plan"],
      plans: [["Plan Basic", "Para una persona que quiere revisar una cuenta Gmail.", ["Prueba de 7 días", "1 cuenta Gmail", "1 clave de licencia", "Detección de suscripciones", "Control de pagos", "Limpieza de correos promocionales", "Procesamiento local", "Cancela cuando quieras"], "Iniciar Basic", "Gestionar / cancelar plan"], ["Plan Family", "Para familias o varias cuentas Gmail con una licencia.", ["Prueba de 7 días", "Hasta 3 cuentas Gmail", "1 clave de licencia", "Detección de suscripciones", "Control de pagos", "Limpieza de correos promocionales", "Procesamiento local", "Cancela cuando quieras"], "Iniciar Family", "Gestionar / cancelar plan"]],
      faqHeading: ["FAQ de facturación", "Precio claro y cancelación sencilla."],
      faq: [["¿Hay prueba gratis?", "Sí. Basic y Family incluyen una prueba de 7 días."], ["¿Cuándo se cobra?", "Después de la prueba de 7 días, tu plan se activa salvo que canceles antes."], ["¿Puedo cancelar cuando quiera?", "Sí. La suscripción se gestiona con Stripe Billing Portal."], ["¿Hay cargos ocultos?", "No. FeeHunt usa precios mensuales simples."], ["¿Puedo cambiar de plan?", "Sí. Los cambios de plan y facturación se gestionan en el portal de cliente."]],
    },
    signup: {
      title: "Iniciar prueba | FeeHunt",
      description: "Crea tu cuenta FeeHunt e inicia una prueba de 7 días.",
      hero: { eyebrow: "Prueba de 7 días", title: "Obtén tu clave FeeHunt.", lead: "Introduce tu email — te enviaremos la clave FeeHunt para activar la app de Windows. No se requiere tarjeta." },
      form: { email: "Dirección Gmail o email", plan: "Plan", planTrial: "Prueba de 7 días - 1 cuenta Gmail", planBasic: "Basic - 1 cuenta Gmail", planFamily: "Family - hasta 3 cuentas Gmail", submit: "Enviar mi clave FeeHunt", note: "No se requiere tarjeta. FeeHunt no guarda contenido de Gmail en el servidor de licencias." },
      footer: { haveKey: "¿Ya tienes una clave? <a class=\"text-link\" href=\"login.html\">Actívala en la página de inicio de sesión</a>." },
    },
    success: {
      title: "Pago correcto | FeeHunt",
      description: "Tu pago de FeeHunt se completó correctamente.",
      hero: ["Pago correcto", "Tu plan FeeHunt se está activando.", "Stripe confirmó el pago. FeeHunt enviará la clave de licencia al email usado en checkout.", "Si el email no llega en unos minutos, usa Iniciar sesión / Reenviar clave con el mismo email.", "Descargar FeeHunt", "Reenviar clave"],
      cards: [["Qué pasa después", ["Revisa tu email para encontrar la clave de licencia FeeHunt.", "Descarga o abre FeeHunt en Windows.", "Pega la clave en la app de escritorio.", "Conecta Gmail solo cuando estés listo."]], ["Siguientes pasos", ["Revisa el email usado para el pago de Stripe.", "Abre FeeHunt para Windows.", "Pega la clave de licencia en la app.", "Conecta Gmail cuando quieras."]]],
    },
    account: {
      title: "Gestionar suscripción | FeeHunt",
      description: "Gestiona o cancela tu suscripción FeeHunt.",
      hero: ["Cuenta", "Gestiona tu suscripción FeeHunt.", "Pega tu clave de licencia FeeHunt para abrir Stripe Billing Portal de forma segura. FeeHunt nunca pide los datos de tu tarjeta aquí.", "La cancelación y los cambios de facturación se gestionan con Stripe. Tus datos de Gmail permanecen en tu ordenador."],
      form: ["Clave de licencia FeeHunt", "Gestionar / cancelar suscripción", "¿Necesitas la clave otra vez?", "Reenviar clave de licencia"],
    },
  },
  de: {
    home: {
      title: "FeeHunt | Vergessene Abonnements finden",
      description: "Finde vergessene Abonnements, spare Geld und schütze deinen Posteingang mit FeeHunt.",
      heroEyebrow: "Abokontrolle mit Datenschutz zuerst",
      heroHeading: "Finde vergessene Abonnements, spare Geld und schütze deinen Posteingang.",
      heroLead: "FeeHunt hilft dir, Abonnements, Zahlungskontrolle, Werbe-E-Mails und mögliche Phishing-Gefahren privat und lokal zu erkennen.",
      principle: "FeeHunt arbeitet für dich. Du behältst die Kontrolle.",
      badges: ["7 Tage Testphase", "Jederzeit kündbar", "Datenschutz zuerst", "Läuft lokal"],
      badgeDetails: ["Lokale Verarbeitung", "Auf deinem Gerät", "Keine Datenerfassung"],
      why: ["Warum FeeHunt", "Abonnements sind leicht zu starten und leicht zu vergessen.", "Zahlungshinweise verschwinden zwischen Newslettern, Werbung, Belegen und Benachrichtigungen. FeeHunt hilft, Wichtiges zu prüfen.", "FeeHunt analysiert Signale lokal und fragt vor Gmail-Änderungen nach."],
      pricingHeading: ["Preisübersicht", "Einfache Monatspläne mit 7 Tagen Testphase."],
      pricingNotice: "Keine versteckten Gebühren. Jederzeit kündbar.",
    },
    pricing: {
      title: "Preise | FeeHunt",
      description: "Einfache FeeHunt-Preise mit Basic- und Family-Plan.",
      hero: ["Preise", "Einfache Preise für einen saubereren Posteingang und weniger vergessene Abonnements.", "Starte mit 7 Tagen Testphase. Wähle den Plan passend zur Anzahl deiner Gmail-Konten. Jederzeit kündbar.", "Du behältst die Kontrolle: starte mit einer Testphase, prüfe den Plan und kündige vor dem kostenpflichtigen Zeitraum.", "Testphase starten", "Plan upgraden"],
      plans: [["Basic-Plan", "Für eine Person, die ein Gmail-Konto prüfen möchte.", ["7 Tage Testphase", "1 Gmail-Konto", "1 Lizenzschlüssel", "Abo-Erkennung", "Zahlungskontrolle", "Aufräumen von Werbe-E-Mails", "Lokale Verarbeitung", "Jederzeit kündbar"], "Basic testen", "Plan verwalten / kündigen"], ["Family-Plan", "Für Familien oder mehrere Gmail-Konten mit einer Lizenz.", ["7 Tage Testphase", "Bis zu 3 Gmail-Konten", "1 Lizenzschlüssel", "Abo-Erkennung", "Zahlungskontrolle", "Aufräumen von Werbe-E-Mails", "Lokale Verarbeitung", "Jederzeit kündbar"], "Family testen", "Plan verwalten / kündigen"]],
      faqHeading: ["Abrechnungs-FAQ", "Klare Preise und einfache Kündigung."],
      faq: [["Gibt es eine kostenlose Testphase?", "Ja. Basic und Family enthalten 7 Tage Testphase."], ["Wann wird abgerechnet?", "Nach der Testphase wird dein gewählter Plan aktiv, sofern du nicht vorher kündigst."], ["Kann ich jederzeit kündigen?", "Ja. Das Abonnement wird über das Stripe Billing Portal verwaltet."], ["Gibt es versteckte Gebühren?", "Nein. FeeHunt nutzt einfache monatliche Preise."], ["Kann ich später den Plan wechseln?", "Ja. Planwechsel und Abrechnung werden im Kundenportal verwaltet."]],
    },
    signup: {
      title: "Testphase starten | FeeHunt",
      description: "Erstelle dein FeeHunt-Konto und starte 7 Tage Testphase.",
      hero: { eyebrow: "7 Tage Testphase", title: "Erhalte deinen FeeHunt-Schlüssel.", lead: "Gib deine E-Mail ein — wir senden dir den FeeHunt-Schlüssel, damit du die Windows-App aktivieren kannst. Keine Karte erforderlich." },
      form: { email: "Gmail- oder E-Mail-Adresse", plan: "Plan", planTrial: "7 Tage Testphase - 1 Gmail-Konto", planBasic: "Basic - 1 Gmail-Konto", planFamily: "Family - bis zu 3 Gmail-Konten", submit: "FeeHunt-Schlüssel senden", note: "Keine Karte erforderlich. FeeHunt speichert keine Gmail-Inhalte auf dem Lizenzserver." },
      footer: { haveKey: "Du hast bereits einen Schlüssel? <a class=\"text-link\" href=\"login.html\">Aktiviere ihn auf der Login-Seite</a>." },
    },
    success: {
      title: "Zahlung erfolgreich | FeeHunt",
      description: "Deine FeeHunt-Zahlung war erfolgreich.",
      hero: ["Zahlung erfolgreich", "Dein FeeHunt-Plan wird aktiviert.", "Stripe hat die Zahlung bestätigt. FeeHunt sendet den Lizenzschlüssel an die beim Checkout verwendete E-Mail.", "Wenn die E-Mail nicht in wenigen Minuten ankommt, nutze Einloggen / Schlüssel erneut senden mit derselben E-Mail.", "FeeHunt herunterladen", "Schlüssel erneut senden"],
      cards: [["Was passiert als Nächstes", ["Prüfe deine E-Mail auf den FeeHunt-Lizenzschlüssel.", "Lade FeeHunt herunter oder öffne es unter Windows.", "Füge den Schlüssel in der Desktop-App ein.", "Verbinde Gmail erst, wenn du bereit bist."]], ["Nächste Schritte", ["Prüfe die für Stripe verwendete E-Mail.", "Öffne FeeHunt für Windows.", "Füge den Lizenzschlüssel in der App ein.", "Verbinde Gmail, wenn du bereit bist."]]],
    },
    account: {
      title: "Abonnement verwalten | FeeHunt",
      description: "Verwalte oder kündige dein FeeHunt-Abonnement.",
      hero: ["Konto", "Verwalte dein FeeHunt-Abonnement.", "Füge deinen FeeHunt-Lizenzschlüssel ein, um das Stripe Billing Portal sicher zu öffnen. FeeHunt fragt hier nie nach Kartendaten.", "Kündigung und Abrechnungsänderungen werden von Stripe verarbeitet. Deine Gmail-Daten bleiben auf deinem Computer."],
      form: ["FeeHunt-Lizenzschlüssel", "Abonnement verwalten / kündigen", "Brauchst du deinen Schlüssel erneut?", "Lizenzschlüssel erneut senden"],
    },
  },
  fr: {
    home: {
      title: "FeeHunt | Retrouvez les abonnements oubliés",
      description: "Retrouvez les abonnements oubliés, économisez et protégez votre boîte mail avec FeeHunt.",
      heroEyebrow: "Contrôle des abonnements axé sur la confidentialité",
      heroHeading: "Retrouvez les abonnements oubliés, économisez et protégez votre boîte mail.",
      heroLead: "FeeHunt vous aide à détecter les abonnements, le contrôle des paiements, les emails promotionnels et les menaces de phishing possibles, localement et en privé.",
      principle: "FeeHunt travaille pour vous. Vous gardez le contrôle.",
      badges: ["Essai de 7 jours", "Annulation à tout moment", "Confidentialité d'abord", "Fonctionne localement"],
      badgeDetails: ["Traitement local", "Sur votre appareil", "Aucune collecte de données"],
      why: ["Pourquoi FeeHunt", "Les abonnements sont faciles à lancer et faciles à oublier.", "Les alertes de paiement se perdent entre newsletters, promotions, reçus et notifications. FeeHunt vous aide à voir l'important.", "FeeHunt analyse les signaux localement et demande confirmation avant toute action qui modifie Gmail."],
      pricingHeading: ["Aperçu des tarifs", "Plans mensuels simples avec essai de 7 jours."],
      pricingNotice: "Aucuns frais cachés. Annulation à tout moment.",
    },
    pricing: {
      title: "Tarifs | FeeHunt",
      description: "Tarifs FeeHunt simples avec les plans Basic et Family.",
      hero: ["Tarifs", "Des tarifs simples pour une boîte mail plus claire et moins d'abonnements oubliés.", "Commencez avec un essai de 7 jours. Choisissez le plan adapté au nombre de comptes Gmail. Annulez à tout moment.", "Vous gardez le contrôle : commencez par un essai, vérifiez le plan et annulez avant la période payante.", "Démarrer l'essai", "Changer de plan"],
      plans: [["Plan Basic", "Pour une personne qui veut vérifier un compte Gmail.", ["Essai de 7 jours", "1 compte Gmail", "1 clé de licence", "Détection des abonnements", "Contrôle des paiements", "Nettoyage des emails promotionnels", "Traitement local", "Annulation à tout moment"], "Essayer Basic", "Gérer / annuler le plan"], ["Plan Family", "Pour les familles ou plusieurs comptes Gmail avec une seule licence.", ["Essai de 7 jours", "Jusqu'à 3 comptes Gmail", "1 clé de licence", "Détection des abonnements", "Contrôle des paiements", "Nettoyage des emails promotionnels", "Traitement local", "Annulation à tout moment"], "Essayer Family", "Gérer / annuler le plan"]],
      faqHeading: ["FAQ facturation", "Prix clairs et annulation simple."],
      faq: [["Y a-t-il un essai gratuit ?", "Oui. Basic et Family incluent un essai de 7 jours."], ["Quand serai-je facturé ?", "Après l'essai, le plan choisi devient actif sauf si vous annulez avant la fin."], ["Puis-je annuler à tout moment ?", "Oui. L'abonnement se gère via Stripe Billing Portal."], ["Y a-t-il des frais cachés ?", "Non. FeeHunt utilise une tarification mensuelle simple."], ["Puis-je changer de plan plus tard ?", "Oui. Les changements de plan et la facturation sont gérés dans le portail client."]],
    },
    signup: {
      title: "Démarrer l'essai | FeeHunt",
      description: "Créez votre compte FeeHunt et démarrez un essai de 7 jours.",
      hero: { eyebrow: "Essai de 7 jours", title: "Obtenez votre clé FeeHunt.", lead: "Entrez votre email — nous envoyons votre clé FeeHunt pour activer l'application Windows. Aucune carte requise." },
      form: { email: "Adresse Gmail ou email", plan: "Plan", planTrial: "Essai de 7 jours - 1 compte Gmail", planBasic: "Basic - 1 compte Gmail", planFamily: "Family - jusqu'à 3 comptes Gmail", submit: "Envoyer ma clé FeeHunt", note: "Aucune carte requise. FeeHunt ne stocke pas le contenu Gmail sur le serveur de licences." },
      footer: { haveKey: "Vous avez déjà une clé ? <a class=\"text-link\" href=\"login.html\">Activez-la sur la page de connexion</a>." },
    },
    success: {
      title: "Paiement réussi | FeeHunt",
      description: "Votre paiement FeeHunt a réussi.",
      hero: ["Paiement réussi", "Votre plan FeeHunt est en cours d'activation.", "Stripe a confirmé le paiement. FeeHunt enverra la clé de licence à l'email utilisé lors du paiement.", "Si l'email n'arrive pas en quelques minutes, utilisez Connexion / Renvoyer la clé avec la même adresse.", "Télécharger FeeHunt", "Renvoyer la clé"],
      cards: [["Ce qui se passe ensuite", ["Vérifiez votre email pour la clé de licence FeeHunt.", "Téléchargez ou ouvrez FeeHunt sur Windows.", "Collez la clé dans l'application de bureau.", "Connectez Gmail seulement quand vous êtes prêt."]], ["Étapes suivantes", ["Vérifiez l'email utilisé pour le paiement Stripe.", "Ouvrez FeeHunt pour Windows.", "Collez la clé de licence dans l'application.", "Connectez Gmail quand vous êtes prêt."]]],
    },
    account: {
      title: "Gérer l'abonnement | FeeHunt",
      description: "Gérez ou annulez votre abonnement FeeHunt.",
      hero: ["Compte", "Gérez votre abonnement FeeHunt.", "Collez votre clé de licence FeeHunt pour ouvrir Stripe Billing Portal en toute sécurité. FeeHunt ne demande jamais vos données de carte ici.", "L'annulation et les changements de facturation sont gérés par Stripe. Vos données Gmail restent sur votre ordinateur."],
      form: ["Clé de licence FeeHunt", "Gérer / annuler l'abonnement", "Besoin de votre clé à nouveau ?", "Renvoyer la clé de licence"],
    },
  },
};

function mergeTranslation(target, source) {
  Object.entries(source).forEach(([key, override]) => {
    if (override && typeof override === "object" && !Array.isArray(override)) {
      target[key] = target[key] || {};
      mergeTranslation(target[key], override);
    } else {
      target[key] = override;
    }
  });
}

Object.entries(FH_LANGUAGE_OVERRIDES).forEach(([code, overrides]) => {
  mergeTranslation(FH_I18N[code], overrides);
});

const FH_STATIC_PAGE_TRANSLATIONS = {
  en: {
    download: {
      title: "Download FeeHunt | FeeHunt",
      description: "Download FeeHunt for Windows. We walk you through the install step by step, including the Windows security warning you will see.",
      hero: {
        eyebrow: "Windows app · 5-minute setup",
        title: "Download FeeHunt and we'll walk you through every step.",
        lead: "FeeHunt is a small Windows program. You'll see one Windows warning and one Google warning during setup — both are normal. We tell you what to click each time. Honestly, it's a 5-minute job.",
        button: "⬇ Download FeeHunt for Windows",
        meta: "Free 7-day trial · No credit card · Works on Windows 10 and 11",
      },
      walk: {
        title: "What happens after you click download",
        s1: { title: "A file will start downloading", body: "Your browser will save FeeHunt-Setup-v1.12.7.exe to your Downloads folder. It's a small file (~80 MB) and takes about 30 seconds on most connections." },
        s2: { title: "Double-click the downloaded file", body: "Open your Downloads folder and double-click FeeHunt-Setup-v1.12.7.exe." },
        s3: {
          title: "Windows will show a blue warning — this is normal",
          body: "What you'll see: A blue box titled \"Windows protected your PC\" with a small \"Don't run\" button. Windows may show this for a new or unsigned installer while it has limited download reputation. FeeHunt code signing is being prepared.",
          action: "<strong>What to click:</strong> Click the small <em>\"More info\"</em> link on the LEFT of the box. A new <em>\"Run anyway\"</em> button will appear. Click that.",
        },
        s4: { title: "Click through the installer (Next, Next, Install)", body: "A standard Windows installer appears. Three short screens, all default settings are fine: click Next → Next → Install → Finish. FeeHunt will open automatically." },
        s5: { title: "Paste your license key", body: "FeeHunt opens in your browser at http://localhost:8501 — this is FeeHunt running locally on your computer, not a website. Paste the FHUNT-XXXX-XXXX-XXXX-XXXX key from your email, click Activate." },
        s6: {
          title: "Click \"Connect Gmail\"",
          body: "What you'll see: Google opens its sign-in and permission flow. Pick the Gmail account you want FeeHunt to review, read the requested permissions, and continue only if you are comfortable granting them.",
          action: "<strong>What to click:</strong> Follow Google's sign-in flow and approve the Gmail permissions FeeHunt requests. You can revoke access later in your Google account settings.",
          trust: "🔒 FeeHunt never sees or stores your Gmail password. Google's official OAuth flow grants FeeHunt a token that you can revoke at any moment in your Google account settings.",
        },
        s7: { title: "Done! Click \"Scan Gmail\" and see what FeeHunt finds.", body: "Your first scan takes about 1–2 minutes and reads the most recent 200 emails. Nothing is changed in Gmail until you confirm. From now on, FeeHunt runs from your Start menu like any other app." },
        help: "Stuck at any step? Email <a href=\"mailto:support@feehunt.pro\">support@feehunt.pro</a> — we usually reply within a day.",
      },
      trust: {
        title: "Why FeeHunt is safe",
        local: "<strong>Everything runs on your computer.</strong> Scan results, settings, and tokens are stored in your Windows user profile. Nothing about your email content is sent to FeeHunt's servers.",
        password: "<strong>FeeHunt never sees your Gmail password.</strong> Google's OAuth grants a scoped token; you approve through Google's own sign-in window.",
        revoke: "<strong>You can revoke access any time.</strong> Open <a href=\"https://myaccount.google.com/permissions\" target=\"_blank\" rel=\"noopener\">Google account permissions</a> and remove FeeHunt with one click.",
        read: "<strong>You stay in control.</strong> Gmail actions like archive, delete, mark as spam, and mark as important affect your real Gmail account — review before acting.",
      },
    },
    faqPage: {
      title: "FAQ | FeeHunt",
      description: "Frequently asked questions about FeeHunt.",
      hero: ["FAQ", "Questions before you try FeeHunt?", "Clear answers about privacy, Gmail access, trials, cancellation, and account limits."],
      items: [["How does FeeHunt work?", "FeeHunt connects to Gmail through Google OAuth and scans recent emails for subscriptions, renewals, invoices, failed payments, promotions, newsletters, shop emails, and future phishing-risk patterns."], ["Is my email private?", "FeeHunt is designed as a privacy-first local desktop app. Email analysis happens locally on your computer. FeeHunt does not sell your data."], ["Can I cancel anytime?", "Yes. FeeHunt is built around clear cancellation and subscription management."], ["Which Gmail accounts are supported?", "FeeHunt is designed for Gmail accounts connected through Google's OAuth authorization flow. During beta, the product focuses on Gmail and Windows."], ["What happens after the free trial?", "After the 7-day free trial, the selected paid plan becomes active unless you cancel before the trial ends."], ["How many Gmail accounts can I connect?", "The Basic plan supports 1 Gmail account. The Family plan supports up to 3 Gmail accounts."]],
    },
    contact: {
      title: "Contact | FeeHunt",
      description: "Contact FeeHunt.",
      hero: ["Contact", "Contact FeeHunt.", "Have a question, bug report, product idea, or business inquiry? We would like to hear from you."],
      left: ["General inquiries", "Email: ", "For beta feedback, please use the Feedback page so we can collect structured reports and improve the product faster.", "Send Feedback"],
      right: ["What to include", ["Your operating system", "Whether you are using the beta or public version", "A short description of the issue or question", "Screenshots only if they do not contain private email content"], "Please do not send private email content, OAuth tokens, license keys, or sensitive account information."],
    },
    feedback: {
      title: "Feedback | FeeHunt",
      description: "Send FeeHunt beta feedback.",
      hero: ["Feedback", "Help shape FeeHunt.", "Beta feedback helps us improve detection quality, cancellation flows, onboarding, and privacy-first product design."],
      left: ["What to send", ["Bug reports", "Confusing setup steps", "False subscription detections", "Feature ideas", "Cancellation success stories"]],
      right: ["Contact", "Email feedback to ", "Please avoid sending private email content, OAuth tokens, license keys, or sensitive account information.", "Send Feedback"],
    },
    privacy: {
      title: "Privacy Policy | FeeHunt",
      description: "FeeHunt Privacy Policy.",
      hero: ["Privacy Policy", "Privacy-first by design.", "FeeHunt is designed around local processing, minimal data collection, and user control."],
      intro: ["Last updated:", " 2026-07-01", "This Privacy Policy is effective as of July 1, 2026."],
      sections: [["Overview", ["FeeHunt is designed as a privacy-first desktop application that helps users identify subscriptions, payment-control emails, promotional clutter, and future phishing-risk patterns."]], ["Local Processing", ["FeeHunt processes Gmail scan results locally on the user's computer. Email analysis, scan results, settings, and license metadata are designed to remain on the user's device unless a future feature clearly states otherwise."]], ["Gmail Access", ["FeeHunt uses OAuth-based Gmail access. Users authorize access through Google. FeeHunt does not ask for or store Gmail passwords. OAuth tokens may be stored locally so FeeHunt can connect to Gmail after authorization."]], ["Google User Data", ["FeeHunt accesses the following Google user data through Gmail OAuth:", "Gmail message metadata and content (read-only) to identify subscription-related emails, billing notices, and promotional clutter.", "FeeHunt requests only the minimum OAuth scopes necessary: Gmail read access (https://www.googleapis.com/auth/gmail.readonly) and Gmail modify access for user-initiated actions (https://www.googleapis.com/auth/gmail.modify)."], "lead-list"], ["Data Sharing and Disclosure", ["FeeHunt does not share, transfer, sell, or disclose Google user data to any third parties. All Gmail analysis is performed locally on the user's device. No email content or metadata is transmitted to FeeHunt servers."]], ["Data Protection and Security", ["FeeHunt protects sensitive Google user data (your Gmail messages and metadata) using the following security mechanisms:", "Encryption in transit: all communication with the Gmail API uses encrypted HTTPS/TLS connections.", "Encryption at rest: your Gmail OAuth token is stored on your device encrypted at rest using the operating system's native data-protection facility (Windows Data Protection API, DPAPI), tied to your Windows user account so other users or applications on the device cannot read it.", "Local-only processing: all Gmail analysis runs locally on your device; email content and metadata are never transmitted to, stored on, or processed by FeeHunt servers or any third party.", "Least-privilege access: FeeHunt requests only the minimum OAuth scopes required and accesses your Gmail data solely to perform actions you initiate (scanning and cleanup actions you explicitly approve).", "Retention and deletion: scan results and settings stay on your device and can be deleted by you at any time; you can revoke FeeHunt's access to your Gmail at any time through your Google Account, after which the stored token can no longer be used.", "Limited Use: FeeHunt's use of information received from Google APIs adheres to the Google API Services User Data Policy (https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use requirements."], "lead-list"], ["Data Stored Locally", ["OAuth authorization token", "Scan results", "User settings", "Cleanup preferences", "Local license metadata"], "list"], ["Minimal Data Collection", ["FeeHunt should collect only the minimum data required to operate, support licensing, improve reliability, and provide customer support."]], ["No Selling User Data", ["FeeHunt does not sell user data and should not sell, rent, or trade Gmail data, scan results, or personal account information."]], ["Future Payment and Licensing", ["Public launch licensing and payment features may require account, billing, and license data. Payment processing should be handled by a trusted payment provider such as Stripe. FeeHunt should not store raw payment card data."]], ["User Control", ["Revoke Gmail access through your Google account", "Delete local FeeHunt files from your computer", "Cancel paid subscriptions through a clear self-service flow"], "list"], ["Contact", ["For privacy questions, contact "]]],
    },
    terms: {
      title: "Terms of Service | FeeHunt",
      description: "FeeHunt Terms of Service.",
      hero: ["Terms of Service", "FeeHunt usage terms.", "These terms describe product use, beta limitations, billing principles, cancellation, and user responsibility."],
      intro: ["Last updated:", " 2026-07-01", "These Terms of Service are effective as of June 16, 2026."],
      sections: [["Acceptance of Terms", ["By using FeeHunt, you agree to these Terms of Service. If you do not agree, do not use the product."]], ["Product Description", ["FeeHunt is a desktop application that helps users review Gmail for subscriptions, payment-control messages, promotional clutter, and future security-related email patterns.", "FeeHunt provides detection and organization tools. It does not guarantee that every subscription, payment issue, promotional email, phishing attempt, or scam will be detected."]], ["Beta Software", ["FeeHunt beta versions may contain bugs, incomplete features, placeholder licensing flows, and changing behavior. Users should review results carefully before taking Gmail actions."]], ["User Responsibility", ["Review detected emails before taking action", "Understand that archive, delete, spam, and other Gmail actions affect real email", "Maintain access to your Gmail account", "Keep OAuth files, tokens, license keys, and local data secure"]], ["Gmail Authorization", ["FeeHunt uses Google OAuth for Gmail access. Users can revoke access through their Google account settings."]], ["Subscriptions and Billing", ["Basic: €5.90/month", "Family: €9.90/month", "7-day free trial", "Cancel anytime", "Public billing enforcement should only begin once checkout, customer portal, and cancellation flows are available."]], ["Cancellation", ["Users should be able to cancel paid subscriptions through a clear self-service cancellation flow. Access remains active until the end of the paid billing period unless stated otherwise."]], ["No Misuse", ["Users may not use FeeHunt to violate laws, abuse Gmail, interfere with service operations, reverse engineer protected systems, or attempt unauthorized access to accounts or infrastructure."]], ["Limitation of Liability", ["FeeHunt is provided as a productivity and email review tool. FeeHunt is not responsible for missed subscriptions, missed payment warnings, user decisions, third-party service changes, or user-initiated Gmail actions."]], ["Changes to Terms", ["FeeHunt may update these terms before and after public launch. Continued use after changes means acceptance of the updated terms."]], ["Contact", ["For questions about these terms, contact "]]],
    },
  },
};

FH_STATIC_PAGE_TRANSLATIONS.lt = clone(FH_STATIC_PAGE_TRANSLATIONS.en);
mergeTranslation(FH_STATIC_PAGE_TRANSLATIONS.lt, {
  faqPage: { title: "DUK | FeeHunt", description: "Dažniausi klausimai apie FeeHunt.", hero: ["DUK", "Klausimai prieš išbandant FeeHunt?", "Aiškūs atsakymai apie privatumą, Gmail prieigą, bandymus, atšaukimą ir paskyrų limitus."], items: [["Kaip veikia FeeHunt?", "FeeHunt jungiasi prie Gmail per Google OAuth ir skenuoja naujausius laiškus ieškodamas prenumeratų, atnaujinimų, sąskaitų, nepavykusių mokėjimų, reklamų ir galimų sukčiavimo rizikų."], ["Ar mano el. paštas privatus?", "FeeHunt kuriamas kaip privatumą sauganti vietinė darbalaukio programa. Analizė vyksta jūsų kompiuteryje. FeeHunt neparduoda jūsų duomenų."], ["Ar galiu atsaukti bet kada?", "Taip. FeeHunt sukurtas su aiškiu prenumeratos valdymu ir atšaukimu."], ["Kokios Gmail paskyros palaikomos?", "FeeHunt sukurtas Gmail paskyroms, prijungtoms per Google OAuth. Beta laikotarpiu dėmesys skiriamas Gmail ir Windows."], ["Kas nutiks po nemokamo bandymo?", "Po 7 dienų bandymo pasirinktas mokamas planas taps aktyvus, nebent atsauksite iki bandymo pabaigos."], ["Kiek Gmail paskyrų galiu prijungti?", "Basic planas palaiko 1 Gmail paskyrą. Family planas palaiko iki 3 Gmail paskyrų."]] },
  contact: { title: "Kontaktai | FeeHunt", description: "Susisiekite su FeeHunt.", hero: ["Kontaktai", "Susisiekite su FeeHunt.", "Turite klausimą, klaidos pranešimą, produkto idėją ar verslo užklausą? Mums svarbu išgirsti."], left: ["Bendros užklausos", "El. paštas: ", "Beta atsiliepimams naudokite Feedback puslapį, kad galėtume greičiau surinkti struktūruotą informaciją.", "Siųsti atsiliepimą"], right: ["Ką įtraukti", ["Jūsų operacinę sistemą", "Ar naudojate beta ar viešą versiją", "Trumpą problemos ar klausimo aprašymą", "Ekrano kopijas tik jei jose nėra privataus el. pašto turinio"], "Nesiųskite privataus el. pašto turinio, OAuth tokenų, licencijos raktų ar jautrios paskyros informacijos."] },
  feedback: { title: "Atsiliepimai | FeeHunt", description: "Siųskite FeeHunt beta atsiliepimus.", hero: ["Atsiliepimai", "Padėkite formuoti FeeHunt.", "Beta atsiliepimai padeda gerinti aptikimo kokybę, atšaukimo srautus, įvedimą ir privatumą saugantį dizainą."], left: ["Ką siųsti", ["Klaidų pranešimus", "Neaiškius nustatymo žingsnius", "Neteisingai aptiktas prenumeratas", "Funkcijų idėjas", "Sėkmingo atšaukimo istorijas"]], right: ["Kontaktai", "Atsiliepimus siųskite: ", "Nesiųskite privataus el. pašto turinio, OAuth tokenų, licencijos raktų ar jautrios paskyros informacijos.", "Siųsti atsiliepimą"] },
  privacy: { title: "Privatumo politika | FeeHunt", description: "FeeHunt privatumo politika.", hero: ["Privatumo politika", "Privatumas nuo pat pradžių.", "FeeHunt sukurtas remiantis vietiniu apdorojimu, minimaliu duomenų rinkimu ir vartotojo kontrole."], intro: ["Atnaujinta:", " 2026-07-01", "Ši privatumo politika įsigalioja nuo 2026 m. liepos 1 d."], sections: [["Apžvalga", ["FeeHunt yra privatumą sauganti darbalaukio programa, padedanti aptikti prenumeratas, finansinės rizikos laiškus, reklaminį triukšmą ir būsimas sukčiavimo rizikas."]], ["Vietinis apdorojimas", ["FeeHunt apdoroja Gmail skenavimo rezultatus vartotojo kompiuteryje. Analizė, rezultatai, nustatymai ir licencijos metaduomenys lieka vartotojo įrenginyje, nebent būsima funkcija aiškiai nurodytų kitaip."]], ["Gmail prieiga", ["FeeHunt naudoja Google OAuth prieigą. Vartotojas patvirtina prieigą per Google. FeeHunt neprašo ir nesaugo Gmail slaptažodžių."]], ["„Google“ vartotojo duomenys", ["FeeHunt per „Gmail OAuth“ pasiekia šiuos „Google“ vartotojo duomenis:", "„Gmail“ pranešimų metaduomenis ir turinį (tik skaitymo režimu), siekiant nustatyti su prenumeratomis susijusius laiškus, mokėjimų pranešimus ir reklaminį turinį.", "FeeHunt prašo tik būtiniausių OAuth leidimų: „Gmail“ skaitymo prieigos (https://www.googleapis.com/auth/gmail.readonly) ir „Gmail“ keitimo prieigos vartotojo inicijuotiems veiksmams (https://www.googleapis.com/auth/gmail.modify)."], "lead-list"], ["Duomenų dalijimasis ir atskleidimas", ["FeeHunt nesidalija, neperduoda, neparduoda ir neatskleidžia „Google“ vartotojo duomenų jokioms trečiosioms šalims. Visa „Gmail“ analizė atliekama vietiniame vartotojo įrenginyje. Joks el. laiškų turinys ar metaduomenys nėra perduodami į FeeHunt serverius."]], ["Duomenų apsauga ir saugumas", ["FeeHunt saugo jautrius „Google“ vartotojo duomenis (jūsų „Gmail“ laiškus ir metaduomenis) taikydama šiuos saugumo mechanizmus:", "Šifravimas perdavimo metu: visas ryšys su „Gmail“ API vyksta per šifruotą HTTPS/TLS ryšį.", "Šifravimas saugojimo metu: jūsų „Gmail“ OAuth tokenas įrenginyje saugomas užšifruotas naudojant operacinės sistemos šifravimo mechanizmą („Windows Data Protection API“, DPAPI); jis susietas su jūsų „Windows“ vartotojo paskyra, todėl kiti įrenginio vartotojai ar programos jo perskaityti negali.", "Tik vietinis apdorojimas: visa „Gmail“ analizė vyksta jūsų įrenginyje; laiškų turinys ir metaduomenys niekada neperduodami, nesaugomi ir neapdorojami FeeHunt serveriuose ar trečiųjų šalių sistemose.", "Minimalūs leidimai: FeeHunt prašo tik būtiniausių OAuth leidimų ir pasiekia jūsų „Gmail“ duomenis tik jūsų inicijuotiems veiksmams (skenavimui ir jūsų aiškiai patvirtintiems valymo veiksmams).", "Saugojimas ir trynimas: skenavimo rezultatai ir nustatymai lieka jūsų įrenginyje ir gali būti bet kada ištrinti; „Gmail“ prieigą galite bet kada atšaukti per „Google“ paskyrą, po to saugomas tokenas tampa nebenaudojamas.", "Ribotas naudojimas: FeeHunt naudojasi „Google“ API gauta informacija laikydamasis „Google API Services User Data Policy“ (https://developers.google.com/terms/api-services-user-data-policy), įskaitant „Limited Use“ reikalavimus."], "lead-list"], ["Vietoje saugomi duomenys", ["OAuth autorizacijos tokenas", "Skenavimo rezultatai", "Vartotojo nustatymai", "Valymo pasirinkimai", "Vietiniai licencijos metaduomenys"], "list"], ["Minimalus duomenų rinkimas", ["FeeHunt turėtų rinkti tik minimalius duomenis, reikalingus veikimui, licencijavimui, patikimumui ir klientų aptarnavimui."]], ["Duomenys neparduodami", ["FeeHunt neparduoda vartotojų duomenų ir neturėtų parduoti, nuomoti ar keistis Gmail duomenimis, rezultatais ar paskyros informacija."]], ["Mokėjimai ir licencijavimas", ["Viešo paleidimo licencijavimas ir mokėjimai gali reikalauti paskyros, atsiskaitymo ir licencijos duomenų. Mokėjimus turi tvarkyti patikimas tiekėjas, pvz., Stripe. FeeHunt neturėtų saugoti kortelių duomenų."]], ["Vartotojo kontrolė", ["Atšaukti Gmail prieigą per Google paskyrą", "Ištrinti vietinius FeeHunt failus iš kompiuterio", "Atšaukti mokamą prenumeratą per aiškų savitarnos kelią"], "list"], ["Kontaktai", ["Privatumo klausimais rašykite "]]]},
  terms: { title: "Naudojimo sąlygos | FeeHunt", description: "FeeHunt naudojimo sąlygos.", hero: ["Naudojimo sąlygos", "FeeHunt naudojimo sąlygos.", "Šios sąlygos aprašo produkto naudojimą, beta ribojimus, atsiskaitymą, atšaukimą ir vartotojo atsakomybę."], intro: ["Atnaujinta:", " 2026-07-01", "Šios naudojimo sąlygos įsigalioja nuo 2026 m. birželio 16 d."], sections: [["Sąlygų priėmimas", ["Naudodami FeeHunt sutinkate su šiomis naudojimo sąlygomis. Jei nesutinkate, produkto nenaudokite."]], ["Produkto aprašymas", ["FeeHunt yra darbalaukio programa, padedanti peržiūrėti Gmail prenumeratas, finansinės rizikos laiškus, reklaminį triukšmą ir būsimas saugumo rizikas.", "FeeHunt teikia aptikimo ir organizavimo įrankius, bet negarantuoja, kad aptiks kiekvieną prenumeratą, mokėjimo problemą, reklamą ar sukčiavimą."]], ["Beta programinė įranga", ["FeeHunt beta versijose gali būti klaidų, nebaigtų funkcijų ir besikeičiančio elgesio. Vartotojai turi atidžiai peržiūrėti rezultatus prieš Gmail veiksmus."]], ["Vartotojo atsakomybė", ["Peržiūrėti aptiktus laiškus prieš veiksmus", "Suprasti, kad archyvavimas, trynimas ir kiti Gmail veiksmai paveikia tikrus laiškus", "Išlaikyti prieigą prie Gmail paskyros", "Saugoti OAuth failus, tokenus, licencijos raktus ir vietinius duomenis"]], ["Gmail autorizacija", ["FeeHunt naudoja Google OAuth Gmail prieigai. Vartotojas gali atšaukti prieigą Google paskyros nustatymuose."]], ["Prenumeratos ir atsiskaitymas", ["Basic: €5.90/mėn.", "Family: €9.90/mėn.", "7 dienų nemokamas bandymas", "Galima atšaukti bet kada", "Viešas mokamas taikymas turi prasidėti tik tada, kai veikia checkout, klientų portalas ir atšaukimo srautai."]], ["Atšaukimas", ["Vartotojai turi galėti atšaukti mokamas prenumeratas per aiškų savitarnos kelią. Prieiga lieka aktyvi iki apmokėto laikotarpio pabaigos, nebent nurodyta kitaip."]], ["Netinkamas naudojimas", ["Vartotojai negali naudoti FeeHunt įstatymų pažeidimui, Gmail piktnaudžiavimui ar neteisėtai prieigai prie paskyrų ar infrastruktūros."]], ["Atsakomybės ribojimas", ["FeeHunt yra produktyvumo ir el. pašto peržiūros įrankis. FeeHunt neatsako už praleistas prenumeratas, mokėjimo perspėjimus, vartotojo sprendimus ar vartotojo inicijuotus Gmail veiksmus."]], ["Sąlygų keitimai", ["FeeHunt gali atnaujinti šias sąlygas prieš ir po viešo paleidimo. Toliau naudodami produktą sutinkate su atnaujintomis sąlygomis."]], ["Kontaktai", ["Dėl šių sąlygų rašykite "]]]},
});

const shortLanguageNames = {
  no: ["norsk", "konto", "lisensnøkkel", "prøveperiode", "Last ned"],
  es: ["español", "cuenta", "clave de licencia", "prueba", "Descargar"],
  de: ["deutsch", "Konto", "Lizenzschlüssel", "Testphase", "Download"],
  fr: ["français", "compte", "clé de licence", "essai", "Télécharger"],
};

["no", "es", "de", "fr"].forEach((code) => {
  const [languageName, accountWord, keyWord, trialWord, downloadWord] = shortLanguageNames[code];
  FH_STATIC_PAGE_TRANSLATIONS[code] = clone(FH_STATIC_PAGE_TRANSLATIONS.en);
  mergeTranslation(FH_STATIC_PAGE_TRANSLATIONS[code], {
    faqPage: {
      title: "FAQ | FeeHunt",
      description: `FeeHunt FAQ in ${languageName}.`,
      hero: ["FAQ", `Questions before trying FeeHunt?`, `Clear answers about privacy, Gmail access, ${trialWord}, cancellation, and account limits.`],
      items: [["How does FeeHunt work?", "FeeHunt connects through Google OAuth and scans recent Gmail messages for subscriptions, renewals, invoices, failed payments, promotions, and risk signals."], ["Is my email private?", "FeeHunt is designed as a privacy-first local desktop app. Email analysis happens on your computer."], ["Can I cancel anytime?", "Yes. FeeHunt supports clear subscription management and cancellation."], ["Which Gmail accounts are supported?", "FeeHunt is designed for Gmail accounts connected through Google OAuth."], ["What happens after the free trial?", "After the 7-day trial, the selected paid plan becomes active unless you cancel before the trial ends."], ["How many Gmail accounts can I connect?", "Basic supports 1 Gmail account. Family supports up to 3 Gmail accounts."]],
    },
    contact: { title: "Contact | FeeHunt", description: `Contact FeeHunt in ${languageName}.`, hero: ["Contact", "Contact FeeHunt.", "Questions, bug reports, product ideas, and business inquiries are welcome."], left: ["General inquiries", "Email: ", "For beta feedback, please use the Feedback page so we can improve faster.", "Send Feedback"], right: ["What to include", ["Your operating system", "Whether you use beta or public version", "A short description", "Screenshots only without private email content"], "Do not send private email content, OAuth tokens, license keys, or sensitive account information."] },
    feedback: { title: "Feedback | FeeHunt", description: `Send FeeHunt feedback in ${languageName}.`, hero: ["Feedback", "Help shape FeeHunt.", "Beta feedback helps improve detection quality, cancellation flows, onboarding, and privacy-first design."], left: ["What to send", ["Bug reports", "Confusing setup steps", "False subscription detections", "Feature ideas", "Cancellation success stories"]], right: ["Contact", "Email feedback to ", "Avoid private email content, OAuth tokens, license keys, or sensitive account information.", "Send Feedback"] },
    privacy: {
      hero: ["Privacy", "Privacy-first by design.", "FeeHunt is designed around local processing, minimal data collection, and user control."],
      sections: [["Privacy overview", ["FeeHunt helps identify subscriptions, payment-control emails, promotional clutter, and future phishing-risk patterns with privacy-first local analysis."]], ["Local processing", ["Gmail scan results, settings, and license metadata are designed to remain on the user's computer unless a future feature clearly says otherwise."]], ["Gmail access", ["FeeHunt uses Google OAuth. FeeHunt does not ask for or store Gmail passwords."]], ["Local data", ["OAuth authorization token", "Scan results", "User settings", "Cleanup preferences", "Local license metadata"]], ["Minimal data collection", ["FeeHunt should collect only the minimum data required to operate, support licensing, improve reliability, and provide customer support."]], ["No selling user data", ["FeeHunt does not sell Gmail data, scan results, or personal account information."]], ["Payments and licensing", ["Payment and license features may require account, billing, and license data. Stripe should process payments, and FeeHunt should not store raw card data."]], ["User control", ["Revoke Gmail access through Google", "Delete local FeeHunt files", "Cancel paid subscriptions through self-service"]], ["Contact", ["For privacy questions, contact "]]],
    },
    terms: {
      hero: ["Terms", "FeeHunt usage terms.", "These terms describe product use, beta limitations, billing, cancellation, and user responsibility."],
      sections: [["Acceptance", ["By using FeeHunt, you agree to these terms. If you do not agree, do not use the product."]], ["Product description", ["FeeHunt helps users review Gmail for subscriptions, payment-control messages, promotional clutter, and future security-related email patterns.", "FeeHunt provides detection and organization tools, but does not guarantee that every issue will be detected."]], ["Beta software", ["FeeHunt beta versions may contain bugs, incomplete features, and changing behavior. Review results carefully before Gmail actions."]], ["User responsibility", ["Review detected emails before taking action", "Understand that Gmail actions affect real email", "Maintain access to your Gmail account", "Keep OAuth files, tokens, license keys, and local data secure"]], ["Gmail authorization", ["FeeHunt uses Google OAuth for Gmail access. Users can revoke access through Google account settings."]], ["Subscriptions and billing", ["Basic: €5.90/month", "Family: €9.90/month", "7-day free trial", "Cancel anytime", "Paid billing should only be enforced when checkout, customer portal, and cancellation flows are ready."]], ["Cancellation", ["Users should be able to cancel paid subscriptions through a clear self-service flow."]], ["No misuse", ["Users may not use FeeHunt to violate laws, abuse Gmail, or attempt unauthorized access."]], ["Limitation of liability", ["FeeHunt is a productivity and email review tool and is not responsible for missed subscriptions, missed warnings, user decisions, or Gmail actions."]], ["Changes to terms", ["FeeHunt may update these terms before and after public launch."]], ["Contact", ["For questions about these terms, contact "]]],
    },
  });
});

mergeTranslation(FH_STATIC_PAGE_TRANSLATIONS.no, {
  privacy: { title: "Personvern | FeeHunt", description: "FeeHunts personvernerklæring.", hero: ["Personvern", "Personvern først.", "FeeHunt er bygget rundt lokal behandling, minimal datainnsamling og brukerens kontroll."], intro: ["Sist oppdatert:", " 2026-07-01", "Denne personvernerklæringen er gyldig fra 16. juni 2026."], sections: [["Oversikt", ["FeeHunt hjelper brukere å finne abonnementer, økonomiske risikomeldinger, reklamepost og mulige phishing-risikoer med lokal analyse."]], ["Lokal behandling", ["Gmail-resultater, innstillinger og lisensmetadata er laget for å bli på brukerens datamaskin med mindre en fremtidig funksjon tydelig sier noe annet."]], ["Gmail-tilgang", ["FeeHunt bruker Google OAuth. FeeHunt ber ikke om og lagrer ikke Gmail-passord."]], ["Google-brukerdata", ["FeeHunt henter følgende Google-brukerdata via Gmail OAuth:", "Gmail-meldingers metadata og innhold (kun lesetilgang) for å identifisere abonnementsrelaterte e-poster, faktureringsvarsler og reklamestøy.", "FeeHunt ber kun om de minimale OAuth-tillatelsene som er nødvendige: Gmail-lesetilgang (https://www.googleapis.com/auth/gmail.readonly) og Gmail-endringstilgang for brukerinitierte handlinger (https://www.googleapis.com/auth/gmail.modify)."], "lead-list"], ["Deling og utlevering av data", ["FeeHunt deler, overfører, selger eller utleverer ikke Google-brukerdata til noen tredjeparter. All Gmail-analyse utføres lokalt på brukerens enhet. Ikke noe e-postinnhold eller metadata overføres til FeeHunt-servere."]], ["Databeskyttelse", ["FeeHunt beskytter sensitive Google-brukerdata ved å:", "Behandle alle Gmail-data kun lokalt på brukerens enhet", "Aldri lagre e-postinnhold på eksterne servere", "Bruke OAuth-token som brukeren når som helst kan tilbakekalle via innstillingene for Google-kontoen", "Ikke logge eller overføre noe Gmail-innhold eller metadata eksternt"], "lead-list"], ["Lokale data", ["OAuth-token", "Skanneresultater", "Brukerinnstillinger", "Oppryddingsvalg", "Lokal lisensmetadata"], "list"], ["Minimal datainnsamling", ["FeeHunt skal bare samle inn data som trengs for drift, lisensiering, stabilitet og kundestøtte."]], ["Ingen salg av data", ["FeeHunt selger ikke Gmail-data, skanneresultater eller personlig kontoinformasjon."]], ["Betaling og lisens", ["Betaling og lisens kan kreve konto-, faktura- og lisensdata. Stripe bør håndtere betalinger, og FeeHunt skal ikke lagre kortdata."]], ["Brukerkontroll", ["Trekk tilbake Gmail-tilgang via Google", "Slett lokale FeeHunt-filer", "Avbryt betalte abonnementer via selvbetjening"], "list"], ["Kontakt", ["For personvernspørsmål, kontakt "]]]},
  terms: { title: "Vilkår | FeeHunt", description: "FeeHunts bruksvilkår.", hero: ["Vilkår", "FeeHunt bruksvilkår.", "Disse vilkårene beskriver bruk, beta-begrensninger, betaling, avbestilling og brukeransvar."], intro: ["Sist oppdatert:", " 2026-07-01", "Disse bruksvilkårene er gyldige fra 16. juni 2026."], sections: [["Aksept av vilkår", ["Ved å bruke FeeHunt godtar du disse vilkårene. Hvis du ikke godtar dem, må du ikke bruke produktet."]], ["Produktbeskrivelse", ["FeeHunt hjelper brukere å gjennomgå Gmail for abonnementer, økonomiske risikomeldinger, reklamepost og sikkerhetsrelaterte mønstre.", "FeeHunt gir verktøy for oppdagelse og organisering, men garanterer ikke at alt blir funnet."]], ["Beta-programvare", ["Beta-versjoner kan inneholde feil, uferdige funksjoner og endret oppførsel. Gå gjennom resultater før Gmail-handlinger."]], ["Brukeransvar", ["Gå gjennom oppdagede e-poster før handling", "Forstå at Gmail-handlinger påvirker ekte e-post", "Behold tilgang til Gmail-kontoen", "Beskytt OAuth-filer, token, lisensnøkler og lokale data"]], ["Gmail-autorisasjon", ["FeeHunt bruker Google OAuth for Gmail-tilgang. Tilgang kan trekkes tilbake i Google-kontoen."]], ["Abonnement og betaling", ["Basic: €5.90/måned", "Family: €9.90/måned", "7 dagers prøveperiode", "Avbryt når som helst", "Betalt fakturering bør bare håndheves når checkout, kundeportal og avbestilling er klare."]], ["Avbestilling", ["Brukere bør kunne avbryte betalte abonnementer gjennom en tydelig selvbetjeningsflyt."]], ["Forbudt bruk", ["FeeHunt må ikke brukes til lovbrudd, misbruk av Gmail eller uautorisert tilgang."]], ["Ansvarsbegrensning", ["FeeHunt er et produktivitets- og e-postverktøy og er ikke ansvarlig for oversette abonnementer, varsler, brukerbeslutninger eller Gmail-handlinger."]], ["Endringer", ["FeeHunt kan oppdatere disse vilkårene før og etter offentlig lansering."]], ["Kontakt", ["For spørsmål om vilkårene, kontakt "]]]},
});

mergeTranslation(FH_STATIC_PAGE_TRANSLATIONS.es, {
  privacy: { title: "Privacidad | FeeHunt", description: "Política de privacidad de FeeHunt.", hero: ["Privacidad", "Privacidad desde el diseño.", "FeeHunt está diseñado con procesamiento local, mínima recopilación de datos y control del usuario."], intro: ["Última actualización:", " 2026-07-01", "Esta política de privacidad es efectiva a partir del 16 de junio de 2026."], sections: [["Resumen", ["FeeHunt ayuda a identificar suscripciones, correos de control de pagos, promociones y posibles riesgos de phishing con análisis local."]], ["Procesamiento local", ["Los resultados de Gmail, ajustes y metadatos de licencia están diseñados para quedarse en el ordenador del usuario salvo que una función futura indique lo contrario."]], ["Acceso a Gmail", ["FeeHunt usa Google OAuth. FeeHunt no pide ni almacena contraseñas de Gmail."]], ["Datos de usuario de Google", ["FeeHunt accede a los siguientes datos de usuario de Google mediante Gmail OAuth:", "Metadatos y contenido de los mensajes de Gmail (solo lectura) para identificar correos relacionados con suscripciones, avisos de facturación y ruido promocional.", "FeeHunt solicita únicamente los permisos OAuth mínimos necesarios: acceso de lectura a Gmail (https://www.googleapis.com/auth/gmail.readonly) y acceso de modificación de Gmail para acciones iniciadas por el usuario (https://www.googleapis.com/auth/gmail.modify)."], "lead-list"], ["Compartición y divulgación de datos", ["FeeHunt no comparte, transfiere, vende ni divulga los datos de usuario de Google a terceros. Todo el análisis de Gmail se realiza localmente en el dispositivo del usuario. Ningún contenido de correo ni metadato se transmite a los servidores de FeeHunt."]], ["Protección de datos", ["FeeHunt protege los datos sensibles de usuario de Google mediante:", "Procesar todos los datos de Gmail únicamente de forma local en el dispositivo del usuario", "No almacenar nunca el contenido de los correos en servidores externos", "Usar tokens OAuth que el usuario puede revocar en cualquier momento desde la configuración de su cuenta de Google", "No registrar ni transmitir externamente ningún contenido ni metadato de Gmail"], "lead-list"], ["Datos locales", ["Token OAuth", "Resultados de escaneo", "Ajustes de usuario", "Preferencias de limpieza", "Metadatos locales de licencia"], "list"], ["Datos mínimos", ["FeeHunt debe recopilar solo los datos necesarios para operar, licenciar, mejorar fiabilidad y dar soporte."]], ["No venta de datos", ["FeeHunt no vende datos de Gmail, resultados de escaneo ni información personal de cuenta."]], ["Pago y licencia", ["Los pagos y licencias pueden requerir datos de cuenta, facturación y licencia. Stripe debe procesar pagos y FeeHunt no debe guardar tarjetas."]], ["Control del usuario", ["Revocar acceso a Gmail en Google", "Eliminar archivos locales de FeeHunt", "Cancelar suscripciones pagadas por autoservicio"], "list"], ["Contacto", ["Para preguntas de privacidad, contacta "]]]},
  terms: { title: "Términos | FeeHunt", description: "Términos de uso de FeeHunt.", hero: ["Términos", "Términos de uso de FeeHunt.", "Estos términos describen uso, límites beta, pagos, cancelación y responsabilidad del usuario."], intro: ["Última actualización:", " 2026-07-01", "Estos términos de uso son efectivos a partir del 16 de junio de 2026."], sections: [["Aceptación", ["Al usar FeeHunt aceptas estos términos. Si no estás de acuerdo, no uses el producto."]], ["Descripción del producto", ["FeeHunt ayuda a revisar Gmail para suscripciones, correos de control de pagos, promociones y patrones de seguridad.", "FeeHunt ofrece herramientas de detección y organización, pero no garantiza encontrar todos los casos."]], ["Software beta", ["Las versiones beta pueden contener errores, funciones incompletas y cambios de comportamiento. Revisa resultados antes de acciones en Gmail."]], ["Responsabilidad del usuario", ["Revisar correos detectados antes de actuar", "Entender que las acciones de Gmail afectan correos reales", "Mantener acceso a la cuenta Gmail", "Proteger archivos OAuth, tokens, claves y datos locales"]], ["Autorización Gmail", ["FeeHunt usa Google OAuth. El acceso puede revocarse desde Google."]], ["Suscripciones y facturación", ["Basic: €5.90/mes", "Family: €9.90/mes", "Prueba de 7 días", "Cancelar cuando quieras", "La facturación pagada debe aplicarse solo cuando checkout, portal y cancelación estén listos."]], ["Cancelación", ["Los usuarios deben poder cancelar suscripciones pagadas mediante autoservicio claro."]], ["Uso indebido", ["No se puede usar FeeHunt para violar leyes, abusar de Gmail o intentar acceso no autorizado."]], ["Limitación de responsabilidad", ["FeeHunt es una herramienta de productividad y revisión de email y no responde por suscripciones omitidas, avisos omitidos, decisiones del usuario o acciones de Gmail."]], ["Cambios", ["FeeHunt puede actualizar estos términos antes y después del lanzamiento público."]], ["Contacto", ["Para preguntas sobre estos términos, contacta "]]]},
});

mergeTranslation(FH_STATIC_PAGE_TRANSLATIONS.de, {
  privacy: { title: "Datenschutz | FeeHunt", description: "FeeHunt Datenschutzhinweise.", hero: ["Datenschutz", "Datenschutz von Anfang an.", "FeeHunt setzt auf lokale Verarbeitung, minimale Datenerfassung und Nutzerkontrolle."], intro: ["Zuletzt aktualisiert:", " 2026-07-01", "Diese Datenschutzrichtlinie gilt ab dem 16. Juni 2026."], sections: [["Überblick", ["FeeHunt hilft, Abonnements, finanzielle Risiko-E-Mails, Werbung und mögliche Phishing-Risiken lokal zu erkennen."]], ["Lokale Verarbeitung", ["Gmail-Ergebnisse, Einstellungen und Lizenzmetadaten sollen auf dem Computer des Nutzers bleiben, sofern keine künftige Funktion klar etwas anderes sagt."]], ["Gmail-Zugriff", ["FeeHunt nutzt Google OAuth. FeeHunt fragt nicht nach Gmail-Passwörtern und speichert sie nicht."]], ["Google-Nutzerdaten", ["FeeHunt greift über Gmail OAuth auf die folgenden Google-Nutzerdaten zu:", "Metadaten und Inhalte von Gmail-Nachrichten (nur Lesezugriff), um abonnementbezogene E-Mails, Rechnungshinweise und Werbechaos zu identifizieren.", "FeeHunt fordert nur die minimal notwendigen OAuth-Berechtigungen an: Gmail-Lesezugriff (https://www.googleapis.com/auth/gmail.readonly) und Gmail-Änderungszugriff für vom Nutzer ausgelöste Aktionen (https://www.googleapis.com/auth/gmail.modify)."], "lead-list"], ["Weitergabe und Offenlegung von Daten", ["FeeHunt gibt Google-Nutzerdaten nicht an Dritte weiter, überträgt, verkauft oder legt sie nicht offen. Die gesamte Gmail-Analyse erfolgt lokal auf dem Gerät des Nutzers. Es werden keine E-Mail-Inhalte oder Metadaten an FeeHunt-Server übertragen."]], ["Datensicherheit", ["FeeHunt schützt sensible Google-Nutzerdaten durch:", "Verarbeitung aller Gmail-Daten ausschließlich lokal auf dem Gerät des Nutzers", "Niemals Speicherung von E-Mail-Inhalten auf externen Servern", "Verwendung von OAuth-Tokens, die der Nutzer jederzeit über die Einstellungen seines Google-Kontos widerrufen kann", "Kein externes Protokollieren oder Übertragen von Gmail-Inhalten oder Metadaten"], "lead-list"], ["Lokale Daten", ["OAuth-Token", "Scan-Ergebnisse", "Nutzereinstellungen", "Aufräumpräferenzen", "Lokale Lizenzmetadaten"], "list"], ["Minimale Datenerfassung", ["FeeHunt sollte nur Daten erfassen, die für Betrieb, Lizenzierung, Zuverlässigkeit und Support nötig sind."]], ["Kein Verkauf von Daten", ["FeeHunt verkauft keine Gmail-Daten, Scan-Ergebnisse oder persönlichen Kontoinformationen."]], ["Zahlung und Lizenz", ["Zahlung und Lizenz können Konto-, Abrechnungs- und Lizenzdaten erfordern. Stripe sollte Zahlungen verarbeiten; FeeHunt sollte keine Kartendaten speichern."]], ["Nutzerkontrolle", ["Gmail-Zugriff über Google widerrufen", "Lokale FeeHunt-Dateien löschen", "Bezahlte Abos per Selbstbedienung kündigen"], "list"], ["Kontakt", ["Bei Datenschutzfragen kontaktieren Sie "]]]},
  terms: { title: "Bedingungen | FeeHunt", description: "FeeHunt Nutzungsbedingungen.", hero: ["Bedingungen", "FeeHunt Nutzungsbedingungen.", "Diese Bedingungen beschreiben Nutzung, Beta-Grenzen, Zahlung, Kündigung und Nutzerverantwortung."], intro: ["Zuletzt aktualisiert:", " 2026-07-01", "Diese Nutzungsbedingungen gelten ab dem 16. Juni 2026."], sections: [["Annahme der Bedingungen", ["Durch die Nutzung von FeeHunt stimmen Sie diesen Bedingungen zu. Wenn Sie nicht zustimmen, nutzen Sie das Produkt nicht."]], ["Produktbeschreibung", ["FeeHunt hilft, Gmail auf Abonnements, Zahlungskontrolle, Werbung und sicherheitsbezogene Muster zu prüfen.", "FeeHunt bietet Erkennungs- und Organisationswerkzeuge, garantiert aber nicht, jeden Fall zu finden."]], ["Beta-Software", ["Beta-Versionen können Fehler, unvollständige Funktionen und verändertes Verhalten enthalten. Prüfen Sie Ergebnisse vor Gmail-Aktionen."]], ["Nutzerverantwortung", ["Gefundene E-Mails vor Aktionen prüfen", "Verstehen, dass Gmail-Aktionen echte E-Mails betreffen", "Zugriff auf das Gmail-Konto erhalten", "OAuth-Dateien, Token, Lizenzschlüssel und lokale Daten schützen"]], ["Gmail-Autorisierung", ["FeeHunt nutzt Google OAuth. Zugriff kann in den Google-Kontoeinstellungen widerrufen werden."]], ["Abos und Abrechnung", ["Basic: €5.90/Monat", "Family: €9.90/Monat", "7 Tage Testphase", "Jederzeit kündbar", "Bezahlte Abrechnung sollte erst gelten, wenn Checkout, Kundenportal und Kündigung bereit sind."]], ["Kündigung", ["Nutzer sollten bezahlte Abos über einen klaren Selbstbedienungsweg kündigen können."]], ["Missbrauch", ["FeeHunt darf nicht für Rechtsverstöße, Gmail-Missbrauch oder unbefugten Zugriff verwendet werden."]], ["Haftungsbegrenzung", ["FeeHunt ist ein Produktivitäts- und E-Mail-Prüfwerkzeug und haftet nicht für verpasste Abos, Warnungen, Nutzerentscheidungen oder Gmail-Aktionen."]], ["Änderungen", ["FeeHunt kann diese Bedingungen vor und nach dem öffentlichen Start aktualisieren."]], ["Kontakt", ["Bei Fragen zu diesen Bedingungen kontaktieren Sie "]]]},
});

mergeTranslation(FH_STATIC_PAGE_TRANSLATIONS.fr, {
  privacy: { title: "Confidentialité | FeeHunt", description: "Politique de confidentialité FeeHunt.", hero: ["Confidentialité", "Confidentialité dès la conception.", "FeeHunt repose sur le traitement local, la collecte minimale et le contrôle utilisateur."], intro: ["Dernière mise à jour :", " 2026-07-01", "Cette politique de confidentialité est effective à partir du 16 juin 2026."], sections: [["Aperçu", ["FeeHunt aide à identifier les abonnements, emails de contrôle des paiements, promotions et risques de phishing avec une analyse locale."]], ["Traitement local", ["Les résultats Gmail, paramètres et métadonnées de licence sont conçus pour rester sur l'ordinateur de l'utilisateur sauf indication claire d'une future fonction."]], ["Accès Gmail", ["FeeHunt utilise Google OAuth. FeeHunt ne demande ni ne stocke les mots de passe Gmail."]], ["Données utilisateur Google", ["FeeHunt accède aux données utilisateur Google suivantes via Gmail OAuth :", "Métadonnées et contenu des messages Gmail (lecture seule) afin d'identifier les emails liés aux abonnements, les avis de facturation et le bruit promotionnel.", "FeeHunt demande uniquement les autorisations OAuth minimales nécessaires : accès en lecture à Gmail (https://www.googleapis.com/auth/gmail.readonly) et accès en modification à Gmail pour les actions initiées par l'utilisateur (https://www.googleapis.com/auth/gmail.modify)."], "lead-list"], ["Partage et divulgation des données", ["FeeHunt ne partage, ne transfère, ne vend ni ne divulgue les données utilisateur Google à aucun tiers. Toute l'analyse Gmail est effectuée localement sur l'appareil de l'utilisateur. Aucun contenu d'email ni métadonnée n'est transmis aux serveurs de FeeHunt."]], ["Protection des données", ["FeeHunt protège les données utilisateur Google sensibles en :", "Traitant toutes les données Gmail uniquement localement sur l'appareil de l'utilisateur", "Ne stockant jamais le contenu des emails sur des serveurs externes", "Utilisant des jetons OAuth que l'utilisateur peut révoquer à tout moment via les paramètres de son compte Google", "Ne journalisant ni ne transmettant aucun contenu ou métadonnée Gmail en externe"], "lead-list"], ["Données locales", ["Jeton OAuth", "Résultats d'analyse", "Paramètres utilisateur", "Préférences de nettoyage", "Métadonnées locales de licence"], "list"], ["Collecte minimale", ["FeeHunt ne doit collecter que les données nécessaires au fonctionnement, à la licence, à la fiabilité et au support."]], ["Pas de vente des données", ["FeeHunt ne vend pas les données Gmail, résultats d'analyse ou informations personnelles de compte."]], ["Paiement et licence", ["Les paiements et licences peuvent nécessiter des données de compte, facturation et licence. Stripe doit traiter les paiements et FeeHunt ne doit pas stocker les cartes."]], ["Contrôle utilisateur", ["Révoquer l'accès Gmail via Google", "Supprimer les fichiers locaux FeeHunt", "Annuler les abonnements payants en libre-service"], "list"], ["Contact", ["Pour les questions de confidentialité, contactez "]]]},
  terms: { title: "Conditions | FeeHunt", description: "Conditions d'utilisation FeeHunt.", hero: ["Conditions", "Conditions d'utilisation FeeHunt.", "Ces conditions décrivent l'utilisation, les limites beta, le paiement, l'annulation et la responsabilité utilisateur."], intro: ["Dernière mise à jour :", " 2026-07-01", "Ces conditions d'utilisation sont effectives à partir du 16 juin 2026."], sections: [["Acceptation", ["En utilisant FeeHunt, vous acceptez ces conditions. Si vous n'acceptez pas, n'utilisez pas le produit."]], ["Description du produit", ["FeeHunt aide à examiner Gmail pour les abonnements, le contrôle des paiements, promotions et modèles liés à la sécurité.", "FeeHunt fournit des outils de détection et d'organisation, mais ne garantit pas de tout détecter."]], ["Logiciel beta", ["Les versions beta peuvent contenir des erreurs, fonctions incomplètes et comportements changeants. Vérifiez les résultats avant les actions Gmail."]], ["Responsabilité utilisateur", ["Vérifier les emails détectés avant action", "Comprendre que les actions Gmail affectent de vrais emails", "Maintenir l'accès au compte Gmail", "Protéger fichiers OAuth, jetons, clés et données locales"]], ["Autorisation Gmail", ["FeeHunt utilise Google OAuth. L'accès peut être révoqué dans les paramètres Google."]], ["Abonnements et facturation", ["Basic : €5.90/mois", "Family : €9.90/mois", "Essai de 7 jours", "Annulation à tout moment", "La facturation payante ne doit s'appliquer que lorsque checkout, portail client et annulation sont prêts."]], ["Annulation", ["Les utilisateurs doivent pouvoir annuler les abonnements payants via un parcours clair en libre-service."]], ["Utilisation interdite", ["FeeHunt ne doit pas être utilisé pour violer la loi, abuser de Gmail ou tenter un accès non autorisé."]], ["Limitation de responsabilité", ["FeeHunt est un outil de productivité et de revue email et n'est pas responsable des abonnements ou avertissements manqués, décisions utilisateur ou actions Gmail."]], ["Changements", ["FeeHunt peut mettre à jour ces conditions avant et après le lancement public."]], ["Contact", ["Pour les questions sur ces conditions, contactez "]]]},
});

Object.entries(FH_STATIC_PAGE_TRANSLATIONS).forEach(([code, overrides]) => {
  mergeTranslation(FH_I18N[code], overrides);
});

const FH_FINAL_TRANSLATION_PATCHES = {
  lt: {
    common: {
      nav: ["Pradžia", "Kainodara", "Atsisiųsti", "DUK", "Privatumas", "Sąlygos", "Kontaktai", "Prisijungti"],
      navExtra: { "signup.html": "Pradėti bandymą" },
      download: "Atsisiųsti",
      downloadBeta: "Atsisiųsti Beta",
      startTrial: "Pradėti bandymą",
      footer: ["Privatumo politika", "Naudojimo sąlygos", "Kontaktai"],
      menu: "Meniu",
    },
    home: {
      title: "FeeHunt | Raskite pamirštas prenumeratas",
      description: "Raskite pamirštas prenumeratas, taupykite pinigus ir apsaugokite savo paštą su FeeHunt.",
      heroEyebrow: "Privatumu paremta prenumeratų kontrolė",
      heroHeading: "Raskite pamirštas prenumeratas, taupykite pinigus ir apsaugokite savo paštą.",
      heroLead: "FeeHunt padeda aptikti prenumeratas, mokėjimų kontrolės signalus, reklaminį triukšmą ir galimas sukčiavimo grėsmes - privačiai jūsų kompiuteryje.",
      heroButtons: ["Pradėti nemokamą bandymą", "Atsisiųsti Beta"],
      heroScanCards: [["Aptikta pasikartojanti prenumerata", "Rasti atnaujinimo ir apmokėjimo signalai"], ["Aptikta mokėjimo problema", "Nepavykęs mokestis arba kortelės atnaujinimo laiškas"], ["Įtartinas atsiskaitymo laiškas", "Peržiūrėkite prieš spausdami nuorodą"], ["Reklaminis triukšmas", "Naujienlaiškiai ir parduotuvių žinutės sugrupuotos"]],
      principle: "FeeHunt veikia jūsų naudai. Kontrolė lieka jūsų rankose.",
      badges: ["7 dienų bandymas", "Galima atšaukti bet kada", "Privatumas pirmiausia", "Veikia lokaliai"],
      badgeDetails: ["Vietinis apdorojimas", "Jūsų įrenginyje", "Duomenys nerenkami"],
      why: ["Kodėl FeeHunt", "Prenumeratas lengva pradėti ir lengva pamiršti.", "Mokėjimų pranešimai pasimeta tarp naujienlaiškių, reklamų, kvitų ir įprastų laiškų. FeeHunt padeda peržiūrėti tai, kas svarbu.", "FeeHunt analizuoja signalus jūsų kompiuteryje ir klausia prieš Gmail keičiančius veiksmus."],
      visualToolbar: "FeeHunt vietinis valdymo skydas",
      visualPill: "Privatu jūsų kompiuteryje",
      visualRows: [["Prenumeratos prieiga sustabdyta", "Aptikta mokėjimo problema", "Mokėjimų kontrolė"], ["Reklamų ir naujienlaiškių tvarkymas", "Peržiūrėkite siuntėjus prieš archyvavimą ar trynimą", "Pašto tvarkymas"], ["Atšaukti prenumeratą", "Atidaryti tinkamiausią atsisakymo ar paskyros kelią", "Veiksmas paruoštas"]],
      featuresHeading: ["Funkcijos", "Sukurta prenumeratų aiškumui ir pašto kontrolei."],
      features: [["Prenumeratų aptikimas", "Aptinka pasikartojančius mokėjimus, atnaujinimus, sąskaitas ir bandymus."], ["Mokėjimų kontrolė", "Pažymi nepavykusius mokėjimus, atmestas korteles ir sustabdytas paskyras."], ["Prenumeratos atšaukimas", "Atidaro tinkamiausią atsisakymo, paskyros ar apmokėjimo puslapį."], ["Pašto tvarkymas", "Padeda peržiūrėti reklaminius laiškus, naujienlaiškius ir parduotuvių žinutes."], ["Saugumo skydas", "Ateities versijos padės aptikti sukčiavimo rizikas."]],
      pricingHeading: ["Kainų peržiūra", "Paprasti mėnesiniai planai su 7 dienų bandymu."],
      plans: [["Basic", "Vienai Gmail paskyrai.", ["1 Gmail paskyra", "1 licencijos raktas", "7 dienų bandymas", "Galima atšaukti bet kada"], "Pasirinkti Basic"], ["Family", "Iki trijų Gmail paskyrų.", ["Iki 3 Gmail paskyrų", "1 licencijos raktas", "7 dienų bandymas", "Galima atšaukti bet kada"], "Pasirinkti Family"]],
      pricePeriod: "/mėn.",
      pricingNotice: "Jokių paslėptų mokesčių. Atšaukti galima bet kada.",
      faqHeading: ["DUK", "Klausimai apie paslėptas prenumeratas ir Gmail tvarkymą."],
      faq: [["Ar FeeHunt gali rasti paslėptas prenumeratas Gmail?", "FeeHunt ieško prenumeratų laiškų, atnaujinimo pranešimų, sąskaitų, bandomųjų laikotarpių priminimų ir pasikartojančių mokėjimų signalų, kad galėtumėte peržiūrėti pamirštas paslaugas prieš joms kainuojant daugiau."], ["Ar FeeHunt veikia kaip Gmail tvarkymo įrankis?", "Taip. FeeHunt padeda peržiūrėti naujienlaiškius, reklaminius laiškus, parduotuvių žinutes ir kitą pašto triukšmą. Gmail keičiantys veiksmai lieka jūsų kontrolėje."], ["Ar FeeHunt gali įspėti apie finansinės rizikos laiškus?", "FeeHunt paryškina nepavykusių mokėjimų laiškus, vėluojančias sąskaitas, atmestų kortelių pranešimus, pristabdytas prenumeratas ir kitus atsiskaitymo laiškus, kuriems gali reikėti dėmesio."], ["Ar FeeHunt privatus?", "FeeHunt sukurtas privatumą saugančiai vietinei analizei. Gmail peržiūra vyksta jūsų kompiuteryje, o FeeHunt klausia prieš veiksmus, kurie archyvuoja, ištrina ar pakeičia laiškus."], ["Ar FeeHunt aptinka sukčiavimo laiškus?", "Šiuo metu FeeHunt daugiausia dėmesio skiria prenumeratų ir atsiskaitymo signalams. Įtartinų mokėjimo, prisijungimo ir sukčiavimo tipo laiškų aptikimas yra produkto krypties dalis."]],
      start: ["Pradėkite dabar", "Pradėkite bandymą ir susigrąžinkite prenumeratų bei pašto kontrolę.", "Pradėti nemokamą bandymą", "Atsisiųsti Beta"],
    },
    pricing: {
      title: "Kainodara | FeeHunt",
      description: "Paprasta FeeHunt kainodara su Basic ir Family planais.",
      hero: ["Kainodara", "Paprasta kaina švaresnei pašto dėžutei ir mažiau pamirštų prenumeratų.", "Pradėkite nuo 7 dienų bandymo. Pasirinkite planą pagal Gmail paskyrų skaičių. Atšaukti galite bet kada.", "Kontrolė lieka jums: pradėkite nuo bandymo, peržiūrėkite planą ir atšaukite prieš mokamą laikotarpį.", "Pradėti bandymą", "Atnaujinti planą"],
      plans: [["Basic planas", "Tinka vienam žmogui, norinčiam peržiūrėti vieną Gmail paskyrą.", ["7 dienų bandymas", "1 Gmail paskyra", "1 licencijos raktas", "Prenumeratų aptikimas", "Mokėjimų kontrolė", "Reklaminio pašto tvarkymas", "Vietinis apdorojimas", "Galima atšaukti bet kada"], "Pradėti Basic bandymą", "Valdyti prenumeratą"], ["Family planas", "Tinka šeimai arba kelioms Gmail paskyroms su vienu licencijos raktu.", ["7 dienų bandymas", "Iki 3 Gmail paskyrų", "1 licencijos raktas", "Prenumeratų aptikimas", "Mokėjimų kontrolė", "Reklaminio pašto tvarkymas", "Vietinis apdorojimas", "Galima atšaukti bet kada"], "Pradėti Family bandymą", "Valdyti prenumeratą"]],
      pricePeriod: "/mėn.",
      faqHeading: ["Atsiskaitymo DUK", "Aiški kaina ir aiškus atšaukimas."],
      faq: [["Ar yra nemokamas bandymas?", "Taip. Basic ir Family planai turi 7 dienų bandymą."], ["Kada būsiu apmokestintas?", "Po 7 dienų bandymo pasirinktas planas taps aktyvus, nebent atšauksite prieš pabaigą."], ["Ar galiu atšaukti bet kada?", "Taip. Prenumerata valdoma per Stripe Billing Portal."], ["Ar yra paslėptų mokesčių?", "Ne. FeeHunt naudoja paprastą mėnesinę kainodarą."], ["Ar galėsiu keisti planą?", "Taip. Plano keitimas ir atsiskaitymo savitarna vyksta klientų portale."]],
    },
    signup: {
      title: "Pradėti bandymą | FeeHunt",
      description: "Sukurkite FeeHunt paskyrą ir pradėkite 7 dienų bandymą.",
      hero: { eyebrow: "7 dienų nemokamas bandymas", title: "Gaukite FeeHunt raktą.", lead: "Įveskite el. paštą — atsiųsime jūsų FeeHunt raktą, kad galėtumėte aktyvuoti Windows programą. Kortelės nereikia." },
      form: { email: "Gmail arba el. pašto adresas", plan: "Planas", planTrial: "7 dienų nemokamas bandymas - 1 Gmail paskyra", planBasic: "Basic - 1 Gmail paskyra", planFamily: "Family - iki 3 Gmail paskyrų", submit: "Atsiųsti FeeHunt raktą", note: "Kortelės nereikia. FeeHunt licencijų serveryje nesaugo Gmail laiškų turinio." },
      footer: { haveKey: "Jau turite raktą? <a class=\"text-link\" href=\"login.html\">Aktyvuokite jį prisijungimo puslapyje</a>." },
    },
    success: {
      title: "Mokėjimas sėkmingas | FeeHunt",
      description: "FeeHunt mokėjimas sėkmingas.",
      hero: ["Mokėjimas sėkmingas", "Jūsų FeeHunt planas aktyvuojamas.", "Stripe patvirtino mokėjimą. FeeHunt atsiųs licencijos raktą į el. paštą, naudotą mokėjimui.", "Jei laiškas neateina per kelias minutes, naudokite Prisijungti / Siųsti raktą dar kartą.", "Atsisiųsti FeeHunt", "Siųsti raktą dar kartą"],
      cards: [
        ["Kas toliau", ["Patikrinkite el. paštą dėl FeeHunt licencijos rakto.", "Atsisiųskite arba atidarykite FeeHunt Windows programoje.", "Įklijuokite raktą programoje.", "Gmail prijunkite tik tada, kai būsite pasiruošę."]],
        ["Kiti žingsniai", ["Patikrinkite el. paštą, naudotą Stripe mokėjimui.", "Atsisiųskite arba atidarykite FeeHunt Windows programoje.", "Įklijuokite licencijos raktą programoje.", "Gmail prijunkite tik tada, kai būsite pasiruošę."]],
      ],
    },
    account: {
      title: "Valdyti prenumeratą | FeeHunt",
      description: "Valdykite arba atšaukite FeeHunt prenumeratą.",
      hero: ["Paskyra", "Valdykite FeeHunt prenumeratą.", "Įklijuokite FeeHunt licencijos raktą, kad saugiai atidarytumėte Stripe Billing Portal. FeeHunt čia neprašo kortelės duomenų.", "Atšaukimas ir atsiskaitymo keitimai vyksta per Stripe. Gmail duomenys lieka jūsų kompiuteryje."],
      form: ["FeeHunt licencijos raktas", "Valdyti / atšaukti prenumeratą", "Reikia rakto dar kartą?", "Siųsti licencijos raktą dar kartą"],
    },
    download: {
      title: "Atsisiųsti FeeHunt | FeeHunt",
      description: "Atsisiųskite FeeHunt Windows kompiuteriui. Žingsnis po žingsnio pravesime per įdiegimą, įskaitant Windows saugumo įspėjimą, kurį pamatysite.",
      hero: {
        eyebrow: "Windows programa · 5 min. įdiegimas",
        title: "Atsisiųskite FeeHunt — pravesime per kiekvieną žingsnį.",
        lead: "FeeHunt yra nedidelė Windows programa. Įdiegimo metu pamatysite vieną Windows įspėjimą ir vieną Google įspėjimą — abu yra normalūs. Kiekvieną kartą pasakysime, ką spausti. Iš tiesų tai 5 minučių darbas.",
        button: "⬇ Atsisiųsti FeeHunt Windows kompiuteriui",
        meta: "Nemokamas 7 dienų bandymas · Kortelės nereikia · Veikia Windows 10 ir 11",
      },
      walk: {
        title: "Kas vyksta paspaudus atsisiųsti",
        s1: { title: "Pradės siųstis failas", body: "Naršyklė išsaugos FeeHunt-Setup-v1.12.7.exe į jūsų Atsisiuntimų (Downloads) aplanką. Tai nedidelis failas (~80 MB), atsisiunčia per maždaug 30 sekundžių." },
        s2: { title: "Du kartus spustelėkite atsisiųstą failą", body: "Atidarykite Atsisiuntimų aplanką ir dukart spustelėkite FeeHunt-Setup-v1.12.7.exe." },
        s3: {
          title: "Windows parodys mėlyną įspėjimą — tai normalu",
          body: "Ką pamatysite: mėlyną langą pavadinimu „Windows protected your PC“ su mažu mygtuku „Don't run“. Windows gali jį parodyti naujam arba dar nepasirašytam diegikliui, kol failas turi mažai atsisiuntimo reputacijos. FeeHunt kodo pasirašymas ruošiamas.",
          action: "<strong>Ką spausti:</strong> Paspauskite mažą nuorodą <em>„More info“</em> KAIRĖJE lango pusėje. Atsiras naujas mygtukas <em>„Run anyway“</em>. Paspauskite jį.",
        },
        s4: { title: "Pereikite per diegiklį (Next, Next, Install)", body: "Pasirodys įprastas Windows diegiklis. Trys trumpi ekranai, visi numatytieji nustatymai tinka: spauskite Next → Next → Install → Finish. FeeHunt atsidarys automatiškai." },
        s5: { title: "Įklijuokite licencijos raktą", body: "FeeHunt atsidarys jūsų naršyklėje adresu http://localhost:8501 — tai FeeHunt, veikiantis lokaliai jūsų kompiuteryje, ne svetainė. Įklijuokite FHUNT-XXXX-XXXX-XXXX-XXXX raktą iš laiško ir paspauskite Aktyvuoti." },
        s6: {
          title: "Paspauskite „Connect Gmail“",
          body: "Ką pamatysite: Google atidarys savo prisijungimo ir leidimų langą. Pasirinkite Gmail paskyrą, kurią norite peržiūrėti, perskaitykite prašomus leidimus ir tęskite tik jei sutinkate juos suteikti.",
          action: "<strong>Ką spausti:</strong> Sekite Google prisijungimo eigą ir patvirtinkite prašomus Gmail leidimus. Prieigą vėliau galite atšaukti Google paskyros nustatymuose.",
          trust: "🔒 FeeHunt niekada nemato ir nesaugo jūsų Gmail slaptažodžio. Oficiali Google OAuth sistema suteikia FeeHunt prieigos raktą, kurį bet kada galite atšaukti savo Google paskyros nustatymuose.",
        },
        s7: { title: "Baigta! Paspauskite „Skenuoti Gmail“ ir pamatykite, ką FeeHunt randa.", body: "Pirmas skenavimas trunka maždaug 1–2 minutes ir perskaito naujausius 200 laiškų. Niekas Gmail nekeičiama, kol nepatvirtinsite. Nuo šiol FeeHunt paleidžiate iš Start meniu kaip bet kurią kitą programą." },
        help: "Užstrigote kuriame nors žingsnyje? Parašykite <a href=\"mailto:support@feehunt.pro\">support@feehunt.pro</a> — paprastai atsakome per dieną.",
      },
      trust: {
        title: "Kodėl FeeHunt saugus",
        local: "<strong>Viskas vyksta jūsų kompiuteryje.</strong> Skenavimo rezultatai, nustatymai ir tokenai saugomi jūsų Windows vartotojo profilyje. Joks jūsų laiškų turinys nesiunčiamas į FeeHunt serverius.",
        password: "<strong>FeeHunt niekada nemato jūsų Gmail slaptažodžio.</strong> Google OAuth suteikia ribotą prieigos raktą; jūs patvirtinate per paties Google prisijungimo langą.",
        revoke: "<strong>Prieigą galite atšaukti bet kada.</strong> Atidarykite <a href=\"https://myaccount.google.com/permissions\" target=\"_blank\" rel=\"noopener\">Google paskyros leidimus</a> ir pašalinkite FeeHunt vienu paspaudimu.",
        read: "<strong>Kontrolė lieka jums.</strong> Gmail veiksmai — archyvavimas, trynimas, žymėjimas kaip šlamštas ar svarbus — paveikia tikrą Gmail paskyrą. Peržiūrėkite prieš veiksmą.",
      },
    },
    faqPage: {
      title: "DUK | FeeHunt",
      description: "Dažniausi klausimai apie FeeHunt.",
      hero: ["DUK", "Klausimai prieš išbandant FeeHunt?", "Aiškūs atsakymai apie privatumą, Gmail prieigą, bandymus, atšaukimą ir paskyrų limitus."],
      items: [["Kaip veikia FeeHunt?", "FeeHunt jungiasi prie Gmail per Google OAuth ir skenuoja naujausius laiškus ieškodamas prenumeratų, atnaujinimų, sąskaitų, nepavykusių mokėjimų, reklamų ir galimų sukčiavimo rizikų."], ["Ar mano el. paštas privatus?", "FeeHunt kuriamas kaip privatumą sauganti vietinė darbalaukio programa. Analizė vyksta jūsų kompiuteryje. FeeHunt neparduoda jūsų duomenų."], ["Ar galiu atšaukti bet kada?", "Taip. FeeHunt sukurtas su aiškiu prenumeratos valdymu ir atšaukimu."], ["Kokios Gmail paskyros palaikomos?", "FeeHunt sukurtas Gmail paskyroms, prijungtoms per Google OAuth. Beta laikotarpiu dėmesys skiriamas Gmail ir Windows."], ["Kas nutiks po nemokamo bandymo?", "Po 7 dienų bandymo pasirinktas mokamas planas taps aktyvus, nebent atšauksite iki bandymo pabaigos."], ["Kiek Gmail paskyrų galiu prijungti?", "Basic planas palaiko 1 Gmail paskyrą. Family planas palaiko iki 3 Gmail paskyrų."]],
    },
    contact: {
      title: "Kontaktai | FeeHunt",
      description: "Susisiekite su FeeHunt.",
      hero: ["Kontaktai", "Susisiekite su FeeHunt.", "Turite klausimą, klaidos pranešimą, produkto idėją ar verslo užklausą? Mums svarbu išgirsti."],
      left: ["Bendros užklausos", "El. paštas: ", "Beta atsiliepimams naudokite Feedback puslapį, kad galėtume greičiau surinkti struktūruotą informaciją.", "Siųsti atsiliepimą"],
      right: ["Ką įtraukti", ["Jūsų operacinę sistemą", "Ar naudojate beta ar viešą versiją", "Trumpą problemos ar klausimo aprašymą", "Ekrano kopijas tik jei jose nėra privataus el. pašto turinio"], "Nesiųskite privataus el. pašto turinio, OAuth tokenų, licencijos raktų ar jautrios paskyros informacijos."],
    },
    feedback: {
      title: "Atsiliepimai | FeeHunt",
      description: "Siųskite FeeHunt beta atsiliepimus.",
      hero: ["Atsiliepimai", "Padėkite formuoti FeeHunt.", "Beta atsiliepimai padeda gerinti aptikimo kokybę, atšaukimo srautus, įvedimą ir privatumą saugantį dizainą."],
      left: ["Ką siųsti", ["Klaidų pranešimus", "Neaiškius nustatymo žingsnius", "Neteisingai aptiktas prenumeratas", "Funkcijų idėjas", "Sėkmingo atšaukimo istorijas"]],
      right: ["Kontaktai", "Atsiliepimus siųskite: ", "Nesiųskite privataus el. pašto turinio, OAuth tokenų, licencijos raktų ar jautrios paskyros informacijos.", "Siųsti atsiliepimą"],
    },
    login: {
      title: "Aktyvuoti FeeHunt | FeeHunt",
      description: "Įklijuokite FeeHunt licencijos raktą. Patikrinsime ir parodysime, ką daryti toliau.",
      hero: { eyebrow: "Aktyvuoti FeeHunt", title: "Įklijuokite FeeHunt raktą.", lead: "FeeHunt yra Windows darbalaukio programa. Įklijuokite raktą žemiau — patikrinsime ar jis galioja ir tiksliai parodysime, ką daryti toliau." },
      form: { label: "FeeHunt licencijos raktas", submit: "Tikrinti raktą", hint: "Rakto formatas: FHUNT-XXXX-XXXX-XXXX-XXXX (gavote jį el. paštu po registracijos)." },
      help: {
        installed: "<strong>FeeHunt jau įdiegta?</strong> Atidarykite FeeHunt iš Windows Start meniu ir įklijuokite raktą pačioje programoje. Norėdami tame pačiame kompiuteryje naudoti kitą raktą, FeeHunt programoje pasirinkite <em>Prisijungti su kitu raktu</em>. Programos siųstis ir diegti iš naujo nereikia.",
        title: "Kur galiu užstrigti?",
        windows: "<strong>FeeHunt yra Windows darbalaukio programa.</strong> Ši svetainė tik patikrina raktą ir tvarko mokėjimus. Prenumeratų skenavimas vyksta FeeHunt programoje jūsų kompiuteryje.",
        email: "<strong>Negavote rakto į el. paštą?</strong> Patikrinkite šlamšto, reklamos ir naujienų aplankus. Galite atsiųsti dar kartą žemiau.",
        expired: "<strong>Bandymas pasibaigė?</strong> Atnaujinkite į Basic arba Family <a href=\"pricing.html\">kainodaros puslapyje</a>.",
        devices: "<strong>Pasiektas įrenginių limitas?</strong> Kiekvienas planas leidžia tik tam tikrą įrenginių skaičių. Susisiekite: <a href=\"mailto:support@feehunt.pro\">support@feehunt.pro</a>, atlaisvinsime vietą.",
      },
      resend: { kicker: "Pamiršote raktą?", title: "Atsiųsti raktą paštu", label: "El. paštas", submit: "Atsiųsti raktą" },
      footer: { signup: "Naujas FeeHunt vartotojas? <a class=\"text-link\" href=\"signup.html\">Pradėkite nemokamą 7 dienų bandymą</a>." },
    },
    privacy: {
      title: "Privatumo politika | FeeHunt",
      description: "FeeHunt privatumo politika.",
      hero: ["Privatumo politika", "Privatumas nuo pat pradžių.", "FeeHunt sukurtas remiantis vietiniu apdorojimu, minimaliu duomenų rinkimu ir vartotojo kontrole."],
      intro: ["Atnaujinta:", " 2026-07-01", "Ši privatumo politika įsigalioja nuo 2026 m. liepos 1 d."],
      sections: [["Apžvalga", ["FeeHunt yra privatumą sauganti darbalaukio programa, padedanti aptikti prenumeratas, finansinės rizikos laiškus, reklaminį triukšmą ir būsimas sukčiavimo rizikas."]], ["Vietinis apdorojimas", ["FeeHunt apdoroja Gmail skenavimo rezultatus vartotojo kompiuteryje. Analizė, rezultatai, nustatymai ir licencijos metaduomenys lieka vartotojo įrenginyje, nebent būsima funkcija aiškiai nurodytų kitaip."]], ["Gmail prieiga", ["FeeHunt naudoja Google OAuth prieigą. Vartotojas patvirtina prieigą per Google. FeeHunt neprašo ir nesaugo Gmail slaptažodžių."]], ["„Google“ vartotojo duomenys", ["FeeHunt per „Gmail OAuth“ pasiekia šiuos „Google“ vartotojo duomenis:", "„Gmail“ pranešimų metaduomenis ir turinį (tik skaitymo režimu), siekiant nustatyti su prenumeratomis susijusius laiškus, mokėjimų pranešimus ir reklaminį turinį.", "FeeHunt prašo tik būtiniausių OAuth leidimų: „Gmail“ skaitymo prieigos (https://www.googleapis.com/auth/gmail.readonly) ir „Gmail“ keitimo prieigos vartotojo inicijuotiems veiksmams (https://www.googleapis.com/auth/gmail.modify)."], "lead-list"], ["Duomenų dalijimasis ir atskleidimas", ["FeeHunt nesidalija, neperduoda, neparduoda ir neatskleidžia „Google“ vartotojo duomenų jokioms trečiosioms šalims. Visa „Gmail“ analizė atliekama vietiniame vartotojo įrenginyje. Joks el. laiškų turinys ar metaduomenys nėra perduodami į FeeHunt serverius."]], ["Duomenų apsauga ir saugumas", ["FeeHunt saugo jautrius „Google“ vartotojo duomenis (jūsų „Gmail“ laiškus ir metaduomenis) taikydama šiuos saugumo mechanizmus:", "Šifravimas perdavimo metu: visas ryšys su „Gmail“ API vyksta per šifruotą HTTPS/TLS ryšį.", "Šifravimas saugojimo metu: jūsų „Gmail“ OAuth tokenas įrenginyje saugomas užšifruotas naudojant operacinės sistemos šifravimo mechanizmą („Windows Data Protection API“, DPAPI); jis susietas su jūsų „Windows“ vartotojo paskyra, todėl kiti įrenginio vartotojai ar programos jo perskaityti negali.", "Tik vietinis apdorojimas: visa „Gmail“ analizė vyksta jūsų įrenginyje; laiškų turinys ir metaduomenys niekada neperduodami, nesaugomi ir neapdorojami FeeHunt serveriuose ar trečiųjų šalių sistemose.", "Minimalūs leidimai: FeeHunt prašo tik būtiniausių OAuth leidimų ir pasiekia jūsų „Gmail“ duomenis tik jūsų inicijuotiems veiksmams (skenavimui ir jūsų aiškiai patvirtintiems valymo veiksmams).", "Saugojimas ir trynimas: skenavimo rezultatai ir nustatymai lieka jūsų įrenginyje ir gali būti bet kada ištrinti; „Gmail“ prieigą galite bet kada atšaukti per „Google“ paskyrą, po to saugomas tokenas tampa nebenaudojamas.", "Ribotas naudojimas: FeeHunt naudojasi „Google“ API gauta informacija laikydamasis „Google API Services User Data Policy“ (https://developers.google.com/terms/api-services-user-data-policy), įskaitant „Limited Use“ reikalavimus."], "lead-list"], ["Vietoje saugomi duomenys", ["OAuth autorizacijos tokenas", "Skenavimo rezultatai", "Vartotojo nustatymai", "Valymo pasirinkimai", "Vietiniai licencijos metaduomenys"], "list"], ["Minimalus duomenų rinkimas", ["FeeHunt turėtų rinkti tik minimalius duomenis, reikalingus veikimui, licencijavimui, patikimumui ir klientų aptarnavimui."]], ["Duomenys neparduodami", ["FeeHunt neparduoda vartotojų duomenų ir neturėtų parduoti, nuomoti ar keistis Gmail duomenimis, rezultatais ar paskyros informacija."]], ["Mokėjimai ir licencijavimas", ["Viešo paleidimo licencijavimas ir mokėjimai gali reikalauti paskyros, atsiskaitymo ir licencijos duomenų. Mokėjimus turi tvarkyti patikimas tiekėjas, pvz., Stripe. FeeHunt neturėtų saugoti kortelių duomenų."]], ["Vartotojo kontrolė", ["Atšaukti Gmail prieigą per Google paskyrą", "Ištrinti vietinius FeeHunt failus iš kompiuterio", "Atšaukti mokamą prenumeratą per aiškų savitarnos kelią"], "list"], ["Kontaktai", ["Privatumo klausimais rašykite "]]],
    },
    terms: {
      title: "Naudojimo sąlygos | FeeHunt",
      description: "FeeHunt naudojimo sąlygos.",
      hero: ["Naudojimo sąlygos", "FeeHunt naudojimo sąlygos.", "Šios sąlygos aprašo produkto naudojimą, beta apribojimus, atsiskaitymo principus, atšaukimą ir vartotojo atsakomybę."],
      intro: ["Atnaujinta:", " 2026-07-01", "Šios naudojimo sąlygos įsigalioja nuo 2026 m. birželio 16 d."],
      sections: [["Sąlygų priėmimas", ["Naudodami FeeHunt sutinkate su šiomis naudojimo sąlygomis. Jei nesutinkate, produkto nenaudokite."]], ["Produkto aprašymas", ["FeeHunt yra darbalaukio programa, padedanti peržiūrėti Gmail ieškant prenumeratų, mokėjimų kontrolės laiškų, reklaminio triukšmo ir būsimų saugumo signalų.", "FeeHunt teikia aptikimo ir tvarkymo įrankius, bet negarantuoja, kad bus aptikta kiekviena prenumerata, mokėjimo problema, reklama ar sukčiavimo bandymas."]], ["Beta programinė įranga", ["FeeHunt beta versijose gali būti klaidų, nebaigtų funkcijų ir besikeičiančio veikimo. Prieš atlikdami Gmail veiksmus peržiūrėkite rezultatus atsakingai."]], ["Vartotojo atsakomybė", ["Peržiūrėti aptiktus laiškus prieš imantis veiksmų", "Suprasti, kad archyvavimas, trynimas, šlamšto žymėjimas ir kiti Gmail veiksmai paveikia tikrą paštą", "Išlaikyti prieigą prie savo Gmail paskyros", "Saugoti OAuth failus, tokenus, licencijos raktus ir vietinius duomenis"]], ["Gmail autorizacija", ["FeeHunt naudoja Google OAuth Gmail prieigai. Vartotojai gali atšaukti prieigą per Google paskyros nustatymus."]], ["Prenumeratos ir atsiskaitymas", ["Basic: €5.90/mėn.", "Family: €9.90/mėn.", "7 dienų nemokamas bandymas", "Atšaukti galima bet kada", "Mokamas atsiskaitymas turėtų būti taikomas tik tada, kai veikia checkout, klientų portalas ir atšaukimo srautai."]], ["Atšaukimas", ["Vartotojai turėtų galėti atšaukti mokamas prenumeratas per aiškų savitarnos kelią. Prieiga lieka aktyvi iki apmokėto laikotarpio pabaigos, nebent nurodyta kitaip."]], ["Draudžiamas naudojimas", ["FeeHunt negalima naudoti įstatymams pažeisti, piktnaudžiauti Gmail, trikdyti paslaugų veikimą, bandyti apeiti apsaugas ar siekti neteisėtos prieigos prie paskyrų ar infrastruktūros."]], ["Atsakomybės ribojimas", ["FeeHunt yra produktyvumo ir el. pašto peržiūros įrankis. FeeHunt neatsako už praleistas prenumeratas, praleistus mokėjimo įspėjimus, vartotojo sprendimus, trečiųjų šalių paslaugų pokyčius ar vartotojo inicijuotus Gmail veiksmus."]], ["Sąlygų pakeitimai", ["FeeHunt gali atnaujinti šias sąlygas prieš ir po viešo paleidimo. Tolimesnis naudojimas po pakeitimų reiškia atnaujintų sąlygų priėmimą."]], ["Kontaktai", ["Klausimais apie šias sąlygas rašykite "]]],
    },
  },
  no: {
    home: {
      heroScanCards: [["Gjentakende abonnement funnet", "Fornyelses- og fakturasignaler funnet"], ["Betalingsproblem funnet", "Mislykket belastning eller kortoppdatering"], ["Mistenkelig fakturaepost", "Se gjennom for du klikker pa lenker"], ["Reklamestoy samlet", "Nyhetsbrev og butikkmeldinger gruppert"]],
      visualPill: "Privat pa datamaskinen din",
      visualRows: [["Abonnementstilgang satt pa pause", "Betalingsproblem funnet i en fakturaepost", "Betalingskontroll"], ["Opprydding i nyhetsbrev og reklame", "Se gjennom avsendere for arkivering eller sletting", "Innboksopprydding"], ["Avbryt abonnement", "Apne beste faktura- eller avmeldingsvei", "Handling klar"]],
      featuresHeading: ["Funksjoner", "Bygget for abonnementsklarhet og innbokskontroll."],
      features: [["Skjulte abonnementer", "Finn gjentakende betalinger, fornyelser, fakturaer, prover og meldinger som er lette a overse."], ["Betalingskontroll", "Marker mislykkede betalinger, avviste kort, forfalte fakturaer, pauserte kontoer og varsler om abonnement."], ["Avmelding og kansellering", "Apne beste tilgjengelige avmelding, faktura-, konto- eller kanselleringsside uten a endre Gmail automatisk."], ["Gmail-opprydding", "Se gjennom reklame, nyhetsbrev, butikkmeldinger og innboksstoy med praktiske handlinger."], ["Phishing-signaler", "Fremtidige versjoner vil hjelpe med a flagge mistenkelige faktura-, innloggings- og phishing-monstre."]],
      plans: [["Basic", "For en Gmail-konto.", ["1 Gmail-konto", "1 lisensnokkel", "7 dagers proveperiode", "Avbryt nar som helst"], "Velg Basic"], ["Family", "For opptil tre Gmail-kontoer.", ["Opptil 3 Gmail-kontoer", "1 lisensnokkel", "7 dagers proveperiode", "Avbryt nar som helst"], "Velg Family"]],
      start: ["Start na", "Start proveperioden og ta kontroll over abonnementer og innboks.", "Start proveperiode", "Last ned Beta"],
    },
    faqPage: { items: [["Hvordan fungerer FeeHunt?", "FeeHunt kobler til Gmail via Google OAuth og skanner nye e-poster etter abonnementer, fornyelser, fakturaer, mislykkede betalinger, reklame og mulige phishing-risikoer."], ["Er e-posten min privat?", "FeeHunt er laget som en lokal personvernforst desktop-app. E-postanalyse skjer pa datamaskinen din. FeeHunt selger ikke dataene dine."], ["Kan jeg avbryte nar som helst?", "Ja. FeeHunt er bygget rundt tydelig avbestilling og abonnementsstyring."], ["Hvilke Gmail-kontoer stottes?", "FeeHunt er laget for Gmail-kontoer koblet til via Google OAuth. I beta fokuserer produktet pa Gmail og Windows."], ["Hva skjer etter proveperioden?", "Etter 7 dagers proveperiode blir valgt betalt plan aktiv med mindre du avbryter for perioden slutter."], ["Hvor mange Gmail-kontoer kan jeg koble til?", "Basic stotter 1 Gmail-konto. Family stotter opptil 3 Gmail-kontoer."]] },
    contact: { left: ["Generelle henvendelser", "E-post: ", "For beta-tilbakemeldinger, bruk Feedback-siden slik at vi kan samle strukturerte rapporter og forbedre produktet raskere.", "Send tilbakemelding"], right: ["Hva du bor ta med", ["Operativsystemet ditt", "Om du bruker beta eller offentlig versjon", "En kort beskrivelse av problemet eller sporsmalet", "Skjermbilder bare hvis de ikke inneholder privat e-postinnhold"], "Ikke send privat e-postinnhold, OAuth-token, lisensnokler eller sensitiv kontoinformasjon."] },
    feedback: { left: ["Hva du kan sende", ["Feilrapporter", "Uklare oppsettstrinn", "Feil abonnementstreff", "Funksjonsideer", "Historier om vellykket kansellering"]], right: ["Kontakt", "Send tilbakemelding til ", "Unnga privat e-postinnhold, OAuth-token, lisensnokler eller sensitiv kontoinformasjon.", "Send tilbakemelding"] },
  },
  es: {
    home: {
      heroScanCards: [["Suscripcion recurrente detectada", "Senales de renovacion y facturacion encontradas"], ["Problema de pago detectado", "Cargo fallido o email para actualizar tarjeta"], ["Email de facturacion sospechoso", "Revisa antes de hacer clic en enlaces"], ["Ruido promocional agrupado", "Newsletters y mensajes de tiendas agrupados"]],
      visualPill: "Privado en tu ordenador",
      visualRows: [["Acceso de suscripcion pausado", "Problema de pago detectado en un email de facturacion", "Control de pagos"], ["Limpieza de newsletters y promociones", "Revisa remitentes antes de archivar o eliminar", "Limpieza de bandeja"], ["Cancelar suscripcion", "Abrir la mejor ruta de facturacion o baja", "Accion lista"]],
      featuresHeading: ["Funciones", "Creado para claridad de suscripciones y control de la bandeja."],
      features: [["Deteccion de suscripciones ocultas", "Identifica pagos recurrentes, renovaciones, facturas, pruebas y mensajes faciles de pasar por alto."], ["Alertas de control de pagos", "Resalta pagos fallidos, tarjetas rechazadas, facturas vencidas, cuentas pausadas y avisos de suspension."], ["Baja y cancelacion", "Abre la mejor pagina de baja, facturacion, cuenta o cancelacion sin cambiar Gmail automaticamente."], ["Limpieza de Gmail", "Revisa promociones, newsletters, tiendas y ruido de bandeja con acciones practicas."], ["Senales de phishing", "Versiones futuras ayudaran a marcar patrones sospechosos de facturacion, inicio de sesion y phishing."]],
      plans: [["Basic", "Para una cuenta Gmail.", ["1 cuenta Gmail", "1 clave de licencia", "Prueba de 7 dias", "Cancelar cuando quieras"], "Elegir Basic"], ["Family", "Para hasta tres cuentas Gmail.", ["Hasta 3 cuentas Gmail", "1 clave de licencia", "Prueba de 7 dias", "Cancelar cuando quieras"], "Elegir Family"]],
      start: ["Empieza ahora", "Inicia tu prueba y toma control de tus suscripciones y bandeja.", "Iniciar prueba", "Descargar Beta"],
    },
    faqPage: { items: [["Como funciona FeeHunt?", "FeeHunt se conecta a Gmail mediante Google OAuth y escanea emails recientes para suscripciones, renovaciones, facturas, pagos fallidos, promociones y posibles riesgos de phishing."], ["Mi email es privado?", "FeeHunt esta disenado como app local de escritorio con privacidad primero. El analisis ocurre en tu ordenador. FeeHunt no vende tus datos."], ["Puedo cancelar cuando quiera?", "Si. FeeHunt esta pensado para una cancelacion clara y gestion de suscripcion."], ["Que cuentas Gmail son compatibles?", "FeeHunt esta creado para cuentas Gmail conectadas mediante Google OAuth. Durante beta se enfoca en Gmail y Windows."], ["Que pasa despues de la prueba gratis?", "Despues de la prueba de 7 dias, el plan elegido queda activo salvo que canceles antes de que termine."], ["Cuantas cuentas Gmail puedo conectar?", "Basic permite 1 cuenta Gmail. Family permite hasta 3 cuentas Gmail."]] },
    contact: { left: ["Consultas generales", "Email: ", "Para feedback beta, usa la pagina Feedback para que podamos recoger informes estructurados y mejorar mas rapido.", "Enviar feedback"], right: ["Que incluir", ["Tu sistema operativo", "Si usas beta o version publica", "Una breve descripcion del problema o pregunta", "Capturas solo si no contienen contenido privado de email"], "No envies contenido privado de email, tokens OAuth, claves de licencia ni informacion sensible de cuenta."] },
    feedback: { left: ["Que enviar", ["Informes de errores", "Pasos de configuracion confusos", "Detecciones falsas de suscripcion", "Ideas de funciones", "Historias de cancelacion exitosa"]], right: ["Contacto", "Envia feedback a ", "Evita enviar contenido privado de email, tokens OAuth, claves de licencia o informacion sensible.", "Enviar feedback"] },
  },
  de: {
    home: {
      heroScanCards: [["Wiederkehrendes Abo erkannt", "Verlangerungs- und Rechnungssignale gefunden"], ["Zahlungsproblem erkannt", "Fehlgeschlagene Abbuchung oder Kartenaktualisierung"], ["Verdachtige Rechnungs-E-Mail", "Vor dem Klicken auf Links prufen"], ["Werbechaos gebundelt", "Newsletter und Shop-Nachrichten gruppiert"]],
      visualPill: "Privat auf deinem Computer",
      visualRows: [["Abo-Zugriff pausiert", "Zahlungsproblem in Rechnungs-E-Mail erkannt", "Zahlungskontrolle"], ["Newsletter- und Werbeaufraumen", "Absender vor Archivieren oder Loschen prufen", "Postfach aufraumen"], ["Abo kundigen", "Besten Rechnungs- oder Abmeldeweg offnen", "Aktion bereit"]],
      featuresHeading: ["Funktionen", "Gebaut fur Abo-Klarheit und Postfachkontrolle."],
      features: [["Versteckte Abos erkennen", "Erkennt wiederkehrende Zahlungen, Verlangerungen, Rechnungen, Testphasen und leicht ubersehene Nachrichten."], ["Zahlungskontrolle", "Hebt fehlgeschlagene Zahlungen, abgelehnte Karten, fallige Rechnungen, pausierte Konten und Sperrhinweise hervor."], ["Abmelden und kundigen", "Offnet die beste Abmelde-, Rechnungs-, Konto- oder Kundigungsseite, ohne Gmail automatisch zu andern."], ["Gmail aufraumen", "Prufe Werbung, Newsletter, Shop-Nachrichten und Postfachchaos mit praktischen Aktionen."], ["Phishing-Signale", "Kunftige Versionen helfen, verdachtige Rechnungs-, Login- und Phishing-Muster zu markieren."]],
      plans: [["Basic", "Fur ein Gmail-Konto.", ["1 Gmail-Konto", "1 Lizenzschlussel", "7 Tage Testphase", "Jederzeit kundbar"], "Basic wahlen"], ["Family", "Fur bis zu drei Gmail-Konten.", ["Bis zu 3 Gmail-Konten", "1 Lizenzschlussel", "7 Tage Testphase", "Jederzeit kundbar"], "Family wahlen"]],
      start: ["Jetzt starten", "Starte deine Testphase und ubernimm Kontrolle uber Abos und Postfach.", "Test starten", "Beta herunterladen"],
    },
    faqPage: { items: [["Wie funktioniert FeeHunt?", "FeeHunt verbindet sich uber Google OAuth mit Gmail und scannt aktuelle E-Mails nach Abos, Verlangerungen, Rechnungen, fehlgeschlagenen Zahlungen, Werbung und moglichen Phishing-Risiken."], ["Ist meine E-Mail privat?", "FeeHunt ist eine lokale Desktop-App mit Datenschutz zuerst. Die Analyse findet auf deinem Computer statt. FeeHunt verkauft deine Daten nicht."], ["Kann ich jederzeit kundigen?", "Ja. FeeHunt ist auf klare Kundigung und Abo-Verwaltung ausgelegt."], ["Welche Gmail-Konten werden unterstutzt?", "FeeHunt ist fur Gmail-Konten gedacht, die uber Google OAuth verbunden sind. In der Beta liegt der Fokus auf Gmail und Windows."], ["Was passiert nach der Testphase?", "Nach 7 Tagen wird der gewahlte bezahlte Plan aktiv, sofern du nicht vorher kundigst."], ["Wie viele Gmail-Konten kann ich verbinden?", "Basic unterstutzt 1 Gmail-Konto. Family unterstutzt bis zu 3 Gmail-Konten."]] },
    contact: { left: ["Allgemeine Anfragen", "E-Mail: ", "Fur Beta-Feedback nutze bitte die Feedback-Seite, damit wir strukturierte Berichte sammeln und schneller verbessern konnen.", "Feedback senden"], right: ["Was du angeben solltest", ["Dein Betriebssystem", "Ob du Beta oder offentliche Version nutzt", "Eine kurze Beschreibung des Problems oder der Frage", "Screenshots nur ohne private E-Mail-Inhalte"], "Bitte sende keine privaten E-Mail-Inhalte, OAuth-Tokens, Lizenzschlussel oder sensiblen Kontodaten."] },
    feedback: { left: ["Was senden", ["Fehlerberichte", "Unklare Einrichtungsschritte", "Falsche Abo-Erkennungen", "Funktionsideen", "Erfolgreiche Kundigungsberichte"]], right: ["Kontakt", "Feedback senden an ", "Bitte keine privaten E-Mail-Inhalte, OAuth-Tokens, Lizenzschlussel oder sensiblen Kontodaten senden.", "Feedback senden"] },
  },
  fr: {
    home: {
      heroScanCards: [["Abonnement recurrent detecte", "Signaux de renouvellement et facturation trouves"], ["Probleme de paiement detecte", "Echec de paiement ou email de mise a jour carte"], ["Email de facturation suspect", "Verifiez avant de cliquer sur un lien"], ["Bruit promotionnel groupe", "Newsletters et messages boutique regroupes"]],
      visualPill: "Prive sur votre ordinateur",
      visualRows: [["Acces abonnement suspendu", "Probleme de paiement detecte dans un email de facturation", "Controle des paiements"], ["Nettoyage newsletters et promotions", "Verifiez les expediteurs avant archivage ou suppression", "Nettoyage inbox"], ["Annuler abonnement", "Ouvrir le meilleur chemin facturation ou desabonnement", "Action prete"]],
      featuresHeading: ["Fonctions", "Concu pour clarifier les abonnements et controler la boite mail."],
      features: [["Detection d'abonnements caches", "Identifie paiements recurrents, renouvellements, factures, essais et messages faciles a manquer."], ["Alertes de paiement", "Signale paiements echoues, cartes refusees, factures en retard, comptes suspendus et avertissements."], ["Desabonnement et annulation", "Ouvre la meilleure page de desabonnement, facturation, compte ou annulation sans modifier Gmail automatiquement."], ["Nettoyage Gmail", "Revoyez promotions, newsletters, boutiques et bruit de boite mail avec des actions pratiques."], ["Signaux phishing", "Les futures versions aideront a signaler des modeles suspects de facturation, connexion et phishing."]],
      plans: [["Basic", "Pour un compte Gmail.", ["1 compte Gmail", "1 cle de licence", "Essai de 7 jours", "Annulation a tout moment"], "Choisir Basic"], ["Family", "Pour jusqu'a trois comptes Gmail.", ["Jusqu'a 3 comptes Gmail", "1 cle de licence", "Essai de 7 jours", "Annulation a tout moment"], "Choisir Family"]],
      start: ["Commencer", "Demarrez votre essai et reprenez le controle des abonnements et de la boite mail.", "Demarrer l'essai", "Telecharger Beta"],
    },
    faqPage: { items: [["Comment fonctionne FeeHunt ?", "FeeHunt se connecte a Gmail via Google OAuth et analyse les emails recents pour abonnements, renouvellements, factures, paiements echoues, promotions et risques phishing possibles."], ["Mon email est-il prive ?", "FeeHunt est une application locale concue pour la confidentialite. L'analyse se fait sur votre ordinateur. FeeHunt ne vend pas vos donnees."], ["Puis-je annuler a tout moment ?", "Oui. FeeHunt est concu autour d'une annulation claire et de la gestion d'abonnement."], ["Quels comptes Gmail sont pris en charge ?", "FeeHunt est concu pour les comptes Gmail connectes via Google OAuth. Pendant la beta, le produit se concentre sur Gmail et Windows."], ["Que se passe-t-il apres l'essai gratuit ?", "Apres les 7 jours d'essai, le plan payant choisi devient actif sauf annulation avant la fin."], ["Combien de comptes Gmail puis-je connecter ?", "Basic prend en charge 1 compte Gmail. Family prend en charge jusqu'a 3 comptes Gmail."]] },
    contact: { left: ["Demandes generales", "Email : ", "Pour les retours beta, utilisez la page Feedback afin de nous aider a collecter des rapports structures et ameliorer plus vite.", "Envoyer un retour"], right: ["A inclure", ["Votre systeme d'exploitation", "Si vous utilisez la beta ou la version publique", "Une courte description du probleme ou de la question", "Captures uniquement sans contenu email prive"], "N'envoyez pas de contenu email prive, jetons OAuth, cles de licence ou informations sensibles."] },
    feedback: { left: ["Quoi envoyer", ["Rapports de bugs", "Etapes de configuration confuses", "Fausses detections d'abonnement", "Idees de fonctions", "Histoires d'annulation reussie"]], right: ["Contact", "Envoyer les retours a ", "Evitez d'envoyer du contenu email prive, des jetons OAuth, des cles de licence ou des informations sensibles.", "Envoyer un retour"] },
  },
};

Object.entries(FH_FINAL_TRANSLATION_PATCHES).forEach(([code, overrides]) => {
  mergeTranslation(FH_I18N[code], overrides);
});

function detectBrowserLanguage() {
  // First visit (no saved choice): match the browser's preferred language
  // to a supported site language. Norwegian comes through as nb/nn/no.
  // Everyone unmatched falls back to English.
  try {
    const prefs = navigator.languages && navigator.languages.length
      ? navigator.languages
      : [navigator.language || ""];
    for (const pref of prefs) {
      const code = String(pref || "").toLowerCase().slice(0, 2);
      if (code === "nb" || code === "nn" || code === "no") return "no";
      if (FH_I18N[code]) return code;
    }
  } catch (_error) {
    // navigator may be unavailable; fall through to English.
  }
  return "en";
}

function language() {
  try {
    const stored = window.localStorage.getItem(FH_I18N_KEY);
    if (stored && FH_I18N[stored]) return stored;
    return detectBrowserLanguage();
  } catch (_error) {
    return "en";
  }
}

function saveLanguage(code) {
  try {
    window.localStorage.setItem(FH_I18N_KEY, code);
  } catch (_error) {
    // Browsing still works without persisted language.
  }
}

function textBundle() {
  const current = language();
  return { current, text: FH_I18N[current] || FH_I18N.en, fallback: FH_I18N.en };
}

function value(path, source, fallback) {
  return path.split(".").reduce((acc, key) => acc?.[key], source) ??
    path.split(".").reduce((acc, key) => acc?.[key], fallback);
}

function setText(selector, text) {
  const element = document.querySelector(selector);
  if (element && text != null) element.textContent = text;
}

function setAttr(selector, attr, text) {
  const element = document.querySelector(selector);
  if (element && text != null) element.setAttribute(attr, text);
}

function setAll(selector, values) {
  document.querySelectorAll(selector).forEach((element, index) => {
    if (values[index] != null) element.textContent = values[index];
  });
}

function setList(list, values) {
  list?.querySelectorAll("li").forEach((item, index) => {
    if (values[index] != null) item.textContent = values[index];
  });
}

function ensureLanguageMenu() {
  document.querySelectorAll(".language-menu").forEach((menu) => {
    const dropdown = menu.querySelector(".language-dropdown");
    if (!dropdown) return;
    Object.entries(FH_LANGUAGES).forEach(([code, label]) => {
      if (!dropdown.querySelector(`[data-language="${code}"]`)) {
        const button = document.createElement("button");
        button.type = "button";
        button.setAttribute("data-language", code);
        button.textContent = label;
        dropdown.append(button);
      }
    });
  });
}

function applyCommon(text, current) {
  document.documentElement.lang = current;
  setText(".menu-button", text.common.menu);
  document.querySelectorAll(".language-toggle").forEach((toggle) => {
    toggle.innerHTML = `${FH_LANGUAGES[current]} <span>▼</span>`;
  });
  document.querySelectorAll(".nav-links a").forEach((link) => {
    const href = link.getAttribute("href") || "";
    const index = ["index.html", "pricing.html", "download.html", "faq.html", "privacy.html", "terms.html", "contact.html", "login.html"].indexOf(href);
    if (index >= 0) link.textContent = text.common.nav[index];
    if (text.common.navExtra?.[href]) link.textContent = text.common.navExtra[href];
  });
  document.querySelectorAll(".nav-actions a").forEach((link) => {
    const href = link.getAttribute("href") || "";
    if (href.includes("download")) link.textContent = text.common.download;
    if (href.includes("signup")) link.textContent = text.common.startTrial;
  });
  setAll(".footer-links a", text.common.footer);
}

function applyHome(text) {
  const home = text.home;
  if (!home) return;
  document.title = home.title;
  setAttr('meta[name="description"]', "content", home.description);
  setText(".hero .eyebrow", home.heroEyebrow);
  setText(".hero h1", home.heroHeading);
  highlightHeroHeading();
  setText(".hero .lead", home.heroLead);
  setAll(".hero-actions .button", home.heroButtons);
  setText(".product-principle", home.principle);
  document.querySelectorAll(".trust-row .badge").forEach((badge, index) => {
    const label = home.badges[index];
    if (label == null) return;
    const title = badge.querySelector("strong");
    if (title) title.textContent = label;
    else badge.textContent = label;
    const detail = home.badgeDetails?.[index];
    const note = badge.querySelector("small");
    if (note && detail != null) note.textContent = detail;
  });
  applyHeroScannerText(home.heroScanCards);
  if (Array.isArray(home.securityStrip)) {
    document.querySelectorAll(".hero-security-strip > div").forEach((cell, index) => {
      const entry = home.securityStrip[index];
      if (!entry) return;
      setTextFrom(cell, "strong", entry[0]);
      setTextFrom(cell, "small", entry[1]);
    });
  }
  if (typeof home.socialProof === "string") {
    setText(".hero-social-proof", home.socialProof);
  }
  const headings = document.querySelectorAll(".section-heading");
  const why = headings[0];
  if (why) {
    setTextFrom(why, ".eyebrow", home.why[0]);
    setTextFrom(why, "h2", home.why[1]);
    setTextFrom(why, ".lead", home.why[2]);
    setTextFrom(why, ".notice", home.why[3]);
  }
  setText(".visual-toolbar strong", home.visualToolbar);
  setText(".visual-pill", home.visualPill);
  document.querySelectorAll(".visual-row").forEach((row, index) => {
    const item = home.visualRows[index];
    if (!item) return;
    setTextFrom(row, "strong", item[0]);
    setTextFrom(row, "span:not(.status)", item[1]);
    setTextFrom(row, ".status", item[2]);
  });
  const featuresHeading = headings[1];
  if (featuresHeading) {
    setTextFrom(featuresHeading, ".eyebrow", home.featuresHeading[0]);
    setTextFrom(featuresHeading, "h2", home.featuresHeading[1]);
  }
  document.querySelectorAll(".grid.features .card").forEach((card, index) => {
    const item = home.features[index];
    if (!item) return;
    setTextFrom(card, "h3", item[0]);
    setTextFrom(card, "p", item[1]);
  });
  const pricingSection = document.querySelectorAll("main > .section")[2];
  if (pricingSection) {
    setTextFrom(pricingSection, ".section-heading .eyebrow", home.pricingHeading[0]);
    setTextFrom(pricingSection, ".section-heading h2", home.pricingHeading[1]);
    pricingSection.querySelectorAll(".grid.two .card").forEach((card, index) => {
      const plan = home.plans[index];
      if (!plan) return;
      setTextFrom(card, "h3", plan[0]);
      setTextFrom(card, "p:not(.plan-action)", plan[1]);
      setList(card.querySelector(".list"), plan[2]);
      setTextFrom(card, ".plan-action .button", plan[3]);
      setPriceFrom(card, index, home.pricePeriod || "/month");
    });
    setTextFrom(pricingSection, ".notice", home.pricingNotice);
  }
  const faqSection = document.querySelectorAll("main > .section")[3];
  if (faqSection && home.faqHeading && home.faq) {
    setTextFrom(faqSection, ".section-heading .eyebrow", home.faqHeading[0]);
    setTextFrom(faqSection, ".section-heading h2", home.faqHeading[1]);
    faqSection.querySelectorAll(".faq-item").forEach((item, index) => {
      const faq = home.faq[index];
      if (!faq) return;
      setTextFrom(item, "h3", faq[0]);
      setTextFrom(item, "p", faq[1]);
    });
  }
  const startSection = document.querySelectorAll("main > .section.band")[1];
  if (startSection) {
    setTextFrom(startSection, ".eyebrow", home.start[0]);
    setTextFrom(startSection, "h2", home.start[1]);
    setAllFrom(startSection, ".button", [home.start[2], home.start[3]]);
  }
}

function applyHeroScannerText(cards) {
  const fallbackCards = [["Recurring subscription detected", "Renewal and billing signals found"], ["Payment issue detected", "Failed charge or card update email"], ["Suspicious billing email", "Review before clicking any link"], ["Promotional clutter", "Newsletter and shop messages grouped"]];
  document.querySelectorAll(".hero-scan-card").forEach((card, index) => {
    const copy = (cards && cards[index]) || fallbackCards[index];
    if (!copy) return;
    setTextFrom(card, "strong", copy[0]);
    setTextFrom(card, "span:not(.scan-dot)", copy[1]);
  });
}

function highlightHeroHeading() {
  const heading = document.querySelector(".hero h1");
  if (!heading) return;
  const text = heading.textContent || "";
  const keywords = /^(subscriptions?|payment|email|prenumerat|mokej|mokėj|pinig|pašt|past)/i;
  heading.textContent = "";
  text.split(/(\s+)/).forEach((part) => {
    const span = document.createElement("span");
    span.textContent = part;
    if (keywords.test(part.normalize("NFC"))) {
      span.className = "hero-highlight";
    }
    heading.append(span);
  });
}

function setTextFrom(root, selector, text) {
  const element = root.querySelector(selector);
  if (element && text != null) element.textContent = text;
}

function setAllFrom(root, selector, values) {
  root.querySelectorAll(selector).forEach((element, index) => {
    if (values[index] != null) element.textContent = values[index];
  });
}

function setPriceFrom(root, index, period) {
  const price = root.querySelector(".price");
  if (!price) return;
  const amounts = ["\u20ac5.90", "\u20ac9.90"];
  const amount = amounts[index];
  if (!amount) return;
  const periodStyle = "font-size:1rem;font-weight:700;";
  price.innerHTML = "";
  price.append(document.createTextNode(amount));
  const periodElement = document.createElement("span");
  periodElement.style.cssText = periodStyle;
  periodElement.textContent = period;
  price.append(periodElement);
}

function applyPricing(text) {
  const page = text.pricing;
  if (!page) return;
  document.title = page.title;
  setAttr('meta[name="description"]', "content", page.description);
  setText(".page-hero .eyebrow", page.hero[0]);
  setText(".page-hero h1", page.hero[1]);
  setText(".page-hero .lead", page.hero[2]);
  setText(".page-hero .notice", page.hero[3]);
  setAll(".page-hero .button", [page.hero[4], page.hero[5]]);
  document.querySelectorAll(".section .grid.two > .card").forEach((card, index) => {
    const plan = page.plans[index];
    if (!plan) return;
    setTextFrom(card, "h2", plan[0]);
    setTextFrom(card, "p", plan[1]);
    setList(card.querySelector(".list"), plan[2]);
    setTextFrom(card, ".plan-action .button", plan[3]);
    setTextFrom(card, ".button.secondary", plan[4]);
    setPriceFrom(card, index, page.pricePeriod || "/month");
  });
  setText(".section.band .section-heading .eyebrow", page.faqHeading[0]);
  setText(".section.band .section-heading h2", page.faqHeading[1]);
  document.querySelectorAll(".section.band .faq-item").forEach((item, index) => {
    const faq = page.faq[index];
    if (!faq) return;
    setTextFrom(item, "h3", faq[0]);
    setTextFrom(item, "p", faq[1]);
  });
}

function applyDataI18n(text, pageKey) {
  const page = text[pageKey];
  if (!page) return;
  if (page.title) document.title = page.title;
  if (page.description) setAttr('meta[name="description"]', "content", page.description);

  document.querySelectorAll("[data-i18n], [data-i18n-html]").forEach((el) => {
    const useHtml = el.hasAttribute("data-i18n-html");
    const path = el.getAttribute("data-i18n") || el.getAttribute("data-i18n-html");
    if (!path) return;
    const value = path.split(".").reduce((acc, key) => acc?.[key], page);
    if (typeof value !== "string") return;
    if (useHtml) {
      el.innerHTML = value;
    } else {
      el.textContent = value;
    }
  });
}

function applySuccess(text) {
  const page = text.success;
  if (!page) return;
  document.title = page.title;
  setAttr('meta[name="description"]', "content", page.description);
  setText(".page-hero .eyebrow", page.hero[0]);
  setText(".page-hero h1", page.hero[1]);
  setText(".page-hero .lead", page.hero[2]);
  setText(".page-hero .notice", page.hero[3]);
  setAll(".page-hero .button", [page.hero[4], page.hero[5]]);
  document.querySelectorAll(".grid.two .card").forEach((card, index) => {
    const item = page.cards[index];
    if (!item) return;
    setTextFrom(card, "h2", item[0]);
    setList(card.querySelector(".list"), item[1]);
  });
}

function applyAccount(text) {
  const page = text.account;
  if (!page) return;
  document.title = page.title;
  setAttr('meta[name="description"]', "content", page.description);
  setText(".page-hero .eyebrow", page.hero[0]);
  setText(".page-hero h1", page.hero[1]);
  setText(".page-hero .lead", page.hero[2]);
  setText(".page-hero .notice", page.hero[3]);
  const form = document.querySelector("[data-portal-form]");
  if (form) {
    const label = form.querySelector("label");
    if (label) label.childNodes[0].textContent = `${page.form[0]}\n            `;
    setTextFrom(form, "button[type='submit']", page.form[1]);
  }
  const lead = document.querySelector(".small-lead");
  if (lead) {
    lead.childNodes[0].textContent = `${page.form[2]} `;
    const link = lead.querySelector("a");
    if (link) link.textContent = page.form[3];
  }
}

function applyDownload(text) {
  // The /download page now uses data-i18n / data-i18n-html attributes
  // (the step-by-step install walkthrough). The generic walker handles
  // it; languages without a download.walk bundle keep the English HTML.
  applyDataI18n(text, "download");
}

function applyFaqPage(text) {
  const page = text.faqPage;
  if (!page) return;
  document.title = page.title;
  setAttr('meta[name="description"]', "content", page.description);
  setText(".page-hero .eyebrow", page.hero[0]);
  setText(".page-hero h1", page.hero[1]);
  setText(".page-hero .lead", page.hero[2]);
  document.querySelectorAll(".faq-list .faq-item").forEach((item, index) => {
    const row = page.items[index];
    if (!row) return;
    setTextFrom(item, "h3", row[0]);
    setTextFrom(item, "p", row[1]);
  });
}

function applyContact(text) {
  const page = text.contact;
  if (!page) return;
  document.title = page.title;
  setAttr('meta[name="description"]', "content", page.description);
  setText(".page-hero .eyebrow", page.hero[0]);
  setText(".page-hero h1", page.hero[1]);
  setText(".page-hero .lead", page.hero[2]);
  const cards = document.querySelectorAll(".grid.two .card");
  if (cards[0]) {
    setTextFrom(cards[0], "h2", page.left[0]);
    const paragraphs = cards[0].querySelectorAll("p");
    if (paragraphs[0]) paragraphs[0].childNodes[0].textContent = page.left[1];
    if (paragraphs[1]) paragraphs[1].textContent = page.left[2];
    setTextFrom(cards[0], ".button", page.left[3]);
  }
  if (cards[1]) {
    setTextFrom(cards[1], "h2", page.right[0]);
    setList(cards[1].querySelector(".list"), page.right[1]);
    setTextFrom(cards[1], ".notice", page.right[2]);
  }
}

function applyFeedback(text) {
  const page = text.feedback;
  if (!page) return;
  document.title = page.title;
  setAttr('meta[name="description"]', "content", page.description);
  setText(".page-hero .eyebrow", page.hero[0]);
  setText(".page-hero h1", page.hero[1]);
  setText(".page-hero .lead", page.hero[2]);
  const cards = document.querySelectorAll(".grid.two .card");
  if (cards[0]) {
    setTextFrom(cards[0], "h2", page.left[0]);
    setList(cards[0].querySelector(".list"), page.left[1]);
  }
  if (cards[1]) {
    setTextFrom(cards[1], "h2", page.right[0]);
    const paragraph = cards[1].querySelector("p");
    if (paragraph) paragraph.childNodes[0].textContent = page.right[1];
    setTextFrom(cards[1], ".notice", page.right[2]);
    setTextFrom(cards[1], ".button", page.right[3]);
  }
}

function applyLegal(text, key) {
  const page = text[key];
  if (!page) return;
  document.title = page.title;
  setAttr('meta[name="description"]', "content", page.description);
  setText(".page-hero .eyebrow", page.hero[0]);
  setText(".page-hero h1", page.hero[1]);
  setText(".page-hero .lead", page.hero[2]);
  const legal = document.querySelector(".legal");
  if (!legal) return;
  legal.textContent = "";
  const updated = document.createElement("p");
  const strong = document.createElement("strong");
  strong.textContent = page.intro[0];
  updated.append(strong, document.createTextNode(page.intro[1]));
  const draft = document.createElement("p");
  draft.textContent = page.intro[2];
  legal.append(updated, draft);
  const usesMarkers = page.sections.some((section) => section.length >= 3);
  page.sections.forEach(([heading, rows, kind], index) => {
    const h2 = document.createElement("h2");
    h2.textContent = heading;
    legal.append(h2);
    const listSection = usesMarkers ? kind === "list" : (key === "privacy" ? [3, 7].includes(index) : [3].includes(index));
    if (listSection) {
      const list = document.createElement("ul");
      rows.forEach((row) => {
        const li = document.createElement("li");
        li.textContent = row;
        list.append(li);
      });
      legal.append(list);
      return;
    }
    if (kind === "lead-list") {
      const lead = document.createElement("p");
      lead.textContent = rows[0];
      const list = document.createElement("ul");
      rows.slice(1).forEach((row) => {
        const li = document.createElement("li");
        li.textContent = row;
        list.append(li);
      });
      legal.append(lead, list);
      return;
    }
    if (key === "terms" && index === 5) {
      const list = document.createElement("ul");
      rows.slice(0, 4).forEach((row) => {
        const li = document.createElement("li");
        li.textContent = row;
        list.append(li);
      });
      const p = document.createElement("p");
      p.textContent = rows[4];
      legal.append(list, p);
      return;
    }
    const isContactSection = index === page.sections.length - 1 && rows.length === 1 && rows[0].endsWith(" ");
    rows.forEach((row) => {
      const p = document.createElement("p");
      if (isContactSection) {
        p.append(document.createTextNode(row));
        const link = document.createElement("a");
        link.href = "mailto:support@feehunt.pro";
        link.textContent = "support@feehunt.pro";
        p.append(link, document.createTextNode("."));
      } else {
        p.textContent = row;
      }
      legal.append(p);
    });
  });
}

function applyPage() {
  ensureLanguageMenu();
  const { current, text } = textBundle();
  applyCommon(text, current);
  const page = document.body?.dataset.page || (document.body?.classList.contains("pricing-page") && "pricing") || "";
  if (page === "home") applyHome(text);
  if (page === "pricing") applyPricing(text);
  if (page === "signup") applyDataI18n(text, "signup");
  if (page === "login") applyDataI18n(text, "login");
  if (page === "success") applySuccess(text);
  if (page === "account") applyAccount(text);
  if (page === "download") applyDownload(text);
  if (page === "faq") applyFaqPage(text);
  if (page === "contact") applyContact(text);
  if (page === "feedback") applyFeedback(text);
  if (page === "privacy") applyLegal(text, "privacy");
  if (page === "terms") applyLegal(text, "terms");
}

document.addEventListener("click", (event) => {
  const option = event.target.closest?.("[data-language]");
  if (!option) return;
  const code = option.getAttribute("data-language");
  if (!FH_I18N[code]) return;
  saveLanguage(code);
  window.setTimeout(() => {
    applyPage();
    window.dispatchEvent(new CustomEvent("feehunt:language-changed", { detail: { language: code } }));
  }, 0);
});

applyPage();
