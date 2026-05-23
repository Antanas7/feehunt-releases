import { requireSupabase, supabaseSelect } from "./_utils.js";

export async function onRequestGet({ env }) {
  const emailConfigured = env.RESEND_API_KEY || env.SMTP_PASS;

  if (!requireSupabase(env)) {
    return Response.json({
      api: "ok",
      supabase: "missing",
      email: emailConfigured ? "configured" : "missing",
    }, { status: 503 });
  }

  try {
    await supabaseSelect(env, "users", "select=id&limit=1");
  } catch (error) {
    console.error("[Health] Supabase failed:", error.message);
    return Response.json({
      api: "ok",
      supabase: "error",
      email: emailConfigured ? "configured" : "missing",
    }, { status: 503 });
  }

  return Response.json({
    api: "ok",
    supabase: "ok",
    email: emailConfigured ? "configured" : "missing",
  });
}
