# FeeHunt — rankinio testo scenarijus (v1.12.6)

> Tikslas: uždaryti vienintelį likusį „neperžengtą" gate'ą prieš viešą paleidimą —
> realaus Windows įrenginio + realaus Gmail elgsenos patikra. Inžinerija paruošta
> (32/32 vienetiniai testai žali, DPAPI, atomic writes, Gmail retry). Šis dokumentas
> tikrina tai, ko automatika negali: pirmą įspūdį, OAuth gedimus ir pasitikėjimą.

**Versija:** v1.12.6
**Installer:** `FeeHunt-Setup-v1.12.6.exe`
**Vartotojo duomenų aplankas:** `%APPDATA%\FeeHunt`
**Data:** ____________  **Testuotojas:** ____________  **PC / Windows versija:** ____________

---

## 0. Ko reikia prieš pradedant

- [ ] **Švarus Windows** — nauja Windows vartotojo paskyra, VM arba kito žmogaus PC,
      kuriame FeeHunt **niekada nebuvo įdiegtas** (kad pamatytume tikrą pirmo karto patirtį).
- [ ] **Ne pagrindinis Gmail** — bandomoji Gmail paskyra (arba tokia, kurios nebijai liesti),
      su bent: 1 reklamos laišku, 1 prenumeratos/sąskaitos laišku, 1 „failed payment"/sąskaitos laišku.
- [ ] **Galiojantis licencijos raktas** (tester arba realus).
- [ ] **Antras licencijos raktas** (J fazei — licencijos keitimui). Jei neturi — tą fazę praleisk.
- [ ] **Internetas**, kurį gali laikinai išjungti (H4 testui).
- [ ] **Telefonas nuotraukoms** — fiksuok bet kokią klaidą, kuri rodo techninį tekstą.

> **Bendra „PASS" sąlyga:** netechninis žmogus gali pereiti **aktyvuoti → prijungti Gmail →
> skenuoti → peržiūrėti → atšaukimo kelias** be techninės pagalbos, ir niekur nemato
> tracebacko, „403", „token", „OAuth failed", developerio kompiuterio kelio ar užšalimo.

---

## A. Švarus įdiegimas ir pirmas paleidimas

1. [ ] Atsisiųsk `FeeHunt-Setup-v1.12.6.exe` iš svetainės **Download** mygtuko
       (ne iš tiesioginio failo — tikrinam ir nuorodą).
   - **PASS:** atsisiunčiama būtent **v1.12.6** (ne v1.12.4/v1.12.5). _Žr. pastabą dokumento gale._
2. [ ] Paleisk installer.
   - **Stebėk SmartScreen:** ar rodo „Windows protected your PC / unknown publisher"?
     - ⚠️ Jei taip — užfiksuok. _Tai code-signing blokatorius, ne klaida, bet baido vartotoją._
   - **PASS:** įdiegimas pereina iki galo be klaidų; sukuriamas Start meniu / darbalaukio įrašas.
3. [ ] Paleisk FeeHunt.
   - **PASS:** programa atsidaro **be** „missing DLL", „VCRUNTIME", „python", „ModuleNotFound" ar
     juodo konsolinio lango su klaida. Pirmas ekranas yra suprantamas.
4. [ ] Pasirink kalbą (jei siūloma).
   - **PASS:** sąsaja persijungia visa, be angliškų likučių mišinyje.

**Pastabos / nuotraukos:** ______________________________________________

---

## B. Licencijos aktyvavimas

5. [ ] Įvesk galiojantį licencijos raktą.
   - **PASS:** aiškus „aktyvuota / sėkmė" pranešimas; programa praleidžia toliau.
6. [ ] Įvesk **neteisingą** raktą (vieną kartą tyčia).
   - **PASS:** ramus „raktas neteisingas / patikrink" pranešimas, **ne** raw klaida ar užšalimas.

**Pastabos:** ______________________________________________

---

## C. Gmail prijungimas (laimingas kelias)

7. [ ] Spausk „prijungti Gmail" → atsidaro Google OAuth naršyklėje.
8. [ ] Patvirtink prieigą bandomajai paskyrai.
   - **PASS:** grįžus į FeeHunt rodomas prisijungęs el. paštas; nėra raw redirect klaidos.
9. [ ] **Privatumo patikra (DPAPI):** atidaryk `%APPDATA%\FeeHunt\token.json` Notepad'e.
   - **PASS:** turinys yra **neįskaitomi/šifruoti baitai**, NE atviras JSON su `refresh_token`.
     _(Tai patvirtina token-at-rest šifravimą.)_

**Pastabos:** ______________________________________________

---

## D. Skenavimas (signature moment)

10. [ ] Paleisk skenavimą.
    - **PASS:** rodomas „gyvas" progresas (Žemės gaublys / radaras / realūs skaičiai), o ne
      tuščias spinneris; **nesijaučia užšalimo**.
11. [ ] Palauk iki pabaigos (~200 laiškų partija — tai sąmoninga, ne klaida).
    - **PASS:** skenavimas baigiasi suvestine; aišku, kas rasta ir kiek.

**Skenavimo trukmė:** ______  **Pastabos:** ______________________________________________

---

## E. Kategorizacijos peržiūra

12. [ ] Peržiūrėk rezultatus pagal kategorijas.
    - **PASS:** matosi atskirtos: prenumeratos, mokėjimų kontrolės laiškai (failed/overdue),
      reklaminis triukšmas, phishing signalai.
13. [ ] Atidaryk vieną laišką „Open in Gmail".
    - **PASS:** atsidaro tikras Gmail laiškas naršyklėje.
14. [ ] Patikrink phishing/saugumo signalą (jei yra).
    - **PASS:** saugumo įspėjimas (pvz. Supabase/Dependabot) **nerodomas** kaip „prenumerata,
      kurią reikia atšaukti". Rizikos lygis suprantamas (caution vs danger).

**Pastabos:** ______________________________________________

---

## F. Atšaukimo vedlys / Subscription Control Center (flagman)

15. [ ] Atidaryk vienos realios prenumeratos atšaukimo kelią.
    - **PASS:** FeeHunt veda į **tikrą atšaukimo valdiklį** (paslaugos billing/cancel puslapį),
      o ne į pagalbos/dokumentų puslapį.
16. [ ] **Unsubscribe ≠ cancel patikra:** paimk vieną reklaminį laišką su „unsubscribe".
    - **PASS:** FeeHunt **nerodo** el. laiškų atsisakymo nuorodos kaip mokamos prenumeratos
      atšaukimo. Aiškiai skiria: tiesioginis cancel / billing puslapis / paieškos fallback.
17. [ ] Pereik Control Center „atšaukti juos visus" srautą (bent peržiūrą).
    - **PASS:** jaučiasi kaip vedlys, vedantis iki „atlikta", o ne tik sąrašas.

**Pastabos:** ______________________________________________

---

## G. Realus Gmail veiksmas (saugiai)

18. [ ] Pažymėk **vieną nesvarbų bandomąjį** laišką trinimui („Trinti").
    - **PASS:** prieš veiksmą rodoma **peržiūra + patvirtinimas**; niekas nedaroma tyliai.
19. [ ] Patvirtink trinimą.
    - **PASS:** laiškas atsiranda Gmail **Šiukšliadėžėje** (Trash), ne ištrintas negrįžtamai.
20. [ ] Patikrink, kad nieko kito nepasikeitė be sutikimo.
    - **PASS:** jokių kitų laiškų FeeHunt nepalietė.

**Pastabos:** ______________________________________________

---

## H. OAuth / tinklo gedimų realybė (svarbiausia pasitikėjimui)

> Kiekvienu atveju FeeHunt turi likti **ramus** ir duoti aiškų „prisijunk iš naujo / bandyk dar"
> veiksmą. **FAIL = bet koks** traceback, „403", „invalid token", „OAuth failed", raw Python/Google tekstas.

**H1 — Atmesti leidimą**
21. [ ] Pradėk Gmail prijungimą → Google lange paspausk **Deny / Atmesti**.
    - **PASS:** ramus paaiškinimas + „bandyk prisijungti dar kartą". ____PASS / ____FAIL

**H2 — Uždaryti naršyklę vidury**
22. [ ] Pradėk OAuth → uždaryk naršyklės kortelę nepatvirtinęs.
    - **PASS:** FeeHunt neužšąla; siūlo bandyti vėl. ____PASS / ____FAIL

**H3 — Sugadintas token**
23. [ ] Uždaryk FeeHunt. PowerShell:
```powershell
$dir = Join-Path $env:APPDATA "FeeHunt"
Rename-Item "$dir\token.json" "token.broken.json" -ErrorAction SilentlyContinue
# papildomai: sugadink turinį
"NOT-A-VALID-TOKEN" | Set-Content "$dir\token.json"
```
24. [ ] Atidaryk FeeHunt, bandyk veikti / skenuoti.
    - **PASS:** aiškus „reikia prisijungti iš naujo" kelias, ne raw klaida. ____PASS / ____FAIL
25. [ ] Atstatyk (jei reikia):
```powershell
$dir = Join-Path $env:APPDATA "FeeHunt"
Remove-Item "$dir\token.json" -ErrorAction SilentlyContinue
Rename-Item "$dir\token.broken.json" "token.json" -ErrorAction SilentlyContinue
```

**H4 — Internetas dingsta skenuojant**
26. [ ] Pradėk skenavimą → išjunk Wi‑Fi/tinklą vidury.
    - **PASS:** ramus pranešimas, retry/bandyk vėliau; emails aprašomi kaip saugūs;
      ne „freeze", ne traceback. ____PASS / ____FAIL
27. [ ] Įjunk tinklą atgal, pakartok veiksmą.
    - **PASS:** atsigauna be perkrovimo. ____PASS / ____FAIL

**Pastabos:** ______________________________________________

---

## I. Licencijos keitimas (duomenų izoliacija)

> Praleisk, jei neturi antro rakto.

28. [ ] Pasirink „Use another license key / Naudoti kitą licencijos raktą".
    - **PASS:** senas Gmail ryšys IR vietiniai skenavimo rezultatai **dingsta**.
29. [ ] Aktyvuok kitą raktą.
    - **PASS:** prasideda švari būsena; nematyti senos paskyros duomenų. ____PASS / ____FAIL
30. [ ] (Pasirinktinai) `%APPDATA%\FeeHunt` patikra: senos paskyros `token.json`/
       `last_scan_results.json` nebeturi senų duomenų.

**Pastabos:** ______________________________________________

---

## J. Pastovumas / sugrįžimas po paros

31. [ ] Užbaik skenavimą, uždaryk FeeHunt.
32. [ ] Atidaryk FeeHunt iš naujo (idealiai — kitą dieną).
    - **PASS:** prietaisų skydelis aiškiai parodo paskutinio skenavimo būseną; jaučiasi pažįstamai
      ir stabiliai; vartotojas supranta kitą veiksmą be skaitymo. ____PASS / ____FAIL

**Pastabos:** ______________________________________________

---

## K. Svetainės „Log in" → desktop (`feehunt://open`)

33. [ ] Įdiegtame PC, svetainėje (feehunt.pro) spausk **Log in**.
    - **PASS:** atsidaro įdiegta desktop programa per `feehunt://open`.
34. [ ] PC **be** FeeHunt: ta pati „Download FeeHunt for Windows" nuoroda pasiekia v1.12.6 installer.
    - **PASS:** fallback veikia. ____PASS / ____FAIL

**Pastabos:** ______________________________________________

---

## L. Netechninio žmogaus testas (be paaiškinimų)

35. [ ] Duok programą netechniniam žmogui ir **nieko nepaaiškink**. Stebėk:
    - Kur sustoja / dvejoja / bijo spausti.
    - Ar supranta, kad Gmail saugus.
    - Ar supranta, ką FeeHunt rado.
    - Ar supranta, kas nutiks **prieš** valymą.
    - **PASS:** žmogus pats pereina aktyvuoti → prijungti → skenuoti → peržiūrėti → valymo peržiūra.

**Ką pastebėjai:** ______________________________________________

---

## Rezultatų suvestinė

| Fazė | Tema | PASS / FAIL | Pastaba |
|---|---|---|---|
| A | Švarus įdiegimas + paleidimas | | |
| B | Licencijos aktyvavimas | | |
| C | Gmail prijungimas + DPAPI | | |
| D | Skenavimas | | |
| E | Kategorizacija | | |
| F | Atšaukimo vedlys | | |
| G | Realus trinimo veiksmas | | |
| H1 | OAuth deny | | |
| H2 | Naršyklė uždaryta | | |
| H3 | Sugadintas token | | |
| H4 | Internetas dingsta | | |
| I | Licencijos keitimas | | |
| J | Sugrįžimas po paros | | |
| K | feehunt://open + fallback | | |
| L | Netechninis žmogus | | |

**Bendras verdiktas:** ____ Paruošta viešam paleidimui  ____ Reikia taisymų (žr. žemiau)

**Blokatoriai rasti:**
1. ______________________________________________
2. ______________________________________________
3. ______________________________________________

---

## Žinomi, atskiri nuo šio testo punktai (ne dalis PASS/FAIL)

- **Code-signing:** kol nepasirašytas installer, SmartScreen rodys „unknown publisher". Tikėtina
  A2 fazėje — fiksuok, bet tai atskiras blokatorius (sertifikatas gaunamas atskirai).
- **Google OAuth verification:** vyksta; kol nepatvirtinta, gali matytis „unverified app" Google ekrane.
- **Stripe:** mokėjimai testuojami atskirai test-mode prieš įjungiant.
- **Versijos nuorodos svetainėje:** patikrinta 2026-06-16 — `download.html` rodo v1.12.5, o
  `i18n.js` atsisiuntimo mygtukas v1.12.4, nors naujausia = **v1.12.6**. Prieš A fazę reikia
  suvienodinti svetainės nuorodas su faktiškai į GitHub Releases įkelta v1.12.6.
