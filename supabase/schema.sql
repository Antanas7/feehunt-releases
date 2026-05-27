-- IMPORTANT: this file describes the INTENDED schema, not the live one.
-- Production was originally seeded with users.id and licenses.id as `bigint`
-- (a legacy of the earlier BeSafe migration), so any new FK against those
-- tables must declare its referencing column as `bigint`, not `uuid`. See
-- 2026-05-27-missing-tables.sql for the live-compatible add-on migration.
-- Treat this file as a future-state spec; do not run it against prod as-is.

create extension if not exists pgcrypto;

create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  email text not null unique,
  subscription_plan text not null default 'basic',
  subscription_status text not null default 'trial',
  trial_started_at timestamptz not null default now(),
  trial_ends_at timestamptz not null default (now() + interval '14 days'),
  last_reminder_sent text,
  stripe_customer_id text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.licenses (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  email text not null,
  license_key text not null unique,
  plan text not null default 'basic',
  billing text not null default 'monthly',
  status text not null default 'trial',
  trial_ends_at timestamptz not null default (now() + interval '14 days'),
  devices_used integer not null default 0,
  devices_max integer not null default 3,
  stripe_customer_id text,
  stripe_subscription_id text,
  last_checked_at timestamptz,
  cancelled_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.devices (
  id uuid primary key default gen_random_uuid(),
  license_id uuid references public.licenses(id) on delete cascade,
  device_fingerprint text not null,
  device_name text,
  first_seen_at timestamptz not null default now(),
  last_seen_at timestamptz not null default now(),
  unique (license_id, device_fingerprint)
);

create table if not exists public.email_notifications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
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

create index if not exists idx_users_email on public.users(email);
create index if not exists idx_licenses_key on public.licenses(license_key);
create index if not exists idx_licenses_user_id on public.licenses(user_id);
create index if not exists idx_devices_license on public.devices(license_id);
create index if not exists idx_trial_status on public.users(subscription_status, trial_ends_at);

-- Lock every table to service_role only. FeeHunt's API uses
-- SUPABASE_SERVICE_ROLE_KEY (RLS-bypassing); the browser never touches
-- Supabase directly. anon + authenticated get default-deny.
alter table if exists public.users               enable row level security;
alter table if exists public.licenses            enable row level security;
alter table if exists public.devices             enable row level security;
alter table if exists public.email_notifications enable row level security;
alter table if exists public.webhook_events      enable row level security;
alter table if exists public.ai_audit_log        enable row level security;
