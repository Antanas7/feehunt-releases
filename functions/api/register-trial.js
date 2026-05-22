import {
  TRIAL_DAYS,
  accountSetupIssue,
  generateLicenseKey,
  isValidEmail,
  json,
  normalizeEmail,
  normalizePlan,
  requireSupabase,
  sendLicenseEmail,
  supabaseInsert,
  supabaseSelect,
  trialEndsAt,
} from "./_utils.js";

export async function onRequestPost({ request, env }) {
  try {
    if (!requireSupabase(env)) return accountSetupIssue();

    const body = await request.json().catch(() => ({}));
    const email = normalizeEmail(body.email);
    const plan = normalizePlan(body.plan);

    if (!isValidEmail(email)) {
      return json({ code: "invalid_email", error: "Please enter a valid Gmail or email address." }, 400);
    }

    const existingUsers = await supabaseSelect(env, "users", `email=eq.${encodeURIComponent(email)}&select=id`);
    const existing = existingUsers[0];

    if (existing) {
      const licenses = await supabaseSelect(env, "licenses", `user_id=eq.${existing.id}&select=*`);
      const existingLicense = licenses[0];
      if (!existingLicense) {
        return json({
          code: "license_creation_issue",
          error: "Account exists, but no license was found. Please contact support.",
        }, 409);
      }

      try {
        await sendLicenseEmail(env, email, existingLicense.license_key, existingLicense.plan || plan, "existing");
      } catch (error) {
        console.error("[Register] existing license email failed:", error.message);
        return json({
          code: "email_delivery_issue",
          error: "FeeHunt found your license, but could not send the email right now. Please try Log in / Resend key in a moment.",
        }, 502);
      }

      return json({
        success: true,
        message: "You already have a FeeHunt account. We sent your license key to your email again.",
        plan: existingLicense.plan,
        status: existingLicense.status,
        trial_days: TRIAL_DAYS,
      });
    }

    const licenseKey = generateLicenseKey();
    const endDate = trialEndsAt();

    let users;
    try {
      users = await supabaseInsert(env, "users", {
        email,
        subscription_plan: plan,
        subscription_status: "trial",
        trial_ends_at: endDate,
      });
    } catch (error) {
      console.error("[Register] user insert failed:", error.message);
      return json({
        code: "account_setup_issue",
        error: "FeeHunt could not create your account right now. Please try again in a moment.",
      }, 500);
    }

    const userId = users[0]?.id;
    try {
      await supabaseInsert(env, "licenses", {
        license_key: licenseKey,
        user_id: userId,
        email,
        plan,
        billing: "monthly",
        status: "trial",
        trial_ends_at: endDate,
      });
    } catch (error) {
      console.error("[Register] license insert failed:", error.message);
      return json({
        code: "license_creation_issue",
        error: "FeeHunt could not create your license key right now. Please try again in a moment.",
      }, 500);
    }

    try {
      await sendLicenseEmail(env, email, licenseKey, plan, "new");
    } catch (error) {
      console.error("[Register] license email failed:", error.message);
      return json({
        code: "email_delivery_issue",
        error: "FeeHunt created your trial, but could not send the license email right now. Please try Log in / Resend key in a moment.",
      }, 502);
    }

    return json({
      success: true,
      message: "Your 14-day FeeHunt trial has started. We sent your license key to your email.",
      trial_days: TRIAL_DAYS,
      plan,
      status: "trial",
    });
  } catch (error) {
    console.error("[Register] error:", error.message);
    return json({
      code: "server_connection_issue",
      error: "FeeHunt could not complete signup right now. Your information was not lost. Please try again in a moment.",
    }, 500);
  }
}
