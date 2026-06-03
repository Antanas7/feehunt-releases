import { isValidEmail, normalizeEmail, normalizeLanguage, stripeRequest } from "./_utils.js";

const PRICE_IDS = {
  basic: "price_1Tazn1JlxAPRgwiDc90y2ksZ",
  family: "price_1TazoiJlxAPRgwiDwvzTNX1Q",
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "POST, OPTIONS",
      "access-control-allow-headers": "content-type, accept",
    },
  });
}

export function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "POST, OPTIONS",
      "access-control-allow-headers": "content-type, accept",
      "access-control-max-age": "86400",
    },
  });
}

export async function onRequestPost({ request, env }) {
  try {
    const body = await request.json().catch(() => ({}));
    const plan = String(body.plan || "").trim().toLowerCase();
    const email = normalizeEmail(body.email);
    const language = normalizeLanguage(body.language);
    const priceId = PRICE_IDS[plan];

    if (!priceId) {
      return json({ error: "Invalid plan. Use basic or family." }, 400);
    }

    if (!env.STRIPE_SECRET_KEY) {
      return json({ error: "Stripe is not configured." }, 500);
    }

    const sessionPayload = {
      mode: "subscription",
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: "https://feehunt.pro/success.html?session_id={CHECKOUT_SESSION_ID}",
      cancel_url: "https://feehunt.pro/pricing.html",
      metadata: { plan, language },
      subscription_data: { metadata: { plan, language } },
    };

    if (isValidEmail(email)) {
      sessionPayload.customer_email = email;
      sessionPayload.metadata.email = email;
      sessionPayload.subscription_data.metadata.email = email;
    }

    const session = await stripeRequest(env, "checkout/sessions", sessionPayload);

    return json({ url: session.url });
  } catch (error) {
    console.error("[StripeCheckout] error", {
      message: error?.message,
      type: error?.type,
    });

    return json({ error: "Could not create Stripe Checkout session." }, 500);
  }
}

export function onRequest() {
  return json({ error: "Method not allowed." }, 405);
}
