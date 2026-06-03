import {
  TRIAL_DAYS,
  accountSetupIssue,
  generateLicenseKey,
  isValidEmail,
  json,
  normalizeEmail,
  normalizeLanguage,
  normalizePlan,
  requireSupabase,
  sendLicenseEmail,
  supabaseInsert,
  supabaseSelect,
  supabaseUpdate,
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
    const language = normalizeLanguage(body.language);
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
        `email=eq.${encodeURIComponent(email)}&select=id,email,subscription_plan,trial_ends_at`
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
        console.warn("[Register] existing user has no license; creating replacement trial license", {
          userId: existing.id,
          email,
        });

        const recoveredLicenseKey = generateLicenseKey();
        const recoveredPlan = normalizePlan(plan || existing.subscription_plan);
        const recoveredTrialEnd = existing.trial_ends_at || trialEndsAt();

        try {
          await supabaseInsert(env, "licenses", {
            license_key: recoveredLicenseKey,
            user_id: existing.id,
            email,
            plan: recoveredPlan,
            billing: "monthly",
            status: "trial",
            trial_ends_at: recoveredTrialEnd,
          });
        } catch (error) {
          logError("[Register] replacement license insert failed", error, {
            userId: existing.id,
            email,
            plan: recoveredPlan,
          });

          return json(
            {
              code: "license_creation_issue",
              error: "FeeHunt found your account, but could not create your license key right now. Please try again in a moment.",
            },
            500
          );
        }

        try {
          await sendLicenseEmail(env, email, recoveredLicenseKey, recoveredPlan, "new", language);
        } catch (error) {
          logError("[Register] replacement license email failed", error, {
            userId: existing.id,
            email,
          });

          return json(
            {
              code: "email_delivery_issue",
              error: "FeeHunt created your license, but could not send the email right now. Please try Log in / Resend key in a moment.",
            },
            502
          );
        }

        return json({
          success: true,
          message: "Your FeeHunt license key has been created and sent to your email.",
          plan: recoveredPlan,
          status: "trial",
          trial_days: TRIAL_DAYS,
        });
      }

      let selectedLicensePlan = normalizePlan(existingLicense.plan || plan);
      const isExplicitPaidPlanSelection = ["basic", "family", "pro"].includes(plan);
      if (existingLicense.status === "trial" && isExplicitPaidPlanSelection && plan !== selectedLicensePlan) {
        selectedLicensePlan = plan;

        try {
          const nowIso = new Date().toISOString();
          await supabaseUpdate(env, "licenses", `id=eq.${existingLicense.id}`, {
            plan: selectedLicensePlan,
            updated_at: nowIso,
          });
          await supabaseUpdate(env, "users", `id=eq.${existing.id}`, {
            subscription_plan: selectedLicensePlan,
            updated_at: nowIso,
          });

          console.log("[Register] existing trial plan updated", {
            userId: existing.id,
            email,
            plan: selectedLicensePlan,
          });
        } catch (error) {
          logError("[Register] existing trial plan update failed", error, {
            userId: existing.id,
            email,
            plan: selectedLicensePlan,
          });

          return json(
            {
              code: "plan_update_issue",
              error: "FeeHunt found your account, but could not update your selected plan right now. Please try again in a moment.",
            },
            500
          );
        }
      }

      try {
        await sendLicenseEmail(
          env,
          email,
          existingLicense.license_key,
          selectedLicensePlan,
          "existing",
          language
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
        plan: selectedLicensePlan,
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
      await sendLicenseEmail(env, email, licenseKey, plan, "new", language);

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
      message: `Your ${TRIAL_DAYS}-day FeeHunt trial has started. We sent your license key to your email.`,
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
