import {
  isValidLicenseKey,
  json,
  options,
  requireSupabase,
  stripeRequest,
  supabaseSelect,
} from "./_utils.js";

function normalizeLicenseKey(value) {
  return String(value || "").trim().toUpperCase().replace(/\s+/g, "");
}

export function onRequestOptions() {
  return options();
}

export async function onRequestPost({ request, env }) {
  try {
    if (!env.STRIPE_SECRET_KEY) {
      return json({ error: "Stripe is not configured." }, 500);
    }

    if (!requireSupabase(env)) {
      return json({ error: "FeeHunt account service is not configured." }, 503);
    }

    const body = await request.json().catch(() => ({}));
    const licenseKey = normalizeLicenseKey(body.license_key);

    if (!licenseKey || !isValidLicenseKey(licenseKey)) {
      return json({ error: "Please enter a valid FeeHunt license key." }, 400);
    }

    const licenses = await supabaseSelect(
      env,
      "licenses",
      `license_key=eq.${encodeURIComponent(licenseKey)}&select=id,user_id,email,stripe_customer_id`
    );
    const license = licenses[0];

    if (!license) {
      return json({ error: "FeeHunt could not find this license key." }, 404);
    }

    let stripeCustomerId = license.stripe_customer_id || null;

    if (!stripeCustomerId && license.user_id) {
      const users = await supabaseSelect(
        env,
        "users",
        `id=eq.${license.user_id}&select=stripe_customer_id`
      );
      stripeCustomerId = users[0]?.stripe_customer_id || null;
    }

    if (!stripeCustomerId) {
      return json(
        {
          error:
            "This license is not connected to a Stripe subscription yet. If you just paid, please wait a moment and try again.",
        },
        400
      );
    }

    const portalSession = await stripeRequest(env, "billing_portal/sessions", {
      customer: stripeCustomerId,
      return_url: "https://feehunt.pro/account.html",
    });

    return json({ url: portalSession.url });
  } catch (error) {
    console.error("[StripePortal] error", {
      message: error?.message,
      type: error?.type,
    });
    return json({ error: "Could not open Stripe subscription management right now." }, 500);
  }
}

export function onRequest() {
  return json({ error: "Method not allowed." }, 405);
}
