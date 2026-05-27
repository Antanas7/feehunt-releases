import "dotenv/config";
import crypto from "crypto";
import path from "path";
import { fileURLToPath } from "url";
import express from "express";
import cors from "cors";
import nodemailer from "nodemailer";
import Stripe from "stripe";
import { createClient } from "@supabase/supabase-js";
import { createRateLimit, keyByIp, keyByLicenseBody } from "./middleware/rateLimit.js";

const PORT = Number(process.env.PORT || 3001);
const APP_URL = process.env.FEEHUNT_APP_URL || "https://feehunt.pro";
const DOWNLOAD_URL = process.env.FEEHUNT_DOWNLOAD_URL || `${APP_URL}/download`;
const TRIAL_DAYS = 7;
const MAX_DEVICES = 3;
const LICENSE_PREFIX = "FHUNT";
const LICENSE_REGEX = /^FHUNT-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/;
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SITE_DIR = path.resolve(__dirname, "../site");

const supabase = createClient(
  process.env.SUPABASE_URL || "",
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY || "",
);

const stripe = process.env.STRIPE_SECRET_KEY
  ? new Stripe(process.env.STRIPE_SECRET_KEY)
  : null;

const mailer = nodemailer.createTransport({
  host: process.env.SMTP_HOST || "smtp.resend.com",
  port: Number(process.env.SMTP_PORT || 465),
  secure: String(process.env.SMTP_SECURE || "true") === "true",
  auth: {
    user: process.env.SMTP_USER || "resend",
    pass: process.env.RESEND_API_KEY || process.env.SMTP_PASS || "",
  },
});

const app = express();

app.post("/api/webhook", express.raw({ type: "application/json" }), handleWebhook);
app.use(cors());
app.use(express.json({ limit: "1mb" }));
app.use(express.static(SITE_DIR, {
  extensions: ["html"],
  setHeaders: (res) => {
    res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate, proxy-revalidate");
  },
}));

const registerRateLimit = createRateLimit({ limit: 10, windowMs: 60_000, keyExtractor: keyByIp });
const verifyIpRateLimit = createRateLimit({ limit: 30, windowMs: 60_000, keyExtractor: keyByIp });
const verifyKeyRateLimit = createRateLimit({ limit: 10, windowMs: 60_000, keyExtractor: keyByLicenseBody });

function normalizeEmail(email) {
  return String(email || "").trim().toLowerCase();
}

function isSupabaseConfigured() {
  return Boolean(process.env.SUPABASE_URL && (process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY));
}

function requireSupabase(res) {
  if (isSupabaseConfigured()) return true;
  return res.status(503).json({
    code: "account_setup_issue",
    error: "FeeHunt account setup is not finished yet. Please contact support@feehunt.pro.",
    setup_error: "Missing Supabase server configuration.",
  });
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function normalizePlan(plan) {
  const normalized = String(plan || "").trim().toLowerCase();
  if (normalized === "personal") return "basic";
  return ["trial", "basic", "family", "pro"].includes(normalized) ? normalized : "trial";
}

function generateLicenseKey() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  const segment = () => Array.from({ length: 4 }, () => chars[crypto.randomInt(chars.length)]).join("");
  return `${LICENSE_PREFIX}-${segment()}-${segment()}-${segment()}-${segment()}`;
}

function trialEndsAt() {
  return new Date(Date.now() + TRIAL_DAYS * 24 * 60 * 60 * 1000).toISOString();
}

function daysRemaining(dateValue) {
  if (!dateValue) return 0;
  return Math.max(Math.ceil((new Date(dateValue).getTime() - Date.now()) / 86_400_000), 0);
}

function fromEmail() {
  return `"FeeHunt" <${process.env.EMAIL_FROM || "support@feehunt.pro"}>`;
}

async function sendMail(options) {
  if (!process.env.RESEND_API_KEY && !process.env.SMTP_PASS) {
    console.warn("[Email] SMTP credentials not configured; skipping email to", options.to);
    return { skipped: true };
  }
  return mailer.sendMail({ from: fromEmail(), ...options });
}

async function sendLicenseEmail(email, licenseKey, plan, kind = "new") {
  const planLabel = plan === "family" ? "Family" : plan === "pro" ? "Pro" : plan === "basic" || plan === "personal" ? "Basic" : `${TRIAL_DAYS}-day free trial`;
  const subject = kind === "existing"
    ? "Your FeeHunt license key"
    : `Welcome to FeeHunt - your ${TRIAL_DAYS}-day trial is ready`;

  return sendMail({
    to: email,
    subject,
    html: `
      <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;padding:28px;background:#f6f7f4;color:#17211b">
        <h1 style="margin:0 0 8px;color:#16664f">FeeHunt</h1>
        <h2 style="margin:0 0 16px">Your ${TRIAL_DAYS}-day free trial is ready</h2>
        <p>No credit card required. Install FeeHunt, paste this license key, connect Gmail, and scan for subscriptions.</p>
        <div style="background:#fff;border:1px solid #dce4dd;border-radius:8px;padding:20px;text-align:center;margin:22px 0">
          <div style="font-size:12px;color:#5c6a61;text-transform:uppercase;font-weight:700">Your license key</div>
          <div style="font-family:Consolas,monospace;font-size:22px;color:#16664f;font-weight:800;letter-spacing:2px;word-break:break-all">${licenseKey}</div>
        </div>
        <p><strong>Plan:</strong> ${planLabel}<br><strong>Trial:</strong> ${TRIAL_DAYS} days</p>
        <p style="text-align:center;margin:26px 0">
          <a href="${DOWNLOAD_URL}" style="background:#16664f;color:#fff;padding:12px 22px;border-radius:8px;text-decoration:none;font-weight:700">Download FeeHunt</a>
        </p>
        <p style="font-size:13px;color:#5c6a61">FeeHunt does not store Gmail contents on this licensing server. Gmail scan results stay on the user's computer.</p>
      </div>
    `,
  });
}

app.get("/api/health", async (_req, res) => {
  const checks = { api: "ok", supabase: "unknown" };

  try {
    await supabase.from("users").select("id").limit(1);
    checks.supabase = "ok";
  } catch (error) {
    checks.supabase = "error";
  }

  checks.email = process.env.RESEND_API_KEY || process.env.SMTP_PASS ? "configured" : "missing";

  res.json(checks);
});

async function handleRegisterTrial(req, res) {
  try {
    if (!requireSupabase(res)) return;

    const email = normalizeEmail(req.body.email);
    const plan = normalizePlan(req.body.plan);

    if (!isValidEmail(email)) {
      return res.status(400).json({ error: "Please enter a valid Gmail or email address." });
    }

    const { data: existing } = await supabase
      .from("users")
      .select("id")
      .eq("email", email)
      .maybeSingle();

    if (existing) {
      const { data: existingLicense } = await supabase
        .from("licenses")
        .select("*")
        .eq("user_id", existing.id)
        .maybeSingle();

      if (!existingLicense) {
        return res.status(409).json({ error: "Account exists, but no license was found. Please contact support." });
      }

      try {
        await sendLicenseEmail(email, existingLicense.license_key, existingLicense.plan || plan, "existing");
      } catch (emailError) {
        console.error("[Register] existing license email failed:", emailError.message);
        return res.status(502).json({
          code: "email_delivery_issue",
          error: "FeeHunt found your license, but could not send the email right now. Please try Log in / Resend key in a moment.",
        });
      }
      return res.json({
        success: true,
        message: "You already have a FeeHunt account. We sent your license key to your email again.",
        plan: existingLicense.plan,
        status: existingLicense.status,
        trial_days: TRIAL_DAYS,
      });
    }

    const licenseKey = generateLicenseKey();
    const endDate = trialEndsAt();

    const { data: userRows, error: userError } = await supabase
      .from("users")
      .insert({
        email,
        subscription_plan: plan,
        subscription_status: "trial",
        trial_ends_at: endDate,
      })
      .select("id");

    if (userError) {
      console.error("[Register] user insert failed:", userError.message);
      return res.status(500).json({
        code: "account_setup_issue",
        error: "FeeHunt could not create your account right now. Please try again in a moment.",
      });
    }

    const userId = userRows?.[0]?.id;
    const { error: licenseError } = await supabase.from("licenses").insert({
      license_key: licenseKey,
      user_id: userId,
      email,
      plan,
      billing: "monthly",
      status: "trial",
      devices_used: 0,
      devices_max: MAX_DEVICES,
    });

    if (licenseError) {
      console.error("[Register] license insert failed:", licenseError.message);
      return res.status(500).json({
        code: "license_creation_issue",
        error: "FeeHunt could not create your license key right now. Please try again in a moment.",
      });
    }

    try {
      await sendLicenseEmail(email, licenseKey, plan, "new");
    } catch (emailError) {
      console.error("[Register] license email failed:", emailError.message);
      return res.status(502).json({
        code: "email_delivery_issue",
        error: "FeeHunt created your trial, but could not send the license email right now. Please try Log in / Resend key in a moment.",
      });
    }

    return res.json({
      success: true,
      message: `Your ${TRIAL_DAYS}-day FeeHunt trial has started. We sent your license key to your email.`,
      trial_days: TRIAL_DAYS,
      plan,
      status: "trial",
    });
  } catch (error) {
    console.error("[Register] error:", error.message);
    return res.status(500).json({
      code: "server_connection_issue",
      error: "FeeHunt could not complete signup right now. Your information was not lost. Please try again in a moment.",
    });
  }
}

app.post("/api/register", registerRateLimit, handleRegisterTrial);
app.post("/api/register-trial", registerRateLimit, handleRegisterTrial);

app.post("/api/login", registerRateLimit, async (req, res) => {
  try {
    if (!requireSupabase(res)) return;

    const email = normalizeEmail(req.body.email);
    if (!isValidEmail(email)) {
      return res.status(400).json({ error: "Please enter your email address." });
    }

    const { data: user } = await supabase.from("users").select("id").eq("email", email).maybeSingle();
    if (!user) {
      return res.status(404).json({ error: "No FeeHunt account was found for this email." });
    }

    const { data: license } = await supabase.from("licenses").select("*").eq("user_id", user.id).maybeSingle();
    if (!license) {
      return res.status(404).json({ error: "No license was found. Please contact support." });
    }

    try {
      await sendLicenseEmail(email, license.license_key, license.plan || "personal", "existing");
    } catch (emailError) {
      console.error("[Login] email failed:", emailError.message);
      return res.status(502).json({
        code: "email_delivery_issue",
        error: "FeeHunt found your license, but could not send the email right now. Please try again in a moment.",
      });
    }
    return res.json({
      success: true,
      message: "We sent your FeeHunt license key to your email.",
      plan: license.plan,
      status: license.status,
      license_key: license.license_key,
    });
  } catch (error) {
    console.error("[Login] error:", error.message);
    return res.status(500).json({ code: "server_connection_issue", error: "FeeHunt could not complete login right now. Please try again in a moment." });
  }
});

app.post("/api/verify-license", verifyIpRateLimit, verifyKeyRateLimit, async (req, res) => {
  try {
    if (!requireSupabase(res)) return;

    const licenseKey = String(req.body.license_key || "").trim().toUpperCase();
    const deviceFingerprint = String(req.body.device_fingerprint || "").trim();
    const deviceName = String(req.body.device_name || "").trim() || null;
    const checkOnly = req.body.check_only === true;

    if (!LICENSE_REGEX.test(licenseKey) || (!checkOnly && !deviceFingerprint)) {
      return res.status(400).json({ status: "invalid", error: "Missing or invalid license key." });
    }

    const { data: license } = await supabase
      .from("licenses")
      .select("*")
      .eq("license_key", licenseKey)
      .maybeSingle();

    if (!license) {
      return res.json({ status: "invalid", error: "License key not found." });
    }

    let trialEndDate = license.trial_ends_at || null;
    if (!trialEndDate && license.user_id) {
      const { data: user } = await supabase
        .from("users")
        .select("trial_ends_at")
        .eq("id", license.user_id)
        .maybeSingle();
      trialEndDate = user?.trial_ends_at || null;
    }

    if (["cancelled", "expired"].includes(license.status)) {
      return res.json({
        status: "read_only",
        plan: license.plan,
        days_remaining: 0,
        message: "Your trial or subscription has ended.",
      });
    }

    if (license.status === "payment_failed") {
      return res.json({
        status: "payment_required",
        plan: license.plan,
        days_remaining: daysRemaining(trialEndDate),
        message: "Payment failed. Please update your payment method.",
      });
    }

    if (license.status === "trial" && trialEndDate && Date.now() > new Date(trialEndDate).getTime()) {
      await supabase
        .from("licenses")
        .update({ status: "expired", updated_at: new Date().toISOString() })
        .eq("license_key", licenseKey);
      await supabase
        .from("users")
        .update({ subscription_status: "expired", updated_at: new Date().toISOString() })
        .eq("id", license.user_id);
      return res.json({
        status: "read_only",
        plan: license.plan,
        days_remaining: 0,
        message: `Your ${TRIAL_DAYS}-day trial has ended.`,
      });
    }

    const nowIso = new Date().toISOString();
    const configuredMaxDevices = license.devices_max || MAX_DEVICES;
    const maxDevices = license.status === "trial" ? Math.max(configuredMaxDevices, 10) : configuredMaxDevices;

    if (!checkOnly) {
      const { data: existingDevice } = await supabase
        .from("devices")
        .select("id")
        .eq("license_id", license.id)
        .eq("device_fingerprint", deviceFingerprint)
        .maybeSingle();

      if (existingDevice) {
        await supabase.from("devices").update({ last_seen_at: nowIso }).eq("id", existingDevice.id);
      } else {
        const { count } = await supabase
          .from("devices")
          .select("id", { count: "exact", head: true })
          .eq("license_id", license.id);

        if ((count || 0) >= maxDevices) {
          return res.json({
            status: "device_limit",
            error: `Device limit reached (${maxDevices}).`,
            max_devices: maxDevices,
            current_devices: count || 0,
          });
        }

        await supabase.from("devices").insert({
          license_id: license.id,
          device_fingerprint: deviceFingerprint,
          device_name: deviceName,
          first_seen_at: nowIso,
          last_seen_at: nowIso,
        });
        await supabase.from("licenses").update({ devices_used: (count || 0) + 1 }).eq("id", license.id);
      }

      await supabase.from("licenses").update({ last_checked_at: nowIso }).eq("id", license.id);
    }

    return res.json({
      status: license.status === "trial" ? "trial" : "active",
      plan: license.plan,
      billing: license.billing,
      days_remaining: daysRemaining(trialEndDate),
      trial_ends_at: trialEndDate,
      max_devices: maxDevices,
      message: "FeeHunt license is active.",
    });
  } catch (error) {
    console.error("[Verify] error:", error.message);
    return res.status(500).json({ status: "error", error: "Server error." });
  }
});

app.get("/api/check-trials", async (req, res) => {
  try {
    const secret = process.env.FEEHUNT_CRON_SECRET || process.env.CRON_SECRET || "";
    const provided = req.get("x-feehunt-cron-secret") || req.query.secret || "";
    if (!secret || provided !== secret) {
      return res.status(401).json({ code: "unauthorized", error: "Unauthorized." });
    }
    if (!requireSupabase(res)) return;

    const { data: trialUsers, error } = await supabase
      .from("users")
      .select("id, email, trial_ends_at, last_reminder_sent")
      .eq("subscription_status", "trial");

    if (error) return res.status(500).json({ error: "Failed to query trial users." });

    let sent = 0;
    let expired = 0;
    let skipped = 0;

    for (const user of trialUsers || []) {
      const left = daysRemaining(user.trial_ends_at);
      const milestone = left <= 0 ? "expired" : left <= 1 ? "day13" : left <= 3 ? "day11" : left <= 7 ? "day7" : null;
      if (!milestone || user.last_reminder_sent === milestone) {
        skipped += 1;
        continue;
      }

      await sendTrialReminder(user.email, milestone, left);
      await supabase.from("email_notifications").insert({ user_id: user.id, type: milestone });
      await supabase.from("users").update({ last_reminder_sent: milestone }).eq("id", user.id);

      if (milestone === "expired") {
        expired += 1;
        await supabase.from("users").update({ subscription_status: "expired" }).eq("id", user.id);
        await supabase.from("licenses").update({ status: "expired" }).eq("user_id", user.id);
      }
      sent += 1;
    }

    return res.json({ processed: trialUsers?.length || 0, sent, expired, skipped });
  } catch (error) {
    console.error("[TrialCheck] error:", error.message);
    return res.status(500).json({ error: "Trial check failed." });
  }
});

async function sendTrialReminder(email, milestone, daysLeft) {
  const subject = milestone === "expired"
    ? "Your FeeHunt trial has ended"
    : `${daysLeft} day(s) left in your FeeHunt trial`;
  const body = milestone === "expired"
    ? `Your ${TRIAL_DAYS}-day FeeHunt trial has ended. Upgrade to keep scanning Gmail for subscriptions.`
    : `You have ${daysLeft} day(s) left in your FeeHunt trial.`;
  return sendMail({
    to: email,
    subject,
    html: `<div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;padding:28px"><h1>FeeHunt</h1><p>${body}</p><p><a href="${APP_URL}/pricing">View plans</a></p></div>`,
  });
}

app.post("/api/create-checkout", async (req, res) => {
  if (!stripe) {
    return res.status(501).json({ error: "Stripe checkout is not configured yet." });
  }
  return res.status(501).json({ error: "Stripe checkout will be enabled in the paid-plan phase." });
});

app.get("/", (_req, res) => {
  res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate, proxy-revalidate");
  res.sendFile(path.join(SITE_DIR, "index.html"));
});

async function handleWebhook(req, res) {
  return res.status(501).json({ received: false, error: "Stripe webhook will be enabled in the paid-plan phase." });
}

export default app;

if (!process.env.VERCEL) {
  app.listen(PORT, () => {
    console.log(`FeeHunt licensing server running on http://127.0.0.1:${PORT}`);
  });
  setInterval(() => {}, 60_000);
}
