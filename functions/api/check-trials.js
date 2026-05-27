import {
  daysRemaining,
  json,
  requireSupabase,
  supabaseInsert,
  supabaseSelect,
  supabaseUpdate,
} from "./_utils.js";

function isAuthorized(request, env) {
  const secret = env.FEEHUNT_CRON_SECRET || env.CRON_SECRET || "";
  if (!secret) return false;
  const url = new URL(request.url);
  return (
    request.headers.get("x-feehunt-cron-secret") === secret ||
    url.searchParams.get("secret") === secret
  );
}

function reminderMilestone(daysLeft) {
  if (daysLeft <= 0) return null;
  if (daysLeft <= 3) return "day11";
  return null;
}

function reminderCopy(milestone, daysLeft) {
  return {
    subject: `${daysLeft} day(s) left in FeeHunt trial / Liko ${daysLeft} d. FeeHunt bandyme`,
    heading: `${daysLeft} day(s) left in your FeeHunt trial`,
    body:
      "Your FeeHunt trial is close to ending. Review your plan and decide whether you want to continue after the trial.",
    headingLt: `Liko ${daysLeft} d. iki FeeHunt bandymo pabaigos`,
    bodyLt:
      "Jusu FeeHunt bandymas arteja prie pabaigos. Perziurekite plana ir nuspreskite, ar norite testi naudojima po bandymo.",
    cta: "Review plans",
    ctaLt: "Perziureti planus",
  };
}

async function sendTrialReminder(env, email, milestone, daysLeft) {
  if (!env.RESEND_API_KEY) {
    throw new Error("RESEND_API_KEY is not configured.");
  }

  const appUrl = env.FEEHUNT_APP_URL || "https://feehunt.pro";
  const pricingUrl = `${appUrl.replace(/\/$/, "")}/pricing`;
  const from = `"FeeHunt" <${env.EMAIL_FROM || "support@feehunt.pro"}>`;
  const copy = reminderCopy(milestone, daysLeft);

  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      authorization: `Bearer ${env.RESEND_API_KEY}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      from,
      to: email,
      subject: copy.subject,
      html: `
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:28px;background:#f6f7f4;color:#17211b">
          <h1 style="margin:0 0 8px;color:#16664f">FeeHunt</h1>
          <div style="background:#fff;border:1px solid #dce4dd;border-left:4px solid #16664f;border-radius:8px;padding:20px;margin:18px 0">
            <h2 style="margin:0 0 10px">${copy.heading}</h2>
            <p style="margin:0;color:#405047;line-height:1.55">${copy.body}</p>
          </div>
          <div style="background:#fff;border:1px solid #dce4dd;border-left:4px solid #16664f;border-radius:8px;padding:20px;margin:18px 0">
            <h2 style="margin:0 0 10px">${copy.headingLt}</h2>
            <p style="margin:0;color:#405047;line-height:1.55">${copy.bodyLt}</p>
          </div>
          <p style="text-align:center;margin:26px 0">
            <a href="${pricingUrl}" style="background:#16664f;color:#fff;padding:12px 22px;border-radius:8px;text-decoration:none;font-weight:700">${copy.cta} / ${copy.ctaLt}</a>
          </p>
          <p style="font-size:13px;color:#5c6a61">You are receiving this because you started a FeeHunt trial. FeeHunt uses reminders sparingly and only around important account dates.</p>
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

export async function onRequestGet({ request, env }) {
  try {
    if (!isAuthorized(request, env)) {
      return json({ code: "unauthorized", error: "Unauthorized." }, 401);
    }

    if (!requireSupabase(env)) {
      return json({ code: "account_setup_issue", error: "Supabase is not configured." }, 503);
    }

    const trialUsers = await supabaseSelect(
      env,
      "users",
      "subscription_status=eq.trial&select=id,email,trial_ends_at,last_reminder_sent"
    );

    let sent = 0;
    let skipped = 0;
    const errors = [];

    for (const user of trialUsers) {
      const daysLeft = daysRemaining(user.trial_ends_at);
      const milestone = reminderMilestone(daysLeft);

      if (!milestone || user.last_reminder_sent === milestone) {
        skipped += 1;
        continue;
      }

      try {
        await sendTrialReminder(env, user.email, milestone, daysLeft);

        try {
          await supabaseInsert(env, "email_notifications", {
            user_id: user.id,
            type: milestone,
          });
        } catch (error) {
          console.warn("[TrialCheck] notification log skipped", {
            userId: user.id,
            milestone,
            message: error?.message,
          });
        }

        await supabaseUpdate(env, "users", `id=eq.${user.id}`, {
          last_reminder_sent: milestone,
          updated_at: new Date().toISOString(),
        });

        sent += 1;
      } catch (error) {
        errors.push({
          user_id: user.id,
          email: user.email,
          milestone,
          message: error?.message || "Unknown error",
        });
      }
    }

    return json({
      processed: trialUsers.length,
      sent,
      skipped,
      errors,
    });
  } catch (error) {
    console.error("[TrialCheck] error", error);
    return json({ code: "trial_check_failed", error: "Trial check failed." }, 500);
  }
}
