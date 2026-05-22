import {
  MAX_DEVICES,
  daysRemaining,
  isValidLicenseKey,
  json,
  requireSupabase,
  supabaseInsert,
  supabaseSelect,
  supabaseUpdate,
} from "./_utils.js";

export async function onRequestPost({ request, env }) {
  try {
    if (!requireSupabase(env)) {
      return json({
        status: "error",
        code: "account_setup_issue",
        error: "FeeHunt account setup is not finished yet.",
      }, 503);
    }

    const body = await request.json().catch(() => ({}));
    const licenseKey = String(body.license_key || "").trim().toUpperCase();
    const deviceFingerprint = String(body.device_fingerprint || "").trim();
    const deviceName = String(body.device_name || "").trim() || null;

    if (!isValidLicenseKey(licenseKey) || !deviceFingerprint) {
      return json({ status: "invalid", error: "Missing or invalid license key." }, 400);
    }

    const licenses = await supabaseSelect(env, "licenses", `license_key=eq.${encodeURIComponent(licenseKey)}&select=*`);
    const license = licenses[0];
    if (!license) {
      return json({ status: "invalid", error: "License key not found." });
    }

    let trialEndDate = license.trial_ends_at || null;
    if (!trialEndDate && license.user_id) {
      const users = await supabaseSelect(env, "users", `id=eq.${license.user_id}&select=trial_ends_at`);
      trialEndDate = users[0]?.trial_ends_at || null;
    }

    if (["cancelled", "expired"].includes(license.status)) {
      return json({
        status: "read_only",
        plan: license.plan,
        days_remaining: 0,
        message: "Your trial or subscription has ended.",
      });
    }

    if (license.status === "payment_failed") {
      return json({
        status: "payment_required",
        plan: license.plan,
        days_remaining: daysRemaining(trialEndDate),
        message: "Payment failed. Please update your payment method.",
      });
    }

    if (license.status === "trial" && trialEndDate && Date.now() > new Date(trialEndDate).getTime()) {
      const nowIso = new Date().toISOString();
      await supabaseUpdate(env, "licenses", `license_key=eq.${encodeURIComponent(licenseKey)}`, {
        status: "expired",
        updated_at: nowIso,
      });
      if (license.user_id) {
        await supabaseUpdate(env, "users", `id=eq.${license.user_id}`, {
          subscription_status: "expired",
          updated_at: nowIso,
        });
      }
      return json({
        status: "read_only",
        plan: license.plan,
        days_remaining: 0,
        message: "Your 14-day trial has ended.",
      });
    }

    const nowIso = new Date().toISOString();
    const maxDevices = license.devices_max || MAX_DEVICES;
    const existingDevices = await supabaseSelect(
      env,
      "devices",
      `license_id=eq.${license.id}&device_fingerprint=eq.${encodeURIComponent(deviceFingerprint)}&select=id`,
    );
    const existingDevice = existingDevices[0];

    if (existingDevice) {
      await supabaseUpdate(env, "devices", `id=eq.${existingDevice.id}`, { last_seen_at: nowIso });
    } else {
      const devices = await supabaseSelect(env, "devices", `license_id=eq.${license.id}&select=id`);
      if (devices.length >= maxDevices) {
        return json({
          status: "device_limit",
          error: `Device limit reached (${maxDevices}).`,
          max_devices: maxDevices,
          current_devices: devices.length,
        });
      }

      await supabaseInsert(env, "devices", {
        license_id: license.id,
        device_fingerprint: deviceFingerprint,
        device_name: deviceName,
        first_seen_at: nowIso,
        last_seen_at: nowIso,
      });
      await supabaseUpdate(env, "licenses", `id=eq.${license.id}`, { devices_used: devices.length + 1 });
    }

    await supabaseUpdate(env, "licenses", `id=eq.${license.id}`, { last_checked_at: nowIso });

    return json({
      status: license.status === "trial" ? "trial" : "active",
      plan: license.plan,
      billing: license.billing,
      days_remaining: daysRemaining(trialEndDate),
      trial_ends_at: trialEndDate,
      max_devices: maxDevices,
      message: "FeeHunt license is active.",
    });
  } catch (error) {
    console.error("[Verify] error:", error.message);
    return json({ status: "error", error: "Server error." }, 500);
  }
}
