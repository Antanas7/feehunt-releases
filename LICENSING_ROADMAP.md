# FeeHunt BeSafe Licensing Integration

FeeHunt now follows the BeSafe licensing model:

1. User enters Gmail/email on `feehunt.pro/signup`.
2. Server creates a 7-day trial in Supabase.
3. Server generates an `FHUNT-XXXX-XXXX-XXXX-XXXX` license key.
4. Server emails the license key to the user.
5. User installs FeeHunt and pastes the key into the desktop app.
6. Desktop app calls `/api/verify-license`.
7. Active trial or paid license unlocks Gmail connection and scanning.
8. Expired trial disables scanning and shows upgrade guidance.

## Implemented

- `server/server.js` Node/Express API adapted from BeSafe.
- `supabase/schema.sql` for users, licenses, devices, reminders, webhook idempotency, and audit log.
- `POST /api/register`
- `POST /api/login` for resending license keys.
- `POST /api/verify-license`
- `GET /api/check-trials`
- `POST /api/create-checkout` placeholder for Stripe paid phase.
- `POST /api/webhook` placeholder for Stripe paid phase.
- Desktop activation by license key.
- 7-day offline grace after last successful verification.

## Production Env

- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `EMAIL_FROM`
- `RESEND_API_KEY` or SMTP settings
- `FEEHUNT_APP_URL`
- `FEEHUNT_DOWNLOAD_URL`
- `STRIPE_SECRET_KEY` later for paid plans

## Phase 2

- Stripe checkout and webhooks.
- Customer billing portal.
- Paid status activation.
- Cancellation/reactivation emails.
