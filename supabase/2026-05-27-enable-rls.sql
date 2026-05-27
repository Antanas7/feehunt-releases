-- =============================================================================
-- Enable Row-Level Security on all FeeHunt tables (2026-05-27)
-- =============================================================================
--
-- Purpose:
--   Close the Supabase linter warning "Publicly accessible table — anyone with
--   the project URL can read, edit and delete all data because Row-Level
--   Security is disabled". Without RLS, the anon API key (embedded in any
--   browser request to the Supabase REST endpoint) gives full read/write
--   access to every row.
--
-- Effect:
--   - anon role: NO access to any row (no policies = default deny).
--   - authenticated role: NO access (no policies = default deny).
--   - service_role: full access (RLS is bypassed for service_role by design).
--
-- FeeHunt's API (server/server.js, functions/api/*.js) uses
-- SUPABASE_SERVICE_ROLE_KEY, so server-side queries continue to work
-- unchanged after this migration. The website (site/script.js) never talks
-- to Supabase directly — it goes through our own /api/* endpoints — so the
-- browser is unaffected.
--
-- Run this in Supabase Dashboard → SQL Editor (one-shot). Idempotent: safe
-- to re-run.
-- =============================================================================

alter table if exists public.users               enable row level security;
alter table if exists public.licenses            enable row level security;
alter table if exists public.devices             enable row level security;
alter table if exists public.email_notifications enable row level security;
alter table if exists public.webhook_events      enable row level security;
alter table if exists public.ai_audit_log        enable row level security;

-- Verify (read-only): every table below should return rowsecurity = true.
-- select schemaname, tablename, rowsecurity
--   from pg_tables
--  where schemaname = 'public'
--    and tablename in ('users','licenses','devices','email_notifications','webhook_events','ai_audit_log')
--  order by tablename;
