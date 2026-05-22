# FeeHunt Supabase + Resend Setup

Šis dokumentas skirtas vienam tikslui: užpildyti `.env`, paleisti Supabase lenteles ir patikrinti visą trial kelią.

Galutinis srautas:

1. Vartotojas įveda Gmail / el. paštą.
2. FeeHunt sukuria 14 dienų trial.
3. FeeHunt išsiunčia licencijos raktą el. paštu.
4. Vartotojas įklijuoja raktą FeeHunt programoje.
5. Programa patikrina licenciją per `/api/verify-license`.

## 1. Sukurk `.env`

Projekto šakniniame aplanke nukopijuok:

```powershell
Copy-Item .\.env.example .\.env
```

Tada atidaryk `.env` ir užpildyk reikšmes.

## 2. Supabase Reikšmės

Supabase dashboard:

1. Atidaryk savo Supabase projektą.
2. Eik į **Project Settings -> API**.
3. Nukopijuok **Project URL**.
4. Įrašyk į `.env`:

```env
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
```

Tame pačiame puslapyje rask **service_role** key.

Įrašyk:

```env
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY
```

Svarbu: `service_role` yra slaptas serverio raktas. Jo negalima dėti į frontend JavaScript ar viešinti GitHub.

`SUPABASE_SERVICE_KEY` gali likti tuščias:

```env
SUPABASE_SERVICE_KEY=
```

## 3. Supabase SQL Schema

Atidaryk failą:

```text
supabase/schema.sql
```

Supabase dashboard:

1. Eik į **SQL Editor**.
2. Spausk **New query**.
3. Įklijuok visą `supabase/schema.sql` turinį.
4. Spausk **Run**.

Po paleidimo Supabase turi atsirasti lentelės:

- `users`
- `licenses`
- `devices`
- `email_notifications`
- `webhook_events`
- `ai_audit_log`

Alternatyva su `psql`, jei jis įdiegtas:

```powershell
psql "$env:SUPABASE_DB_URL" -f .\supabase\schema.sql
```

## 4. Resend / SMTP Reikšmės

Resend dashboard:

1. Sukurk arba atidaryk Resend paskyrą.
2. Eik į **Domains**.
3. Pridėk `feehunt.pro`.
4. Patvirtink DNS įrašus Cloudflare DNS.
5. Eik į **API Keys**.
6. Sukurk API key.

`.env` faile įrašyk:

```env
RESEND_API_KEY=re_YOUR_RESEND_API_KEY
EMAIL_FROM=support@feehunt.pro
```

`EMAIL_FROM` turi būti iš patvirtinto Resend domeno.

Numatytos SMTP reikšmės Resend:

```env
SMTP_HOST=smtp.resend.com
SMTP_PORT=465
SMTP_SECURE=true
SMTP_USER=resend
SMTP_PASS=
```

Jei naudoji `RESEND_API_KEY`, `SMTP_PASS` gali likti tuščias.

## 5. Kiti Būtini Kintamieji

`.env` turi turėti:

```env
NODE_ENV=development
PORT=3001
FEEHUNT_APP_URL=https://feehunt.pro
FEEHUNT_DOWNLOAD_URL=https://feehunt.pro/download
```

Stripe Phase 1 nereikalingas:

```env
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_PRICE_BASIC_MONTHLY=
STRIPE_PRICE_FAMILY_MONTHLY=
STRIPE_PRICE_PRO_MONTHLY=
```

## 6. Įdiek Priklausomybes

PowerShell aplinkoje naudok `npm.cmd`, nes `npm.ps1` kartais blokuojamas Windows Execution Policy.

```powershell
npm.cmd install
```

## 7. Paleisk Serverį

```powershell
npm.cmd run server
```

Serveris turi rodyti:

```text
FeeHunt licensing server running on http://127.0.0.1:3001
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:3001/api/health
```

Tikėtina:

```text
api       : ok
supabase  : ok
```

## 8. E2E Testas

Atidaryk antrą terminalą.

Įrašyk testinį email, kurį gali realiai patikrinti:

```powershell
$env:FEEHUNT_E2E_EMAIL="tavo-test-email@domain.com"
npm.cmd run test:e2e
```

Tikėtinas rezultatas:

```text
[e2e] Registering trial...
[e2e] register-trial: ok
[e2e] Resending license key via login endpoint
[e2e] login/resend: ok
[e2e] Verifying license key
[e2e] verify-license: trial
[e2e] SUCCESS
```

Tada patikrink inbox:

- turi ateiti welcome email,
- email turi turėti `FHUNT-XXXX-XXXX-XXXX-XXXX` licencijos raktą.

## 9. FeeHunt Desktop Testas

Jei testuoji lokaliai:

```powershell
$env:FEEHUNT_API_BASE_URL="http://127.0.0.1:3001/api"
streamlit run app.py
```

Programoje:

1. Įklijuok `FHUNT-...` licencijos raktą.
2. Spausk **Activate FeeHunt**.
3. Turi atsirasti žinutė, kad FeeHunt aktyvuotas.
4. Spausk **Connect Gmail**.
5. Prisijunk per Google.
6. Spausk **Scan Gmail**.

## Draugiškos Klaidos

Jei Supabase dar nesukonfigūruotas, API grąžins:

```text
FeeHunt account setup is not finished yet. Please contact support@feehunt.pro.
```

Jei email neteisingas:

```text
Please enter a valid Gmail or email address.
```

Jei licencijos raktas neteisingas:

```text
Missing or invalid license key.
```

Jei trial baigėsi:

```text
Your 14-day trial has ended.
```

Trumpai: dabar reikia užpildyti `.env` ir paleisti `supabase/schema.sql`. Tada bus galima testuoti visą kelią.
