const nav = document.querySelector(".nav");
const menuButton = document.querySelector(".menu-button");
const languageMenus = document.querySelectorAll(".language-menu");

const KEY_REGEX = /^FHUNT-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/;

// Page-level i18n (hero/nav/footer/page bodies) is owned by i18n.js (FH_I18N).
// This map holds only the few runtime form-feedback strings that script.js shows
// after form submit; they are intentionally separate from the static page copy.
const runtimeMessages = {
  en: {
    registerSuccess: "Your trial has started. Check your email for the FeeHunt key, then activate it on the login page.",
    resendSuccess: "We sent your FeeHunt key to your email.",
    keyShape: "This does not look like a FeeHunt key. Expected format: FHUNT-XXXX-XXXX-XXXX-XXXX.",
    verifying: "Verifying your key...",
    statusActive: { title: "Your key is active.", body: "FeeHunt is ready to scan Gmail on your Windows computer." },
    statusTrial: { title: "Your trial key works.", body: "You can run FeeHunt on Windows during your free trial." },
    statusReadOnly: { title: "Your trial or subscription has ended.", body: "Upgrade your plan to keep using FeeHunt scans and cleanup." },
    statusPayment: { title: "Payment failed.", body: "Update your card in Stripe Billing Portal to keep your plan active." },
    statusDeviceLimit: { title: "Device limit reached.", body: "You have activated FeeHunt on the maximum number of devices allowed by your plan." },
    statusInvalid: { title: "We do not recognise this key.", body: "Check for typos, then resend the key by email or start a free trial." },
    statusError: { title: "We could not verify the key right now.", body: "Please try again in a moment. If it keeps failing, contact support." },
    planLabel: "Plan",
    daysLeft: (n) => `${n} day${n === 1 ? "" : "s"} remaining`,
    daysLeftZero: "Expired",
    deviceCount: (current, max) => `Devices: ${current ?? "?"} of ${max}`,
    openDesktop: "Open FeeHunt on your computer",
    downloadCta: "Download FeeHunt for Windows",
    upgradeCta: "Upgrade your plan",
    billingCta: "Manage billing in Stripe",
    contactCta: "Contact support",
    resendCta: "Resend by email",
    trialCta: "Start free trial",
  },
  lt: {
    registerSuccess: "Bandymas pradėtas. Patikrinkite el. paštą — atsiuntėme FeeHunt raktą. Po to grįžkite į prisijungimo puslapį ir aktyvuokite raktą.",
    resendSuccess: "Raktas išsiųstas į jūsų el. paštą.",
    keyShape: "Tai nepanašu į FeeHunt raktą. Laukiamas formatas: FHUNT-XXXX-XXXX-XXXX-XXXX.",
    verifying: "Tikriname raktą...",
    statusActive: { title: "Raktas galioja.", body: "FeeHunt paruoštas skenuoti Gmail jūsų Windows kompiuteryje." },
    statusTrial: { title: "Bandymo raktas veikia.", body: "Galite naudoti FeeHunt Windows kompiuteryje visą nemokamo bandymo laikotarpį." },
    statusReadOnly: { title: "Jūsų bandymas arba prenumerata pasibaigė.", body: "Atnaujinkite planą, kad galėtumėte tęsti skenavimus ir tvarkymus." },
    statusPayment: { title: "Nepavyko apmokėjimas.", body: "Atnaujinkite kortelę Stripe portale, kad planas vėl būtų aktyvus." },
    statusDeviceLimit: { title: "Pasiektas įrenginių limitas.", body: "Aktyvavote FeeHunt didžiausiame jūsų plane leidžiamame įrenginių skaičiuje." },
    statusInvalid: { title: "Tokio rakto neradome.", body: "Patikrinkite, ar nėra rašybos klaidos. Galite atsiųsti raktą paštu arba pradėti nemokamą bandymą." },
    statusError: { title: "Nepavyko patikrinti rakto.", body: "Pabandykite po akimirkos. Jei kartojasi — susisiekite su pagalba." },
    planLabel: "Planas",
    daysLeft: (n) => `Liko ${n} d.`,
    daysLeftZero: "Pasibaigė",
    deviceCount: (current, max) => `Įrenginiai: ${current ?? "?"} iš ${max}`,
    openDesktop: "Atidarykite FeeHunt savo kompiuteryje",
    downloadCta: "Atsisiųsti FeeHunt Windows",
    upgradeCta: "Atnaujinti planą",
    billingCta: "Tvarkyti mokėjimą Stripe",
    contactCta: "Susisiekti su pagalba",
    resendCta: "Atsiųsti paštu dar kartą",
    trialCta: "Pradėti nemokamą bandymą",
  },
  no: {
    resendSuccess: "Vi sendte FeeHunt-nøkkelen til e-posten din.", keyShape: "Dette ser ikke ut som en FeeHunt-nøkkel. Forventet format: FHUNT-XXXX-XXXX-XXXX-XXXX.", verifying: "Kontrollerer nøkkelen...",
    statusActive: { title: "Nøkkelen din er aktiv.", body: "FeeHunt er klar til å skanne Gmail på Windows-datamaskinen din." },
    statusTrial: { title: "Prøvenøkkelen din virker.", body: "Du kan bruke FeeHunt på Windows i den gratis prøveperioden." },
    statusReadOnly: { title: "Prøveperioden eller abonnementet er avsluttet.", body: "Oppgrader abonnementet for å fortsette å bruke FeeHunt." },
    statusPayment: { title: "Betalingen mislyktes.", body: "Oppdater kortet ditt i Stripe-portalen." },
    statusDeviceLimit: { title: "Enhetsgrensen er nådd.", body: "FeeHunt er aktivert på maksimalt antall enheter for abonnementet ditt." },
    statusInvalid: { title: "Vi kjenner ikke igjen denne nøkkelen.", body: "Kontroller nøkkelen og prøv igjen." },
    statusError: { title: "Vi kunne ikke kontrollere nøkkelen nå.", body: "Prøv igjen om et øyeblikk." },
    planLabel: "Abonnement", daysLeft: (n) => `${n} dag${n === 1 ? "" : "er"} igjen`, daysLeftZero: "Utløpt",
    deviceCount: (current, max) => `Enheter: ${current ?? "?"} av ${max}`,
    openDesktop: "Åpne FeeHunt på datamaskinen", downloadCta: "Last ned FeeHunt for Windows",
    upgradeCta: "Oppgrader abonnementet", billingCta: "Administrer betaling i Stripe",
    contactCta: "Kontakt kundestøtte", resendCta: "Send på nytt via e-post", trialCta: "Start gratis prøveperiode",
  },
  es: {
    resendSuccess: "Enviamos tu clave de FeeHunt por correo.", keyShape: "Esta no parece una clave de FeeHunt. Formato esperado: FHUNT-XXXX-XXXX-XXXX-XXXX.", verifying: "Verificando tu clave...",
    statusActive: { title: "Tu clave está activa.", body: "FeeHunt está listo para analizar Gmail en tu ordenador Windows." },
    statusTrial: { title: "Tu clave de prueba funciona.", body: "Puedes usar FeeHunt en Windows durante la prueba gratuita." },
    statusReadOnly: { title: "Tu prueba o suscripción ha terminado.", body: "Actualiza tu plan para seguir usando FeeHunt." },
    statusPayment: { title: "El pago ha fallado.", body: "Actualiza tu tarjeta en el portal de Stripe." },
    statusDeviceLimit: { title: "Se alcanzó el límite de dispositivos.", body: "Has activado FeeHunt en el número máximo de dispositivos permitido." },
    statusInvalid: { title: "No reconocemos esta clave.", body: "Comprueba la clave e inténtalo de nuevo." },
    statusError: { title: "No pudimos verificar la clave.", body: "Inténtalo de nuevo en unos instantes." },
    planLabel: "Plan", daysLeft: (n) => `${n} día${n === 1 ? "" : "s"} restante${n === 1 ? "" : "s"}`, daysLeftZero: "Caducado",
    deviceCount: (current, max) => `Dispositivos: ${current ?? "?"} de ${max}`,
    openDesktop: "Abrir FeeHunt en tu ordenador", downloadCta: "Descargar FeeHunt para Windows",
    upgradeCta: "Actualizar el plan", billingCta: "Gestionar pagos en Stripe",
    contactCta: "Contactar con soporte", resendCta: "Reenviar por correo", trialCta: "Iniciar prueba gratuita",
  },
  de: {
    resendSuccess: "Wir haben deinen FeeHunt-Schlüssel per E-Mail gesendet.", keyShape: "Dies sieht nicht wie ein FeeHunt-Schlüssel aus. Erwartetes Format: FHUNT-XXXX-XXXX-XXXX-XXXX.", verifying: "Schlüssel wird geprüft...",
    statusActive: { title: "Dein Schlüssel ist aktiv.", body: "FeeHunt kann Gmail jetzt auf deinem Windows-Computer prüfen." },
    statusTrial: { title: "Dein Testschlüssel funktioniert.", body: "Du kannst FeeHunt während der kostenlosen Testphase unter Windows verwenden." },
    statusReadOnly: { title: "Deine Testphase oder dein Abonnement ist beendet.", body: "Aktualisiere deinen Tarif, um FeeHunt weiter zu verwenden." },
    statusPayment: { title: "Zahlung fehlgeschlagen.", body: "Aktualisiere deine Karte im Stripe-Portal." },
    statusDeviceLimit: { title: "Gerätelimit erreicht.", body: "FeeHunt wurde auf der maximal zulässigen Anzahl von Geräten aktiviert." },
    statusInvalid: { title: "Wir erkennen diesen Schlüssel nicht.", body: "Prüfe den Schlüssel und versuche es erneut." },
    statusError: { title: "Der Schlüssel konnte nicht geprüft werden.", body: "Versuche es in einem Moment erneut." },
    planLabel: "Tarif", daysLeft: (n) => `${n} Tag${n === 1 ? "" : "e"} verbleibend`, daysLeftZero: "Abgelaufen",
    deviceCount: (current, max) => `Geräte: ${current ?? "?"} von ${max}`,
    openDesktop: "FeeHunt auf deinem Computer öffnen", downloadCta: "FeeHunt für Windows herunterladen",
    upgradeCta: "Tarif aktualisieren", billingCta: "Zahlung in Stripe verwalten",
    contactCta: "Support kontaktieren", resendCta: "Erneut per E-Mail senden", trialCta: "Kostenlose Testphase starten",
  },
  fr: {
    resendSuccess: "Nous avons envoyé votre clé FeeHunt par e-mail.", keyShape: "Cette clé ne ressemble pas à une clé FeeHunt. Format attendu : FHUNT-XXXX-XXXX-XXXX-XXXX.", verifying: "Vérification de votre clé...",
    statusActive: { title: "Votre clé est active.", body: "FeeHunt est prêt à analyser Gmail sur votre ordinateur Windows." },
    statusTrial: { title: "Votre clé d'essai fonctionne.", body: "Vous pouvez utiliser FeeHunt sous Windows pendant votre essai gratuit." },
    statusReadOnly: { title: "Votre essai ou abonnement est terminé.", body: "Mettez votre offre à niveau pour continuer à utiliser FeeHunt." },
    statusPayment: { title: "Le paiement a échoué.", body: "Mettez à jour votre carte dans le portail Stripe." },
    statusDeviceLimit: { title: "Limite d'appareils atteinte.", body: "Vous avez activé FeeHunt sur le nombre maximal d'appareils autorisé." },
    statusInvalid: { title: "Nous ne reconnaissons pas cette clé.", body: "Vérifiez la clé et réessayez." },
    statusError: { title: "Impossible de vérifier la clé.", body: "Réessayez dans quelques instants." },
    planLabel: "Offre", daysLeft: (n) => `${n} jour${n === 1 ? "" : "s"} restant${n === 1 ? "" : "s"}`, daysLeftZero: "Expiré",
    deviceCount: (current, max) => `Appareils : ${current ?? "?"} sur ${max}`,
    openDesktop: "Ouvrir FeeHunt sur votre ordinateur", downloadCta: "Télécharger FeeHunt pour Windows",
    upgradeCta: "Mettre l'offre à niveau", billingCta: "Gérer le paiement dans Stripe",
    contactCta: "Contacter le support", resendCta: "Renvoyer par e-mail", trialCta: "Démarrer l'essai gratuit",
  },
};

function getPreferredLanguage() {
  try {
    return window.localStorage.getItem("feehunt_site_language") || "en";
  } catch (_error) {
    return "en";
  }
}

function getRuntimeMessages() {
  return runtimeMessages[getPreferredLanguage()] || runtimeMessages.en;
}

function desktopOpenUrl() {
  return `feehunt://open?language=${encodeURIComponent(getPreferredLanguage())}`;
}

function setText(selector, value) {
  const element = document.querySelector(selector);
  if (element) {
    element.textContent = value;
  }
}

function startHeroScanner() {
  const cards = Array.from(document.querySelectorAll("[data-detect-card]"));
  if (!cards.length) return;
  cards.forEach((card) => card.classList.remove("is-detected"));
}

if (nav && menuButton) {
  menuButton.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
  });
}

languageMenus.forEach((menu) => {
  const toggle = menu.querySelector(".language-toggle");
  const options = menu.querySelectorAll("[data-language]");

  if (!toggle) {
    return;
  }

  toggle.addEventListener("click", (event) => {
    event.stopPropagation();
    const isOpen = menu.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  options.forEach((option) => {
    option.addEventListener("click", () => {
      menu.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
});

startHeroScanner();

function applySignupPlanFromUrl() {
  if (document.body?.dataset.page !== "signup") {
    return;
  }
  const plan = new URLSearchParams(window.location.search).get("plan");
  if (!["trial", "basic", "family"].includes(plan)) {
    return;
  }
  const planSelect = document.querySelector('form[data-api-form="register"] select[name="plan"]');
  if (planSelect) {
    planSelect.value = plan;
  }
}

function applyLoginKeyFromUrl() {
  if (document.body?.dataset.page !== "login") {
    return;
  }
  const params = new URLSearchParams(window.location.search);
  const key = (params.get("key") || "").trim().toUpperCase();
  if (!KEY_REGEX.test(key)) return;
  const input = document.querySelector('form[data-activate-form] input[name="license_key"]');
  if (input) {
    input.value = key;
  }
}

applySignupPlanFromUrl();
applyLoginKeyFromUrl();

document.addEventListener("click", () => {
  languageMenus.forEach((menu) => {
    menu.classList.remove("open");
    const toggle = menu.querySelector(".language-toggle");
    if (toggle) {
      toggle.setAttribute("aria-expanded", "false");
    }
  });
});

document.querySelectorAll("[data-checkout-plan]").forEach((button) => {
  button.addEventListener("click", async (event) => {
    event.preventDefault();
    const plan = button.getAttribute("data-checkout-plan");
    const originalText = button.textContent;
    button.setAttribute("aria-busy", "true");
    button.textContent = getPreferredLanguage() === "lt" ? "Atidaroma..." : "Opening...";
    try {
      const result = await postJson("/api/create-checkout", { plan, language: getPreferredLanguage() });
      if (!result.url) throw new Error("Missing Stripe Checkout URL.");
      window.location.href = result.url;
    } catch (error) {
      console.error("FeeHunt checkout flow failed", error);
      button.textContent = getPreferredLanguage() === "lt" ? "Bandykite dar kartą" : "Try again";
      window.setTimeout(() => {
        button.textContent = originalText;
        button.removeAttribute("aria-busy");
      }, 2500);
    }
  });
});

function showFormMessage(form, message, isError = false) {
  const target = form.querySelector(".form-message");
  if (!target) return;
  target.textContent = message;
  target.classList.toggle("error", isError);
  target.classList.toggle("success", !isError);
}

function friendlyApiError(error) {
  const message = String(error && error.message ? error.message : error || "");
  const lt = getPreferredLanguage() === "lt";
  if (message.includes("API_NOT_JSON") || message.includes("Unexpected token")) {
    return lt ? "Šiuo metu negalime susisiekti su FeeHunt serveriu. Jūsų duomenys neprarasti — pabandykite po akimirkos."
              : "FeeHunt could not reach the service right now. Your information was not lost. Please try again in a moment.";
  }
  if (message.includes("Failed to fetch") || message.includes("NetworkError") || message.includes("Load failed")) {
    return lt ? "Nepavyko prisijungti prie FeeHunt. Patikrinkite ryšį ir bandykite dar kartą."
              : "FeeHunt could not connect. Please check your connection and try again.";
  }
  if (message.includes("email_delivery_issue")) {
    return lt ? "Radome jūsų licenciją, bet šiuo metu nepavyko išsiųsti laiško. Pabandykite po akimirkos."
              : "FeeHunt found your license, but could not send the email right now. Please try again in a moment.";
  }
  if (message.includes("account_not_found")) {
    return lt ? "Tokio el. pašto FeeHunt sistemoje nerandame. Ar turbūt registravotės kitu adresu? Galite pradėti nemokamą bandymą."
              : "We could not find a FeeHunt account for this email. You can start a free trial instead.";
  }
  if (message.includes("invalid_email")) {
    return lt ? "Įveskite tinkamą el. pašto adresą." : "Please enter a valid email address.";
  }
  if (message.includes("account_setup_issue")) {
    return lt ? "FeeHunt servisas šiuo metu nepilnai sukonfigūruotas. Pabandykite po akimirkos."
              : "FeeHunt service is not fully configured right now. Please try again in a moment.";
  }
  return message || (lt ? "Nepavyko užbaigti veiksmo. Pabandykite po akimirkos." : "Something went wrong. Please try again in a moment.");
}

async function postJson(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(data),
  });
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    const text = await response.text().catch(() => "");
    console.error("FeeHunt API returned a non-JSON response", {
      url, status: response.status, contentType, preview: text.slice(0, 160),
    });
    throw new Error("API_NOT_JSON");
  }
  const body = await response.json().catch(() => ({}));
  if (!response.ok || body.ok === false) {
    const code = body.code ? `${body.code}: ` : "";
    throw new Error(code + (body.error || body.message || ""));
  }
  return body;
}

async function postJsonAllowError(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(data),
  });
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    throw new Error("API_NOT_JSON");
  }
  const body = await response.json().catch(() => ({}));
  return { http: response.status, body };
}

document.querySelectorAll("[data-api-form]").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const type = form.getAttribute("data-api-form");
    const data = Object.fromEntries(new FormData(form).entries());
    data.language = getPreferredLanguage();
    const button = form.querySelector("button[type='submit']");
    if (button) button.disabled = true;

    try {
      if (type === "register") {
        await postJson("/api/register-trial", data);
        renderSignupRoadmap(form, data.email || "");
      }
    } catch (error) {
      console.error("FeeHunt signup flow failed", error);
      showFormMessage(form, friendlyApiError(error), true);
    } finally {
      if (button) button.disabled = false;
    }
  });
});

// After a successful trial signup, replace the form with a clear numbered
// roadmap so the user knows exactly what to do next (the install funnel is
// where non-technical users get lost).
function renderSignupRoadmap(form, email) {
  const lt = getPreferredLanguage() === "lt";
  const safeEmail = escapeHtml(email);
  const copy = lt
    ? {
        title: "Patikrinkite el. paštą",
        sent: `Raktą išsiuntėme adresu <strong>${safeEmail}</strong>. Laiškas ateina per 1–2 min. (patikrinkite ir „Promotions" / „Spam" aplankus).`,
        stepsTitle: "Kas toliau — 5 paprasti žingsniai:",
        s1: "Atidarykite laišką iš FeeHunt ir nukopijuokite licencijos raktą",
        s2: "Atsisiųskite FeeHunt programą (mygtukas laiške arba žemiau)",
        s3: "Paleiskite ją — pravesime pro Windows įspėjimą",
        s4: "Įklijuokite raktą programoje",
        s5: "Prijunkite Gmail (paaiškiname, kodėl tai saugu)",
        download: "Atsisiųsti FeeHunt",
        guide: "Pilnas įdiegimo gidas su paveikslėliais →",
        help: "Užstrigote? Parašykite support@feehunt.pro",
      }
    : {
        title: "Check your email",
        sent: `We sent your key to <strong>${safeEmail}</strong>. It arrives in 1–2 min (check Promotions / Spam folders too).`,
        stepsTitle: "What's next — 5 simple steps:",
        s1: "Open the FeeHunt email and copy your license key",
        s2: "Download the FeeHunt app (button in the email, or below)",
        s3: "Run it — we walk you past the Windows warning",
        s4: "Paste your key inside the app",
        s5: "Connect Gmail (we explain why it's safe)",
        download: "Download FeeHunt",
        guide: "Full install guide with pictures →",
        help: "Stuck? Email support@feehunt.pro",
      };
  const card = document.createElement("div");
  card.className = "signup-roadmap";
  card.innerHTML = `
    <p class="roadmap-sent">✅ <strong>${copy.title}.</strong> ${copy.sent}</p>
    <p class="roadmap-steps-title">${copy.stepsTitle}</p>
    <ol class="roadmap-steps">
      <li>${copy.s1}</li>
      <li>${copy.s2}</li>
      <li>${copy.s3}</li>
      <li>${copy.s4}</li>
      <li>${copy.s5}</li>
    </ol>
    <div class="roadmap-actions">
      <a class="button primary" href="download.html">${copy.download}</a>
      <a class="text-link" href="download.html">${copy.guide}</a>
    </div>
    <p class="roadmap-help">${copy.help}</p>
  `;
  form.replaceWith(card);
  card.scrollIntoView({ behavior: "smooth", block: "start" });
}

// =========================================================
// Login page: paste-key + verify against /api/verify-license
// =========================================================

function statusPanelHtml(state) {
  const t = getRuntimeMessages();
  const variant = state.variant;
  const lines = [];
  if (state.plan) {
    lines.push(`<span class="status-chip"><strong>${t.planLabel}:</strong> ${escapeHtml(state.plan)}</span>`);
  }
  if (typeof state.daysRemaining === "number") {
    const label = state.daysRemaining <= 0 ? t.daysLeftZero : t.daysLeft(state.daysRemaining);
    lines.push(`<span class="status-chip">${label}</span>`);
  }
  if (state.deviceCount) {
    lines.push(`<span class="status-chip">${state.deviceCount}</span>`);
  }
  const chips = lines.length ? `<div class="status-chips">${lines.join("")}</div>` : "";
  const actions = (state.actions || []).map((action) =>
    `<a class="button ${action.primary ? "primary" : "secondary"}" href="${action.href}">${escapeHtml(action.label)}</a>`
  ).join("");
  return `
    <div class="status-panel-card status-${variant}">
      <p class="status-title">${escapeHtml(state.title)}</p>
      <p class="status-body">${escapeHtml(state.body)}</p>
      ${chips}
      ${actions ? `<div class="status-actions">${actions}</div>` : ""}
    </div>
  `;
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[ch]));
}

function renderStatusPanel(panel, state) {
  panel.innerHTML = statusPanelHtml(state);
  panel.hidden = false;
  panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

let lastVerifyResult = null;

window.addEventListener("feehunt:language-changed", () => {
  const panel = document.querySelector("[data-status-panel]");
  if (panel && lastVerifyResult) {
    renderStatusPanel(panel, stateFromVerifyResponse(lastVerifyResult.http, lastVerifyResult.body));
  }
});

function renderVerifyingPanel(panel) {
  const t = getRuntimeMessages();
  panel.innerHTML = `<div class="status-panel-card status-pending"><p class="status-title">${escapeHtml(t.verifying)}</p></div>`;
  panel.hidden = false;
}

function stateFromVerifyResponse(http, body) {
  const t = getRuntimeMessages();
  const status = String(body?.status || "").toLowerCase();
  const plan = body?.plan || null;
  const days = typeof body?.days_remaining === "number" ? body.days_remaining : null;

  if (status === "active") {
    return {
      variant: "ok",
      title: t.statusActive.title,
      body: t.statusActive.body,
      plan, daysRemaining: days,
      actions: [{ label: t.openDesktop, href: desktopOpenUrl(), primary: true }, { label: t.downloadCta, href: "download.html" }, { label: t.billingCta, href: "account.html" }],
    };
  }
  if (status === "trial") {
    return {
      variant: "ok",
      title: t.statusTrial.title,
      body: t.statusTrial.body,
      plan, daysRemaining: days,
      actions: [{ label: t.openDesktop, href: desktopOpenUrl(), primary: true }, { label: t.downloadCta, href: "download.html" }],
    };
  }
  if (status === "read_only") {
    return {
      variant: "warn",
      title: t.statusReadOnly.title,
      body: t.statusReadOnly.body,
      plan, daysRemaining: 0,
      actions: [{ label: t.upgradeCta, href: "pricing.html", primary: true }, { label: t.billingCta, href: "account.html" }],
    };
  }
  if (status === "payment_required") {
    return {
      variant: "warn",
      title: t.statusPayment.title,
      body: t.statusPayment.body,
      plan, daysRemaining: days,
      actions: [{ label: t.billingCta, href: "account.html", primary: true }],
    };
  }
  if (status === "device_limit") {
    const max = body?.max_devices ?? "?";
    const current = body?.current_devices ?? max;
    return {
      variant: "warn",
      title: t.statusDeviceLimit.title,
      body: t.statusDeviceLimit.body,
      deviceCount: t.deviceCount(current, max),
      actions: [{ label: t.contactCta, href: "contact.html", primary: true }],
    };
  }
  if (status === "invalid" || http === 404) {
    return {
      variant: "err",
      title: t.statusInvalid.title,
      body: t.statusInvalid.body,
      actions: [{ label: t.resendCta, href: "#resend", primary: true }, { label: t.trialCta, href: "signup.html" }],
    };
  }
  return {
    variant: "err",
    title: t.statusError.title,
    body: body?.error || body?.message || t.statusError.body,
    actions: [{ label: t.contactCta, href: "contact.html" }],
  };
}

document.querySelectorAll("[data-activate-form]").forEach((form) => {
  const panel = document.querySelector("[data-status-panel]");
  const input = form.querySelector("[name='license_key']");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const messages = getRuntimeMessages();
    const key = String(input?.value || "").trim().toUpperCase().replace(/\s+/g, "");
    if (input) input.value = key;

    if (!KEY_REGEX.test(key)) {
      if (panel) {
        renderStatusPanel(panel, {
          variant: "err",
          title: messages.statusInvalid.title,
          body: messages.keyShape,
          actions: [{ label: messages.resendCta, href: "#resend", primary: true }, { label: messages.trialCta, href: "signup.html" }],
        });
      }
      return;
    }

    const button = form.querySelector("button[type='submit']");
    if (button) button.disabled = true;
    if (panel) renderVerifyingPanel(panel);

    try {
      const { http, body } = await postJsonAllowError("/api/verify-license", { license_key: key, check_only: true });
      lastVerifyResult = { http, body };
      const state = stateFromVerifyResponse(http, body);
      if (panel) renderStatusPanel(panel, state);
    } catch (error) {
      console.error("FeeHunt verify failed", error);
      if (panel) {
        renderStatusPanel(panel, {
          variant: "err",
          title: messages.statusError.title,
          body: friendlyApiError(error),
          actions: [{ label: messages.contactCta, href: "contact.html" }],
        });
      }
    } finally {
      if (button) button.disabled = false;
    }
  });

  // Pre-validate format as the user types so they get instant feedback on shape.
  if (input) {
    input.addEventListener("input", () => {
      input.value = input.value.toUpperCase();
    });
  }
});

document.querySelectorAll("[data-resend-form]").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    data.language = getPreferredLanguage();
    const button = form.querySelector("button[type='submit']");
    if (button) button.disabled = true;
    try {
      const result = await postJson("/api/login", data);
      const messages = getRuntimeMessages();
      showFormMessage(form, result.message || messages.resendSuccess);
    } catch (error) {
      console.error("FeeHunt resend flow failed", error);
      showFormMessage(form, friendlyApiError(error), true);
    } finally {
      if (button) button.disabled = false;
    }
  });
});

document.querySelectorAll("[data-portal-form]").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const input = form.querySelector("[name='license_key']");
    const button = form.querySelector("button[type='submit']");
    const licenseKey = String(input?.value || "").trim().toUpperCase().replace(/\s+/g, "");
    if (input) input.value = licenseKey;
    if (button) {
      button.disabled = true;
      button.textContent = getPreferredLanguage() === "lt" ? "Atidaromas Stripe portalas..." : "Opening Stripe Portal...";
    }
    try {
      const result = await postJson("/api/create-portal-session", { license_key: licenseKey });
      if (!result.url) throw new Error("Missing Stripe Portal URL.");
      window.location.href = result.url;
    } catch (error) {
      console.error("FeeHunt portal flow failed", error);
      showFormMessage(form, friendlyApiError(error), true);
    } finally {
      if (button) {
        button.disabled = false;
        button.textContent = getPreferredLanguage() === "lt" ? "Valdyti / atšaukti prenumeratą" : "Manage / Cancel Subscription";
      }
    }
  });
});

// Smooth-scroll the #resend hash link straight to the resend form
if (document.body?.dataset.page === "login") {
  document.addEventListener("click", (event) => {
    const link = event.target.closest?.('a[href="#resend"]');
    if (!link) return;
    event.preventDefault();
    const resendForm = document.querySelector("[data-resend-form]");
    if (resendForm) {
      resendForm.scrollIntoView({ behavior: "smooth", block: "center" });
      const emailInput = resendForm.querySelector("input[name='email']");
      if (emailInput) emailInput.focus();
    }
  });
}
