# FeeHunt Beta Readiness Report

Date: 2026-05-22
Build: FeeHunt-Beta-v1.2.0-20260522.zip
SHA256: 3D68062EFC39FFB8511E40329B2C42F5182733BDC1C7A68C94FD509B5AA5FB0B

## Verdict

Status: Not ready for public beta until real-environment tests pass.

Engineering build status: Ready for clean-machine validation.

The fresh package was built from the current stabilized codebase and passed local release hygiene checks. The remaining gates require a real Windows environment and human observation.

## Critical Blockers

| Area | Status | Notes |
|---|---|---|
| Fresh beta build | Passed | New PyInstaller output created in `dist_beta/FeeHunt`. |
| Release ZIP | Passed | Created `FeeHunt-Beta-v1.2.0-20260522.zip`. |
| Sensitive data in ZIP | Passed | No `token.json`, scan results, memory, cleanup rules, license/session files, `.env`, or logs found. |
| Clean machine install/run | Not tested | Must be tested on a new Windows user, VM, or different PC. |
| OAuth failure reality | Not tested | Must be tested with deny, closed browser, corrupted token, reconnect, and internet interruption. |
| Real unsubscribe path | Not tested | Must be tested with a real subscription email. |
| Windows Defender scan | Inconclusive | Local `Start-MpScan` was blocked or timed out in this environment. Run manually on the target machine. |

## Important Polish

| Area | Status | Notes |
|---|---|---|
| Language readiness | Improved | User-facing Streamlit text is routed through translations for the audited paths. |
| Plan naming | Fixed | `basic` is the canonical plan. Legacy `personal` is treated as `basic`. |
| Gmail plan limits | Improved | Local Gmail account registration now respects plan account limits. |
| Destructive Gmail actions | Improved | Unused permanent-delete API helper was removed. Current delete flow uses Gmail trash. |
| Cleanup preview | Working | Bulk cleanup uses preview and confirmation before applying changes. |

## Trust Risks To Validate

1. Gmail OAuth denial must show calm guidance, not raw Google/Python errors.
2. Corrupted or expired token must lead to a clear reconnect path.
3. Scan must keep living feedback visible and avoid freeze perception.
4. Unsubscribe flow must make it clear whether FeeHunt found a direct unsubscribe link, a billing/help page, or a search fallback.
5. Reopening the app after one day must feel familiar and stable.

## Clean Machine Test Script

Use a new Windows user profile, VM, or another person's Windows PC.

1. Download `FeeHunt-Beta-v1.2.0-20260522.zip`.
2. Extract all files.
3. Open `FeeHunt.exe`.
4. Select language.
5. Activate license.
6. Connect Gmail.
7. Scan Gmail.
8. Review subscriptions.
9. Open one email in Gmail.
10. Open unsubscribe path for one real subscription.
11. Open Cleanup Rules.
12. Run cleanup preview.
13. Do not apply destructive actions unless intentionally testing with a safe account.
14. Close FeeHunt.
15. Reopen FeeHunt.

Record:

- Missing dependency or DLL errors.
- OAuth redirect issues.
- Any path that mentions the developer machine.
- Any raw traceback or technical error.
- Any app freeze or no-feedback waiting moment.
- Any user confusion.

## OAuth Failure Reality Test

Test with a non-critical Gmail account if possible.

Cases:

1. Deny Gmail permission in Google OAuth.
2. Start OAuth, then close the browser.
3. Corrupt token:

```powershell
$dir = Join-Path $env:APPDATA "FeeHunt"
Rename-Item "$dir\token.json" "token.broken.json" -ErrorAction SilentlyContinue
```

4. Reopen FeeHunt and attempt reconnect.
5. Restore token if needed:

```powershell
$dir = Join-Path $env:APPDATA "FeeHunt"
Rename-Item "$dir\token.broken.json" "token.json" -ErrorAction SilentlyContinue
```

6. Disconnect internet during scan and observe messaging.

Expected result:

- FeeHunt stays calm.
- Emails are described as safe.
- User gets a clear reconnect or retry action.
- No traceback, invalid token, OAuth failed, or 403 raw text is shown.

## Real Subscription Test

Use a real subscription email in Gmail.

Validate:

- Subscription appears in review.
- Open in Gmail works.
- Direct unsubscribe opens if available.
- If no direct unsubscribe exists, fallback is understandable.
- User can distinguish direct unsubscribe, billing/help page, and search cancellation options.
- FeeHunt does not change Gmail without explicit confirmation.

## 24-Hour Return Test

1. Complete a scan.
2. Close FeeHunt.
3. Return next day.
4. Reopen FeeHunt.

Validate:

- Dashboard still explains what matters.
- Last scan state is clear.
- Local memory feels helpful, not invasive.
- User knows the next action without reading too much.

## Non-Technical Human Test

Give the app to a non-technical person and do not explain the product.

Watch for:

- Where they stop.
- Where they hesitate.
- What they are afraid to click.
- Whether they understand Gmail safety.
- Whether they understand what FeeHunt found.
- Whether they understand what will happen before cleanup.

Pass condition:

The person can complete activate, connect, scan, review, and cleanup preview without technical guidance.

## Stability Score

Current engineering confidence: 7.5 / 10

Reason:

- Build and release hygiene are good.
- Core safety flows are in place.
- Clean-machine and real OAuth failure behavior are not yet proven.
- Stripe checkout/webhook is not enabled yet and should remain out of beta unless explicitly tested.

## Next Gate

Run the clean-machine test with `FeeHunt-Beta-v1.2.0-20260522.zip`.

Only after that test passes should this package be shared with first beta users.
