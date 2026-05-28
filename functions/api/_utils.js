const TRIAL_DAYS = 7;
const MAX_DEVICES = 3;
const LICENSE_PREFIX = "FHUNT";
const LICENSE_REGEX = /^FHUNT-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/;

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "GET, POST, OPTIONS",
      "access-control-allow-headers": "content-type, accept",
    },
  });
}

export function options() {
  return new Response(null, {
    status: 204,
    headers: {
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "GET, POST, OPTIONS",
      "access-control-allow-headers": "content-type, accept",
      "access-control-max-age": "86400",
    },
  });
}

export function normalizeEmail(email) {
  return String(email || "").trim().toLowerCase();
}

export function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function normalizePlan(plan) {
  const normalized = String(plan || "").trim().toLowerCase();
  if (normalized === "personal") return "basic";
  return ["trial", "basic", "family", "pro"].includes(normalized) ? normalized : "trial";
}

export function trialEndsAt() {
  return new Date(Date.now() + TRIAL_DAYS * 24 * 60 * 60 * 1000).toISOString();
}

export function daysRemaining(dateValue) {
  if (!dateValue) return 0;
  return Math.max(Math.ceil((new Date(dateValue).getTime() - Date.now()) / 86_400_000), 0);
}

export function isValidLicenseKey(key) {
  return LICENSE_REGEX.test(String(key || "").trim().toUpperCase());
}

export function generateLicenseKey() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  const segment = () => {
    const bytes = new Uint8Array(4);
    crypto.getRandomValues(bytes);
    return Array.from(bytes, (byte) => chars[byte % chars.length]).join("");
  };
  return `${LICENSE_PREFIX}-${segment()}-${segment()}-${segment()}-${segment()}`;
}

export function requireSupabase(env) {
  return Boolean(env.SUPABASE_URL && (env.SUPABASE_SERVICE_ROLE_KEY || env.SUPABASE_SERVICE_KEY));
}

export function supabaseHeaders(env, prefer = null) {
  const key = env.SUPABASE_SERVICE_ROLE_KEY || env.SUPABASE_SERVICE_KEY;
  const headers = {
    apikey: key,
    authorization: `Bearer ${key}`,
    "content-type": "application/json",
  };
  if (prefer) headers.prefer = prefer;
  return headers;
}

export async function supabaseSelect(env, table, query) {
  const url = `${env.SUPABASE_URL.replace(/\/$/, "")}/rest/v1/${table}?${query}`;
  const response = await fetch(url, { headers: supabaseHeaders(env) });
  const data = await response.json().catch(() => []);
  if (!response.ok) {
    throw new Error(data.message || data.error || `Supabase select failed: ${response.status}`);
  }
  return Array.isArray(data) ? data : [];
}

export async function supabaseInsert(env, table, payload) {
  const url = `${env.SUPABASE_URL.replace(/\/$/, "")}/rest/v1/${table}`;
  const response = await fetch(url, {
    method: "POST",
    headers: supabaseHeaders(env, "return=representation"),
    body: JSON.stringify(payload),
  });
  const data = await response.json().catch(() => []);
  if (!response.ok) {
    throw new Error(data.message || data.error || `Supabase insert failed: ${response.status}`);
  }
  return Array.isArray(data) ? data : [];
}

export async function supabaseUpdate(env, table, query, payload) {
  const url = `${env.SUPABASE_URL.replace(/\/$/, "")}/rest/v1/${table}?${query}`;
  const response = await fetch(url, {
    method: "PATCH",
    headers: supabaseHeaders(env, "return=representation"),
    body: JSON.stringify(payload),
  });
  const data = await response.json().catch(() => []);
  if (!response.ok) {
    throw new Error(data.message || data.error || `Supabase update failed: ${response.status}`);
  }
  return Array.isArray(data) ? data : [];
}

export async function sendLicenseEmail(env, email, licenseKey, plan, kind = "new") {
  if (!env.RESEND_API_KEY) {
    throw new Error("RESEND_API_KEY is not configured.");
  }

  const appUrl = env.FEEHUNT_APP_URL || "https://feehunt.pro";
  const downloadUrl = env.FEEHUNT_DOWNLOAD_URL || `${appUrl}/download`;
  const planLabel = plan === "family" ? "Family" : plan === "pro" ? "Pro" : plan === "basic" || plan === "personal" ? "Basic" : `${TRIAL_DAYS}-day free trial`;
  const isActivePlan = kind === "active";
  const subject = kind === "existing"
    ? "Your FeeHunt license key"
    : isActivePlan
      ? "Your FeeHunt plan is active"
      : `Welcome to FeeHunt - your ${TRIAL_DAYS}-day trial is ready`;
  const from = `"FeeHunt" <${env.EMAIL_FROM || "support@feehunt.pro"}>`;

  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      authorization: `Bearer ${env.RESEND_API_KEY}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      from,
      to: email,
      subject,
      html: `
        <div style="font-family:Arial,sans-serif;max-width:580px;margin:0 auto;padding:28px;background:#f6f7f4;color:#17211b">
          <h1 style="margin:0 0 8px;color:#16664f">FeeHunt</h1>
          <h2 style="margin:0 0 16px">${isActivePlan ? "Your FeeHunt plan is active" : `Your ${TRIAL_DAYS}-day free trial is ready`}</h2>
          <p style="line-height:1.5">${isActivePlan ? "Here is your license key. Follow the 5 steps below to start." : "No credit card required. Here is your license key — follow the 5 steps below to start."}</p>
          <div style="background:#fff;border:1px solid #dce4dd;border-radius:8px;padding:20px;text-align:center;margin:22px 0">
            <div style="font-size:12px;color:#5c6a61;text-transform:uppercase;font-weight:700">Your license key</div>
            <div style="font-family:Consolas,monospace;font-size:22px;color:#16664f;font-weight:800;letter-spacing:2px;word-break:break-all">${licenseKey}</div>
          </div>
          <p style="margin:0 0 6px"><strong>Plan:</strong> ${planLabel}${isActivePlan ? "" : `&nbsp;&nbsp;|&nbsp;&nbsp;<strong>Trial:</strong> ${TRIAL_DAYS} days`}</p>
          <h3 style="margin:24px 0 8px;color:#16664f">How to start — 5 steps</h3>
          <ol style="line-height:1.6;padding-left:20px;margin:0 0 8px">
            <li>Click <strong>Download FeeHunt</strong> below and run the file.</li>
            <li><strong>Windows will show a blue "Windows protected your PC" warning — this is normal for new beta apps.</strong> Click <em>"More info"</em> then <em>"Run anyway"</em>.</li>
            <li>Click through the installer (Next → Next → Install). FeeHunt opens automatically.</li>
            <li>Paste the license key above into FeeHunt and click Activate.</li>
            <li>Click <strong>Connect Gmail</strong>. Google shows a similar "app not verified" notice — click <em>Advanced → Go to FeeHunt</em>, then approve. FeeHunt never sees your password.</li>
          </ol>
          <p style="text-align:center;margin:26px 0">
            <a href="${downloadUrl}" style="background:#16664f;color:#fff;padding:12px 22px;border-radius:8px;text-decoration:none;font-weight:700">Download FeeHunt</a>
          </p>
          <p style="font-size:14px;line-height:1.5"><a href="${downloadUrl}" style="color:#16664f;font-weight:700">See the full install guide with pictures →</a><br>Stuck on any step? Just reply to this email or write to support@feehunt.pro.</p>
          <p style="font-size:13px;color:#5c6a61;border-top:1px solid #dce4dd;padding-top:14px;margin-top:20px">FeeHunt does not store Gmail contents on this licensing server. Gmail scan results stay on your computer.</p>
        </div>
      `,
    }),
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.message || data.error || `Resend failed: ${response.status}`);
  }
  return data;
}

export function accountSetupIssue() {
  return json({
    code: "account_setup_issue",
    error: "FeeHunt signup is not fully connected right now. Please try again in a moment.",
  }, 503);
}

export { TRIAL_DAYS, MAX_DEVICES };
