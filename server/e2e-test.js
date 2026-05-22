import "dotenv/config";

const API_BASE = process.env.FEEHUNT_E2E_API_BASE || "http://127.0.0.1:3001/api";
const EMAIL = process.env.FEEHUNT_E2E_EMAIL || `feehunt-test-${Date.now()}@example.com`;

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function postJson(path, body) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  const text = await response.text();
  let data = {};
  try {
    data = JSON.parse(text);
  } catch {
    data = { raw: text };
  }
  if (!response.ok) {
    throw new Error(`${path} failed: ${response.status} ${JSON.stringify(data)}`);
  }
  return data;
}

function requireEnv(name) {
  if (!process.env[name]) {
    throw new Error(`Missing ${name}. Copy .env.example to .env and fill it in.`);
  }
}

async function main() {
  requireEnv("SUPABASE_URL");
  if (!process.env.SUPABASE_SERVICE_ROLE_KEY && !process.env.SUPABASE_SERVICE_KEY) {
    throw new Error("Missing SUPABASE_SERVICE_ROLE_KEY. Copy .env.example to .env and fill it in.");
  }

  console.log(`[e2e] Registering trial for ${EMAIL}`);
  const register = await postJson("/register-trial", {
    email: EMAIL,
    plan: "basic",
  });
  console.log("[e2e] register-trial:", register.success ? "ok" : JSON.stringify(register));

  console.log("[e2e] Resending license key via login endpoint");
  const login = await postJson("/login", { email: EMAIL });
  console.log("[e2e] login/resend:", login.success ? "ok" : JSON.stringify(login));

  if (!login.license_key) {
    throw new Error("Login endpoint did not return license_key. Check server/server.js response and Supabase data.");
  }

  console.log("[e2e] Verifying license key");
  const verify = await postJson("/verify-license", {
    license_key: login.license_key,
    device_fingerprint: `e2e_${Date.now()}`,
    device_name: "FeeHunt E2E Test",
  });
  console.log("[e2e] verify-license:", verify.status);

  if (!["trial", "active"].includes(verify.status)) {
    throw new Error(`Expected trial or active license, got ${verify.status}`);
  }

  console.log("[e2e] SUCCESS");
  if (!process.env.RESEND_API_KEY && !process.env.SMTP_PASS) {
    console.log("[e2e] Email delivery was skipped because RESEND_API_KEY/SMTP_PASS is not configured.");
  } else {
    console.log("[e2e] Welcome/license email should have been sent by SMTP provider.");
  }
}

main().catch((error) => {
  console.error("[e2e] FAILED:", error.message);
  process.exitCode = 1;
});
