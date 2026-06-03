import {
  accountSetupIssue,
  isValidEmail,
  json,
  normalizeEmail,
  normalizeLanguage,
  requireSupabase,
  sendLicenseEmail,
  supabaseSelect,
} from "./_utils.js";

export async function onRequestPost({ request, env }) {
  try {
    if (!requireSupabase(env)) return accountSetupIssue();

    const body = await request.json().catch(() => ({}));
    const email = normalizeEmail(body.email);
    const language = normalizeLanguage(body.language);

    if (!isValidEmail(email)) {
      return json({ code: "invalid_email", error: "Please enter your email address." }, 400);
    }

    const users = await supabaseSelect(env, "users", `email=eq.${encodeURIComponent(email)}&select=id`);
    const user = users[0];
    if (!user) {
      return json({ code: "account_not_found", error: "No FeeHunt account was found for this email." }, 404);
    }

    const licenses = await supabaseSelect(env, "licenses", `user_id=eq.${user.id}&select=*`);
    const license = licenses[0];
    if (!license) {
      return json({ code: "license_creation_issue", error: "No license was found. Please contact support." }, 404);
    }

    try {
      await sendLicenseEmail(env, email, license.license_key, license.plan || "basic", "existing", language);
    } catch (error) {
      console.error("[Login] email failed:", error.message);
      return json({
        code: "email_delivery_issue",
        error: "FeeHunt found your license, but could not send the email right now. Please try again in a moment.",
      }, 502);
    }

    return json({
      success: true,
      message: "We sent your FeeHunt license key to your email.",
      plan: license.plan,
      status: license.status,
    });
  } catch (error) {
    console.error("[Login] error:", error.message);
    return json({
      code: "server_connection_issue",
      error: "FeeHunt could not complete login right now. Please try again in a moment.",
    }, 500);
  }
}
