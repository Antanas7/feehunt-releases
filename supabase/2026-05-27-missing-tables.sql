-- =============================================================================
-- Create FeeHunt tables that schema.sql defines but the live DB never had
-- (2026-05-27)
-- =============================================================================
--
-- Three tables that the code already references but that are missing in
-- production Supabase. Without them, the following code paths silently fail
-- (or throw) the first time real traffic hits them:
--
--   * email_notifications — used by server/server.js (reminder tracking) and
--     functions/api/check-trials.js (trial-ending emails). First scheduled
--     run after launch would fail.
--
--   * webhook_events — used by functions/api/stripe-webhook.js for Stripe
--     idempotency (so the same event is not processed twice). First Stripe
--     payment event after launch would fail to log idempotency, opening the
--     door to double-charged plan upgrades on Stripe retries.
--
--   * ai_audit_log — placeholder for the in-progress AI radar feature. Safe
--     to keep around even if unused.
--
-- Idempotent (uses `if not exists`). Includes RLS so these tables are locked
-- to service_role from the start.
-- =============================================================================

create extension if not exists pgcrypto;

-- NOTE: live public.users.id is bigint (predates schema.sql's uuid spec).
-- Match FK to live type rather than to schema.sql.
create table if not exists public.email_notifications (
  id uuid primary key default gen_random_uuid(),
  user_id bigint references public.users(id) on delete cascade,
  type text not null,
  sent_at timestamptz not null default now(),
  unique (user_id, type)
);

create table if not exists public.webhook_events (
  id uuid primary key default gen_random_uuid(),
  event_id text not null unique,
  event_type text not null,
  created_at timestamptz not null default now()
);

create table if not exists public.ai_audit_log (
  id uuid primary key default gen_random_uuid(),
  license_id uuid,
  license_key text,
  device_fingerprint text,
  ip text,
  user_agent text,
  action text not null,
  status text not null,
  error_message text,
  tokens_used integer,
  created_at timestamptz not null default now()
);

alter table if exists public.email_notifications enable row level security;
alter table if exists public.webhook_events      enable row level security;
alter table if exists public.ai_audit_log        enable row level security;

-- Verify (read-only): expect all three to appear with rowsecurity = true.
-- select tablename, rowsecurity
--   from pg_tables
--  where schemaname = 'public'
--    and tablename in ('email_notifications','webhook_events','ai_audit_log')
--  order by tablename;
