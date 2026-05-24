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

function logError(label, error, extra = {}) {
  console.error(label, {
    message: error?.message,
    stack: error?.stack,
    name: error?.name,
    cause: error?.cause,
    ...extra,
  });
}

export async function onRequestPost({ request, env }) {
  try {
    console.log("[Register] signup started");

    if (!requireSupabase(env)) {
      console.error("[Register] Supabase config missing");
      return accountSetupIssue();
    }

    const body = await request.json().catch(() => ({}));
    const email = normalizeEmail(body.email);
    const plan = normalizePlan(body.plan);

    console.log("[Register] parsed request", { email, plan });

    if (!isValidEmail(email)) {
      return json(
        {
          code: "invalid_email",
          error: "Please enter a valid Gmail or email address.",
        },
        400
      );
    }

    let existingUsers = [];

    try {
      existingUsers = await supabaseSelect(
        env,
        "users",
        `email=eq.${encodeURIComponent(email)}&select=id,email`
      );
    } catch (error) {
      logError("[Register] existing user lookup failed", error, { email });
      return json(
        {
          code: "account_lookup_issue",
          error: "FeeHunt could not check your account right now. Please try again in a moment.",
        },
        500
      );
    }

    const existing = existingUsers[0];

    if (existing) {
      console.log("[Register] existing user found", { userId: existing.id, email });

      let licenses = [];

      try {
        licenses = await supabaseSelect(
          env,
          "licenses",
          `user_id=eq.${existing.id}&select=*`
        );
      } catch (error) {
        logError("[Register] existing license lookup failed", error, {
          userId: existing.id,
          email,
        });

        return json(
          {
            code: "license_lookup_issue",
            error: "FeeHunt found your account, but could not check your license right now. Please try again in a moment.",
          },
          500
        );
      }

      const existingLicense = licenses[0];

      if (!existingLicense) {
        console.error("[Register] existing user has no license", {
          userId: existing.id,
          email,
        });

        return json(
          {
            code: "license_creation_issue",
            error: "Account exists, but no license was found. Please contact support.",
          },
          409
        );
      }

      try {
        await sendLicenseEmail(
          env,
          email,
          existingLicense.license_key,
          existingLicense.plan || plan,
          "existing"
        );
      } catch (error) {
        logError("[Register] existing license email failed", error, {
          userId: existing.id,
          email,
        });

        return json(
          {
            code: "email_delivery_issue",
            error: "FeeHunt found your license, but could not send the email right now. Please try Log in / Resend key in a moment.",
          },
          502
        );
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

    console.log("[Register] creating new trial", {
      email,
      plan,
      trialEndsAt: endDate,
    });

    let users;

    try {
      users = await supabaseInsert(env, "users", {
        email,
        subscription_plan: plan,
        subscription_status: "trial",
        trial_ends_at: endDate,
      });

      console.log("[Register] user insert result", {
        email,
        usersCount: Array.isArray(users) ? users.length : null,
        firstUser: users?.[0] || null,
      });
    } catch (error) {
      logError("[Register] user insert failed", error, { email, plan });

      return json(
        {
          code: "account_setup_issue",
          error: "FeeHunt could not create your account right now. Please try again in a moment.",
        },
        500
      );
    }

    const userId = users?.[0]?.id;

    if (!userId) {
      console.error("[Register] user insert returned no user id", {
        email,
        plan,
        users,
      });

      return json(
        {
          code: "account_setup_issue",
          error: "FeeHunt created a partial account, but could not confirm the user ID. Please contact support.",
        },
        500
      );
    }

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

      console.log("[Register] license created", {
        userId,
        email,
        plan,
      });
    } catch (error) {
      logError("[Register] license insert failed", error, {
        userId,
        email,
        plan,
        attemptedLicensePayload: {
          license_key: "[hidden]",
          user_id: userId,
          email,
          plan,
          billing: "monthly",
          status: "trial",
          trial_ends_at: endDate,
        },
      });

      return json(
        {
          code: "license_creation_issue",
          error: "FeeHunt could not create your license key right now. Please try again in a moment.",
        },
        500
      );
    }

    try {
      await sendLicenseEmail(env, email, licenseKey, plan, "new");

      console.log("[Register] license email sent", {
        userId,
        email,
        plan,
      });
    } catch (error) {
      logError("[Register] license email failed", error, {
        userId,
        email,
        plan,
      });

      return json(
        {
          code: "email_delivery_issue",
          error: "FeeHunt created your trial, but could not send the license email right now. Please try Log in / Resend key in a moment.",
        },
        502
      );
    }

    return json({
      success: true,
      message: "Your 14-day FeeHunt trial has started. We sent your license key to your email.",
      trial_days: TRIAL_DAYS,
      plan,
      status: "trial",
    });
  } catch (error) {
    logError("[Register] unexpected error", error);

    return json(
      {
        code: "server_connection_issue",
        error: "FeeHunt could not complete signup right now. Your information was not lost. Please try again in a moment.",
      },
      500
    );
  }
}