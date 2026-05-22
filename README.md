# FeeHunt Beta v1.2

FeeHunt is a Windows beta app for reviewing Gmail subscriptions, payment-risk
emails, newsletters, shop messages, and promotional email. It runs locally on
your computer.

## Free Trial User Flow

1. Open `https://feehunt.pro/signup`.
2. Enter your Gmail or email address.
3. FeeHunt creates a 14-day free trial and emails your license key.
4. Download and install `FeeHunt-Setup-v1.2.exe`.
5. Open FeeHunt from the desktop shortcut.
6. Paste the `FHUNT-...` license key from your email.
7. Click `Connect Gmail`.
8. Sign in with Google and approve Gmail access.
9. Click `Scan Gmail`.

No manual `credentials.json` copying is required in the packaged beta build.
FeeHunt includes its Gmail OAuth app configuration and creates your personal
Google token automatically after sign-in.

The free trial lasts 14 days and does not require a credit card.

## Where Local Data Is Saved

FeeHunt stores user data in:

```text
%APPDATA%\FeeHunt\
```

These files are local user data and must never be packaged in a release:

- `token.json` - your Google OAuth token created after Gmail sign-in.
- `last_scan_results.json` - latest local Gmail scan results.
- `feehunt_settings.json` - local settings and cleanup preferences.
- `feehunt_rules.json` - local cleanup rules.
- `feehunt_license.json` - local license key and latest license check.

The packaged app may include only `credentials.json`, which is the FeeHunt
OAuth client configuration needed to open Google's sign-in flow.

## Run From Source

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

For source development, keep your local `credentials.json` in the project root.
Do not commit tokens, scan results, settings, rules, or license files.

By default the desktop app checks licenses through:

```text
https://feehunt.pro/api
```

For local backend testing, override it before launching FeeHunt:

```powershell
$env:FEEHUNT_API_BASE_URL="http://localhost:8788/api"
streamlit run app.py
```

## Licensing Backend

FeeHunt Phase 1 licensing uses the BeSafe-style Node/Express + Supabase model.
Full setup instructions are in `LICENSING_SETUP.md`.

```powershell
npm install
psql "$env:SUPABASE_DB_URL" -f .\supabase\schema.sql
npm run server
npm run test:e2e
```

Set these production environment variables:

- `FEEHUNT_APP_URL=https://feehunt.pro`
- `FEEHUNT_DOWNLOAD_URL=https://feehunt.pro/download`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `EMAIL_FROM`
- `RESEND_API_KEY` or `SMTP_PASS`
- `STRIPE_SECRET_KEY` later, when paid checkout is enabled.

## Build

```powershell
pyinstaller .\FeeHunt.spec --clean --noconfirm --distpath .\dist_beta --workpath .\build_beta
```

Before publishing, confirm the generated build contains `credentials.json` and
does not contain `token.json`, `last_scan_results.json`,
`feehunt_settings.json`, `feehunt_rules.json`, or `feehunt_license.json`.

## Beta Note

FeeHunt is beta software. Gmail cleanup actions can affect real email, so
review results before archiving, deleting, or marking messages as spam.
