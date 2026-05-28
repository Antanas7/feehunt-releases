import Stripe from "stripe";
import {
  generateLicenseKey,
  isValidEmail,
  json,
  normalizeEmail,
  normalizePlan,
  requireSupabase,
  sendLicenseEmail,
  supabaseInsert,
  supabaseSelect,
  supabaseUpdate,
} from "./_utils.js";

function stripeClient(env) {
  return new Stripe(env.STRIPE_SECRET_KEY, {
    apiVersion: "2025-11-17.clover",
    httpClient: Stripe.createFetchHttpClient(),
  });
}

function stripeIdsFromSession(session) {
  return {
    stripe_customer_id: typeof session.customer === "string" ? session.customer : session.customer?.id || null,
    stripe_subscription_id: typeof session.subscription === "string" ? session.subscription : session.subscription?.id || null,
  };
}

async function findOrCreateUser(env, email, plan, stripeIds) {
  const existingUsers = await supabaseSelect(
    env,
    "users",
    `email=eq.${encodeURIComponent(email)}&select=id,email,subscription_plan,subscription_status`
  );
  const existing = existingUsers[0];
  const payload = {
    subscription_plan: plan,
    subscription_status: "active",
    stripe_customer_id: stripeIds.stripe_customer_id,
    updated_at: new Date().toISOString(),
  };

  if (existing) {
    await supabaseUpdate(env, "users", `id=eq.${existing.id}`, payload);
    return existing;
  }

  const users = await supabaseInsert(env, "users", {
    email,
    ...payload,
  });
  return users[0];
}

async function activateLicense(env, user, email, plan, stripeIds) {
  const licenses = await supabaseSelect(env, "licenses", `user_id=eq.${user.id}&select=*`);
  const existingLicense = licenses[0];
  const payload = {
    email,
    plan,
    billing: "monthly",
    status: "active",
    stripe_customer_id: stripeIds.stripe_customer_id,
    stripe_subscription_id: stripeIds.stripe_subscription_id,
    updated_at: new Date().toISOString(),
  };

  if (existingLicense) {
    await supabaseUpdate(env, "licenses", `id=eq.${existingLicense.id}`, payload);
    return {
      licenseKey: existingLicense.license_key,
      wasAlreadyActive:
        existingLicense.status === "active" &&
        existingLicense.stripe_subscription_id === stripeIds.stripe_subscription_id,
    };
  }

  const licenseKey = generateLicenseKey();
  await supabaseInsert(env, "licenses", {
    license_key: licenseKey,
    user_id: user.id,
    ...payload,
  });
  return { licenseKey, wasAlreadyActive: false };
}

async function handleCheckoutCompleted(env, session) {
  const email = normalizeEmail(session.customer_details?.email || session.customer_email);
  const plan = normalizePlan(session.metadata?.plan);

  if (!isValidEmail(email)) {
    throw new Error("Stripe checkout session has no valid customer email.");
  }

  if (!["basic", "family", "pro"].includes(plan)) {
    throw new Error(`Unsupported Stripe checkout plan: ${plan}`);
  }

  const stripeIds = stripeIdsFromSession(session);
  const user = await findOrCreateUser(env, email, plan, stripeIds);
  const { licenseKey, wasAlreadyActive } = await activateLicense(env, user, email, plan, stripeIds);
  if (!wasAlreadyActive) {
    await sendLicenseEmail(env, email, licenseKey, plan, "active");
  }
}

async function handleSubscriptionStatus(env, subscription, status) {
  const subscriptionId = typeof subscription.id === "string" ? subscription.id : null;
  if (!subscriptionId) return;

  const licenses = await supabaseSelect(
    env,
    "licenses",
    `stripe_subscription_id=eq.${encodeURIComponent(subscriptionId)}&select=id,user_id`
  );
  const license = licenses[0];
  if (!license) return;

  await supabaseUpdate(env, "licenses", `id=eq.${license.id}`, {
    status,
    updated_at: new Date().toISOString(),
  });

  if (license.user_id) {
    await supabaseUpdate(env, "users", `id=eq.${license.user_id}`, {
      subscription_status: status,
      updated_at: new Date().toISOString(),
    });
  }
}

async function wasWebhookProcessed(env, event) {
  const existingEvents = await supabaseSelect(
    env,
    "webhook_events",
    `event_id=eq.${encodeURIComponent(event.id)}&select=id`
  );
  return Boolean(existingEvents[0]);
}

async function markWebhookProcessed(env, event) {
  try {
    await supabaseInsert(env, "webhook_events", {
      event_id: event.id,
      event_type: event.type,
    });
  } catch (error) {
    console.warn("[StripeWebhook] webhook event log skipped", {
      eventId: event.id,
      eventType: event.type,
      message: error?.message,
    });
  }
}

export async function onRequestPost({ request, env }) {
  try {
    if (!env.STRIPE_SECRET_KEY || !env.STRIPE_WEBHOOK_SECRET) {
      return json({ error: "Stripe webhook is not configured." }, 500);
    }

    if (!requireSupabase(env)) {
      return json({ error: "Supabase is not configured." }, 503);
    }

    const signature = request.headers.get("stripe-signature");
    if (!signature) {
      return json({ error: "Missing Stripe signature." }, 400);
    }

    const payload = await request.text();
    const stripe = stripeClient(env);
    const event = await stripe.webhooks.constructEventAsync(
      payload,
      signature,
      env.STRIPE_WEBHOOK_SECRET,
      undefined,
      Stripe.createSubtleCryptoProvider()
    );

    if (await wasWebhookProcessed(env, event)) {
      return json({ received: true, duplicate: true });
    }

    if (event.type === "checkout.session.completed") {
      await handleCheckoutCompleted(env, event.data.object);
    }

    if (event.type === "customer.subscription.deleted") {
      await handleSubscriptionStatus(env, event.data.object, "cancelled");
    }

    if (event.type === "invoice.payment_failed") {
      const subscriptionId = event.data.object.subscription;
      if (subscriptionId) {
        await handleSubscriptionStatus(env, { id: subscriptionId }, "payment_failed");
      }
    }

    if (event.type === "invoice.paid") {
      const subscriptionId = event.data.object.subscription;
      if (subscriptionId) {
        await handleSubscriptionStatus(env, { id: subscriptionId }, "active");
      }
    }

    await markWebhookProcessed(env, event);

    return json({ received: true });
  } catch (error) {
    console.error("[StripeWebhook] error", {
      message: error?.message,
      type: error?.type,
    });
    return json({ error: "Stripe webhook failed." }, 500);
  }
}

export function onRequest() {
  return json({ error: "Method not allowed." }, 405);
}
