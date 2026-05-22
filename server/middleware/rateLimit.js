const state = new Map();

export function keyByIp(req) {
  const forwarded = req.headers["x-forwarded-for"];
  if (typeof forwarded === "string" && forwarded.trim()) {
    return forwarded.split(",")[0].trim();
  }
  return req.ip || req.socket?.remoteAddress || "unknown";
}

export function keyByLicenseBody(req) {
  const value = req.body?.license_key;
  return typeof value === "string" && value.trim()
    ? value.trim().toUpperCase()
    : null;
}

export function createRateLimit({ limit = 30, windowMs = 60_000, keyExtractor = keyByIp } = {}) {
  return function rateLimit(req, res, next) {
    const key = keyExtractor(req);
    if (!key) return next();

    const now = Date.now();
    const bucketKey = `${req.path}:${key}`;
    const current = state.get(bucketKey);

    if (!current || now - current.windowStart > windowMs) {
      state.set(bucketKey, { count: 1, windowStart: now });
      return next();
    }

    current.count += 1;
    if (current.count > limit) {
      res.set("Retry-After", String(Math.ceil((windowMs - (now - current.windowStart)) / 1000)));
      return res.status(429).json({
        error: "Too many attempts. Please wait a minute and try again.",
      });
    }

    return next();
  };
}
