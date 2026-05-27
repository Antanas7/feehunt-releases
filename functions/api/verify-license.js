import {
  MAX_DEVICES,
  TRIAL_DAYS,
  daysRemaining,
  isValidLicenseKey,
  json,
  options,
  requireSupabase,
  supabaseInsert,
  supabaseSelect,
  supabaseUpdate,
} from "./_utils.js";

export function onRequestOptions() {
  return options();
}

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
    const checkOnly = body.check_only === true;

    if (!isValidLicenseKey(licenseKey) || (!checkOnly && !deviceFingerprint)) {
      return json({
        status: "invalid",
        code: "invalid_request",
        error: "Missing or invalid license key.",
      }, 400);
    }

    const licenses = await supabaseSelect(env, "licenses", `license_key=eq.${encodeURIComponent(licenseKey)}&select=*`);
    const license = licenses[0];
    if (!license) {
      return json({
        status: "invalid",
        code: "license_not_found",
        error: "License key not found.",
      }, 404);
    }

    let trialEndDate = license.trial_ends_at || null;
    if (!trialEndDate && license.user_id) {
      const users = await supabaseSelect(env, "users", `id=eq.${license.user_id}&select=trial_ends_at`);
      trialEndDate = users[0]?.trial_ends_at || null;
    }

    if (["cancelled", "expired"].includes(license.status)) {
      return json({
        status: "read_only",
        code: "license_ended",
        plan: license.plan,
        days_remaining: 0,
        message: "Your trial or subscription has ended.",
      }, 403);
    }

    if (license.status === "payment_failed") {
      return json({
        status: "payment_required",
        code: "payment_required",
        plan: license.plan,
        days_remaining: daysRemaining(trialEndDate),
        message: "Payment failed. Please update your payment method.",
      }, 402);
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
        code: "trial_ended",
        plan: license.plan,
        days_remaining: 0,
        message: `Your ${TRIAL_DAYS}-day trial has ended.`,
      }, 403);
    }

    const nowIso = new Date().toISOString();
    const configuredMaxDevices = license.devices_max || MAX_DEVICES;
    const maxDevices = license.status === "trial" ? Math.max(configuredMaxDevices, 10) : configuredMaxDevices;

    if (!checkOnly) {
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
            code: "device_limit",
            error: `Device limit reached (${maxDevices}).`,
            max_devices: maxDevices,
            current_devices: devices.length,
          }, 409);
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
    }

    return json({
      status: license.status === "trial" ? "trial" : "active",
      code: "license_active",
      plan: license.plan,
      billing: license.billing,
      days_remaining: daysRemaining(trialEndDate),
      trial_ends_at: trialEndDate,
      max_devices: maxDevices,
      message: "FeeHunt license is active.",
    });
  } catch (error) {
    console.error("[Verify] error:", error.message);
    return json({ status: "error", code: "server_error", error: "Server error." }, 500);
  }
}
