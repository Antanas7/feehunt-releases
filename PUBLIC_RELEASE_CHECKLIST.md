# FeeHunt Public Release Checklist

Release candidate: `v1.12.2`

Local installer SHA-256:
`9BBB777B5FF80CEFE8D84EBE8CEE149790F7A5B3FA2386E4CFD553A0B6C50E4E`

## Local Engineering Gates

- [x] Desktop translations are complete for English, Lithuanian, Norwegian,
  Spanish, German, and French.
- [x] Unit tests cover translation completeness, phishing risk levels,
  cancellation-link selection, saved subscription status, and Gmail-token
  cleanup when switching license holders.
- [x] Packaged desktop files exclude user tokens, local scan results, settings,
  memory, cleanup rules, license data, and environment files.
- [x] The production health endpoint reports API, Supabase, and email as ready.
- [x] Website login offers `feehunt://open` first and keeps download as a
  separate fallback for computers where FeeHunt is not installed yet.
- [ ] Apply `supabase/2026-06-02-trial-default-7-days.sql` to production so
  database fallback defaults match the 7-day trial used by the API.
- [x] Rebuild `dist_v1122\FeeHunt` from the frozen source with PyInstaller.
- [x] Re-run the packaged-file privacy audit against `dist_v1122\FeeHunt`.
- [x] Compile `FeeHunt-Setup-v1.12.2.exe` from `dist_v1122\FeeHunt`.
- [x] Upload the installer to GitHub Releases under tag `v1.12.2`.
- [x] Deploy the prepared `site\download.html` only after the GitHub asset exists.

## External Public-Launch Gates

- [ ] Submit and complete Google OAuth verification for the restricted
  `gmail.modify` scope used by FeeHunt.
- [ ] Obtain a Windows code-signing path and sign the public installer.
- [ ] Replace the published Privacy Policy and Terms drafts with reviewed final
  text before commercial launch.
- [ ] Run a clean-machine Windows install test.
- [ ] After installing `v1.12.2`, verify that the website `Log in` flow opens
  the installed desktop app through `feehunt://open`.
- [ ] In the installed app, use `Use another license key`, confirm that the old
  Gmail connection and local results disappear, then activate a different key.
- [ ] Verify the fallback path: on a computer without FeeHunt installed,
  `Download FeeHunt for Windows` still reaches the `v1.12.2` installer.
- [ ] Run a real Gmail inbox test: connect, scan, review phishing signals,
  open a cancellation path, trash a selected test email, close, and reopen.
- [ ] Verify Stripe Checkout, webhook events, Billing Portal, and cancellation
  with test-mode payments before enabling paid billing.

## Language Scope

Ship the first public release with the six complete languages above. Add new
languages only after this checklist passes and the support load is understood.
Polish and Portuguese are sensible candidates for the next localization batch.
