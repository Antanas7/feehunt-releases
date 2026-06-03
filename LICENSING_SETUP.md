# FeeHunt Licensing Setup

This is the BeSafe-style Phase 1 trial system:

1. User enters Gmail/email on `feehunt.pro/signup`.
2. FeeHunt creates a 7-day trial in Supabase.
3. FeeHunt emails an `FHUNT-XXXX-XXXX-XXXX-XXXX` license key.
4. User pastes the key into the FeeHunt Windows app.
5. Desktop app verifies the license through `/api/verify-license`.

## 1. Supabase

1. Create a Supabase project.
2. Open **Project Settings -> API**.
3. Copy:
   - Project URL -> `SUPABASE_URL`
   - `service_role` key -> `SUPABASE_SERVICE_KEY`
4. Open **Project Settings -> Database -> Connection string**.
5. Copy the URI connection string -> `SUPABASE_DB_URL`.
6. Copy `.env.example` to `.env` and fill in those values.
7. Apply the schema:

```powershell
psql "$env:SUPABASE_DB_URL" -f .\supabase\schema.sql
```

If `psql` is not installed, paste the contents of `supabase/schema.sql` into
Supabase **SQL Editor** and run it there.

## 2. Resend

1. Create a Resend account.
2. Add and verify the domain `feehunt.pro`.
3. Create an API key.
4. Set:

```text
RESEND_API_KEY=re_...
EMAIL_FROM=support@feehunt.pro
```

The sender email must belong to a verified Resend domain.

## 3. Local Server

```powershell
npm install
npm run server
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:3001/api/health
```

## 4. End-to-End Test

Use an email inbox you can access:

```powershell
$env:FEEHUNT_E2E_EMAIL="your-test-email@example.com"
npm run test:e2e
```

Expected result:

- `/api/register-trial` creates a trial.
- Welcome email with the license key is sent.
- `/api/login` can resend the license key.
- `/api/verify-license` returns `trial` or `active`.

## 5. Desktop App Test

Start FeeHunt with the local licensing API:

```powershell
$env:FEEHUNT_API_BASE_URL="http://127.0.0.1:3001/api"
streamlit run app.py
```

Then:

1. Paste the `FHUNT-...` license key.
2. Confirm FeeHunt activates.
3. Click `Connect Gmail`.
4. Click `Scan Gmail`.

## Production

Set the same environment variables in the production host:

- `FEEHUNT_APP_URL=https://feehunt.pro`
- `FEEHUNT_DOWNLOAD_URL=https://feehunt.pro/download`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `EMAIL_FROM`
- `RESEND_API_KEY`
- `STRIPE_SECRET_KEY` later for paid checkout
