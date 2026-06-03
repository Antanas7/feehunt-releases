alter table public.users
  alter column trial_ends_at set default (now() + interval '7 days');

alter table public.licenses
  alter column trial_ends_at set default (now() + interval '7 days');
