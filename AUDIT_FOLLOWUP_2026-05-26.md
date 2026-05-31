# FeeHunt Site Audit Followup - 2026-05-26

Visi rasti dalykai per auditą. Aukšti prioritetai jau pataisyti; čia surašyti likę punktai, kuriuos verta peržiūrėti vėliau.

## Pataisyta šiandien

- Hero security strip (Bank-level security / No servers / Calm Gmail protection) ir social proof eilutė dabar verčiami į LT per `siteTranslations` + `applyHomeTranslation` ([site/script.js](site/script.js)).
- Pridėtas "Start Trial" CTA mygtukas nav-actions juose: contact, feedback, faq, privacy, terms (vietoj "Download Beta").
- Cache buster'ai suvienodinti į `v=20260526-audit-fix-1` visuose 14 svetainės puslapių (styles.css, script.js, i18n.js).
- Pridėti `canonical` + Open Graph + Twitter Card meta tag'ai 13 ne-pradinio puslapių (anksčiau tik index.html juos turėjo).
- Language toggle mygtukas suvienodintas: `🌐 English ▼` su `aria-label="Switch language"` visuose puslapiuose.

## Likę punktai

### IMPORTANT - reikia spręsti prieš public launch

1. **Du paraleliai veikiantys i18n sistemos** ([site/script.js](site/script.js) + [site/i18n.js](site/i18n.js))
   - `script.js` turi `siteTranslations` ir per-page `apply*Translation` funkcijas
   - `i18n.js` turi `FH_I18N` su tais pačiais turiniais, bet nematomi `apply*` skambinimai
   - Kiekvienas puslapis load'ina **abu** skriptus
   - **Sprendimas:** apsispręsti, kuris yra canonical (rekomenduoju siteTranslations, nes turi veikiančias apply funkcijas), kitą pašalinti
   - Rizika: gali būti, kad i18n.js pridėtas naujesnis ir buvo planuojama migracija

2. **success.html turi hardcoded LT kortelę alongside EN**
   - [site/success.html:55-63](site/success.html#L55) — antra kortelė "Kas toliau" su LT turiniu rendered nuolat (be runtime perjungimo)
   - Puslapis neturi `applySuccessTranslation` script.js'e, todėl LT vartotojui matosi: angliški hero + EN kortelė + LT kortelė
   - **Sprendimas:** arba pridėti success page handler į script.js (su FH_I18N.lt.success duomenimis kurie jau yra), arba pašalinti LT kortelę ir leisti rodyti tik EN

3. **pricing.html "Upgrade Plan" mygtukas rodo į contact.html**
   - [site/pricing.html:22](site/pricing.html#L22) — nav-actions button href="contact.html" su label "Upgrade Plan"
   - Tikriausiai turėtų rodyti į account.html arba tiesiai į Stripe portal
   - **Sprendimas:** patikrinti, kas turi būti — jei flow yra "klientas → contact us to upgrade", tai OK; jei self-service portal — keisti į account.html

### NICE-TO-HAVE - polish'as

4. **Footer "Terms" vs "Terms of Service" nesutapimas**
   - Pages account.html, login.html, dashboard.html, forgot-password.html, success.html, privacy.html: rodo "Terms"
   - Pages contact.html, feedback.html, pricing.html, ir kiti: rodo "Terms of Service"
   - **Sprendimas:** vienodinti į "Terms" (trumpiau, švelnesnis tonas) arba "Terms of Service" (formalu)
   - Lengva pataisyti per PowerShell bulk replace

5. **Form accessibility - signup.html `<label>` ne susieta su input**
   - [site/signup.html](site/signup.html) plan select dropdown'as turi label wrapping, bet trūksta explicit `for`/`id` susiejimo
   - **Sprendimas:** pridėti `id="signup-plan"` ant `<select>` ir `for="signup-plan"` ant `<label>`
   - Tas pats su email/license key input'ais

6. **Hero security strip dabar `grid-column: 2`** ([site/styles.css:1129](site/styles.css#L1129))
   - Anksčiau buvo `grid-column: 1 / -1` (per visą eilę), bet tai sukėlė overlap'ą su social proof tekstu kairėje
   - Po fix'o (mūsų ankstesnėje sesijoje) yra tik dešinėje pusėje
   - Atskirai @media (max-width: 980px) breakpoint'e turi senesnį styling'ą su hardcoded `left: 220px`
   - **Sprendimas:** patikrinti mobile breakpoint (puslapis < 980px plotis) — gali būti, kad reikės papildomo derinimo

7. **i18n.js cache buster `20260526-lt-diacritics`**
   - Po mūsų bulk update visi cache buster'iai standartizuoti į `audit-fix-1`, įskaitant i18n.js
   - Jei i18n.js bus pakeičiamas vėliau, reikės naujo cache buster'io versioning konvencijos

### Document only - architectural

8. **site/script.js yra labai didelis (~73 KB, 1300+ eilučių)**
   - Visa logika viename faile (i18n, page-specific handlers, hero animations, Stripe integration, language detection)
   - **Sprendimas:** ateityje verta išdalinti į module'ius (translations.js, hero.js, pages/{home,signup,...}.js), bet tai didesnis refactor

9. **Daug puslapių su minify'intu HTML (vienoje eilutėje)**
   - contact.html, faq.html, feedback.html, privacy.html, terms.html — visas HTML vienoje eilutėje, sunku editinti rankomis
   - **Sprendimas:** ateityje gražinti prettify'intą HTML su Prettier ar VS Code "Format Document", kad PRs būtų lengviau review'inti

## Lokali patikra

Po visų pataisymų svetainė available'i [http://localhost:8765/](http://localhost:8765/). Konkrečiai patikrinti:

- [ ] LT mode'as: hero security strip dabar turi "Banko lygio saugumas", "Be serverių. Be sekimo.", "Rami Gmail apsauga"
- [ ] LT mode'as: social proof eilutė rodo "Prisijunkite prie 1 000+ vartotojų..."
- [ ] Nav: contact/feedback/faq/privacy/terms puslapių nav viršuje yra "Start Trial" žalias mygtukas
- [ ] Cache: visi puslapiai naudoja `?v=20260526-audit-fix-1` (vienas refresh ir viskas naujausia)
- [ ] HTML head: kiekvienas puslapis turi canonical + og: + twitter: meta tag'us (peržiūrėti per Inspect Element)
- [ ] Language toggle: visi puslapiai turi vienodą "🌐 English ▼" su accessibility label
