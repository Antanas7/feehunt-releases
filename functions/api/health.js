import { json, requireSupabase, supabaseSelect } from "./_utils.js";

export async function onRequestGet({ env }) {
  const checks = { api: "ok", supabase: "unknown", email: env.RESEND_API_KEY ? "configured" : "missing" };

  if (!requireSupabase(env)) {
    checks.supabase = "missing";
    return json(checks, 503);
  }

  try {
    await supabaseSelect(env, "licenses", "select=id&limit=1");
    checks.supabase = "ok";
  } catch (error) {
    console.error("[Health] Supabase failed:", error.message);
    checks.supabase = "error";
  }

  return json(checks, checks.supabase === "ok" ? 200 : 503);
}
