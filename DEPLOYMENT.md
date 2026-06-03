# FeeHunt Website Deployment

This document explains how to publish the static FeeHunt website from the
`site/` folder to `feehunt.pro`.

## Publish Folder

Use this folder as the web root:

```text
site/
```

The static site includes:

- `index.html`
- `pricing.html`
- `signup.html`
- `login.html`
- `account.html`
- `success.html`
- `download.html`
- `faq.html`
- `privacy.html`
- `terms.html`
- `contact.html`
- `feedback.html`
- `styles.css`
- `script.js`
- `.nojekyll`

## Current CTA URLs

- Start Free Trial: `signup.html`
- Login: `login.html`
- Account and Billing: `account.html`
- Download navigation: `download.html`
- Download FeeHunt for Windows: `https://github.com/Antanas7/feehunt-releases/releases/download/v1.12.2/FeeHunt-Setup-v1.12.2.exe`
- Upgrade Plan: `contact.html`
- Send Feedback: `feedback.html` or `mailto:support@feehunt.pro`
- Contact email: `mailto:support@feehunt.pro`

## Installer Hosting

The download page points to:

```text
https://github.com/Antanas7/feehunt-releases/releases/download/v1.12.2/FeeHunt-Setup-v1.12.2.exe
```

Before publishing the updated download page, upload the installer so this URL resolves.

Recommended options:

- Use GitHub Releases and redirect the download button to the release asset.
- Use Cloudflare R2 with a custom public download URL.
- Use Netlify/Cloudflare static assets only if the platform accepts the ZIP size.

Avoid committing large binary release files directly into a normal Git repository.

## GitHub Pages

1. Create a GitHub repository for the website.
2. Copy the contents of `site/` into the repository root, or keep `site/` and configure Pages to publish from that folder if your workflow supports it.
3. Commit and push the files.
4. In GitHub, open **Settings â†’ Pages**.
5. Choose the publishing source, usually:
   - branch: `main`
   - folder: `/root` if the `site/` contents are at repo root
6. Add the custom domain:

```text
feehunt.pro
```

7. In your DNS provider, point `feehunt.pro` to GitHub Pages using GitHub's current Pages DNS instructions.
8. Enable HTTPS in GitHub Pages.
9. Host the installer separately if GitHub rejects the file size.

## Netlify

1. Open Netlify and choose **Add new site**.
2. Connect the repository or drag-and-drop the `site/` folder.
3. If using a repository, set:

```text
Build command: none
Publish directory: site
```

4. Add the custom domain:

```text
feehunt.pro
```

5. Follow Netlify's DNS instructions.
6. Enable HTTPS.
7. Upload or host the installer so `https://github.com/Antanas7/feehunt-releases/releases/download/v1.12.2/FeeHunt-Setup-v1.12.2.exe` resolves, or update the CTA to the final asset URL.

## Cloudflare Pages

1. Open Cloudflare Pages.
2. Create a new Pages project.
3. Connect the repository.
4. Set:

```text
Framework preset: None
Build command: none
Output directory: site
```

5. Deploy the project.
6. Add the custom domain:

```text
feehunt.pro
```

7. Use Cloudflare DNS and enable HTTPS.
8. For the installer, prefer GitHub Releases or Cloudflare R2, then keep the download CTA pointed at the public EXE URL.

## FeeHunt Licensing Backend

FeeHunt Phase 1 licensing follows the BeSafe Node/Express + Supabase model.

Install server dependencies:

```powershell
npm install
```

Apply the Supabase schema:

```powershell
psql "$env:SUPABASE_DB_URL" -f .\supabase\schema.sql
```

Run locally:

```powershell
npm run server
```

Production environment variables:

- `FEEHUNT_APP_URL=https://feehunt.pro`
- `FEEHUNT_DOWNLOAD_URL=https://feehunt.pro/download`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `EMAIL_FROM`
- `RESEND_API_KEY` or SMTP settings
- `STRIPE_SECRET_KEY` later for paid checkout

Reminder emails are sent by calling:

```text
GET https://feehunt.pro/api/check-trials
```

## Recommended Hosting

Recommended path:

1. Cloudflare Pages for the static website.
2. GitHub Releases or Cloudflare R2 for the installer download.
3. Later, connect `/pricing` or `/checkout` to Stripe when payments are ready.

Cloudflare Pages is a strong fit because it pairs well with DNS, HTTPS, custom domains, and future Cloudflare-hosted download assets.

## Pre-Launch Checklist

- Confirm `https://feehunt.pro` opens the landing page.
- Confirm every navigation link works.
- Confirm the Download FeeHunt button resolves to the installer.
- Confirm Privacy Policy and Terms pages are published.
- Confirm Contact and Feedback paths work.
- Confirm HTTPS is enabled.


