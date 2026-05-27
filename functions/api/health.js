import { json, options, requireSupabase, supabaseSelect } from "./_utils.js";

export function onRequestOptions() {
  return options();
}

export async function onRequestGet({ env }) {
  const emailConfigured = Boolean(env.RESEND_API_KEY || env.SMTP_PASS);

  if (!requireSupabase(env)) {
    return json({
      ok: false,
      api: "ok",
      supabase: "missing",
      email: emailConfigured ? "configured" : "missing",
    }, 503);
  }

  try {
    await supabaseSelect(env, "users", "select=id&limit=1");
  } catch (error) {
    console.error("[Health] Supabase failed:", error.message);
    return json({
      ok: false,
      api: "ok",
      supabase: "error",
      email: emailConfigured ? "configured" : "missing",
    }, 503);
  }

  return json({
    ok: true,
    api: "ok",
    supabase: "ok",
    email: emailConfigured ? "configured" : "missing",
  });
}
