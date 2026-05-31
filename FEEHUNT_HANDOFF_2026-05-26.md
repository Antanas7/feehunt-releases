# FeeHunt handoff - 2026-05-26

## Dabartine kryptis

FeeHunt jau juda nuo paprasto aptikimo link tikro pagalbininko:

- ne tik "radau prenumerata", bet "padedu suprasti ir atidaryti saugiausia kita zingsni";
- ne tik "radau rizikinga laiska", bet "padedu islaikyti mokejimu kontrole";
- ne tik "radau reklamas", bet "padedu ramiai sutvarkyti el. pasto triuksma".

Pagrindinis produkto tonas: ramus, aiskus, kontrolę paliekantis vartotojui.

## Kas jau padaryta

- Dashboard ir rezultatu perziura sutvarkyta, pasalinti dubliuojami mygtukai.
- Veiksmu mygtukai geriau sulygiuoti.
- Skenavimo rezultatu virsutines ir apatines metrikos sulygintos.
- Streamlit `main_navigation` perspejimas sutvarkytas.
- Vieša svetaine isversta i kelias kalbas:
  - English
  - Lietuviu
  - Norsk
  - Espanol
  - Deutsch
  - Francais
- Pridetas saugus Stripe Checkout endpoint.
- Pridetas saugus Stripe Customer Portal / cancel flow.
- Pridetas daugiakalbis frontend i18n pagrindiniams puslapiams.
- SEO pagerintas pagrindiniame puslapyje.
- FAQ, pricing, privacy, terms, contact, feedback, download puslapiai pritaikyti LT ir kitoms kalboms.
- Rezultatu kortelese pridetas action-first FeeHunt pagalbininko blokas.
- `mokėjimų priminimai` pakeista i profesionalesni tona: `Mokėjimų kontrolė`.
- Naujas `FeeHunt.exe` perbuildintas ir patikrintas, kad lokaliai startuoja.

## Dabartinis FeeHunt veidas

Kortele turi padeti vartotojui per kelias sekundes suprasti:

1. Kas cia galimai yra.
2. Kodel tai svarbu.
3. Koks saugiausias kitas zingsnis.
4. Kad Gmail nebus keiciamas be patvirtinimo.

Pavyzdinis tonas:

- "Tai gali būti pasikartojanti prenumerata."
- "Saugiausias žingsnis: atidaryti atsisakymo arba mokėjimų puslapį."
- "Prieš spręsdami galite peržiūrėti susijusius mokėjimų laiškus."
- "FeeHunt padeda išlikti saugiai; Gmail nekeičiamas be jūsų patvirtinimo."
- "Jei šiandien tai nesvarbu, galite saugiai palikti ramybėje."

## Rytoj verta patikrinti

1. Paleisti nauja `dist\FeeHunt\FeeHunt.exe`.
2. Prisijungti su Gmail.
3. Paleisti realu scan.
4. Patikrinti 3 kategorijas:
   - Prenumeratos
   - Mokėjimų kontrolė
   - Reklaminiai laiškai
5. Kiekvienoje korteleje ivertinti:
   - ar tekstas ne per ilgas;
   - ar vartotojas per 3 sekundes supranta prasme;
   - ar saugiausias veiksmas matomas;
   - ar Gmail paieskos mygtukas naudingas;
   - ar seni veiksmai vis dar veikia.

## Galimi kiti patobulinimai

- Dar labiau sutrumpinti korteliu tekstus, jei realiuose rezultatuose atrodo per daug.
- Prideti aiškesnius statusus:
  - "Verta patikrinti"
  - "Galima sutvarkyti veliau"
  - "Saugus veiksmas"
- Sukurti trumpa "ka daryti toliau" mikro-vedli:
  - "Patikrinkite mokėjimą"
  - "Atidarykite susijusius laiškus"
  - "Atšaukite, jei nebenaudojate"
- Patikrinti ar visos kalbos turi naturalu tona, ne tik tiesiogini vertima.
- Padaryti maza "trust checklist" pirmam vartotojo paleidimui:
  - Gmail lieka jusu kompiuteryje
  - Veiksmai vyksta tik po patvirtinimo
  - Galite bet kada atsaukti plana

## Svarbu neliesti be reikalo

- Stripe price IDs
- Stripe webhook logika
- Supabase subscription/license logika
- Gmail veiksmu API
- Plan values: `basic`, `family`
- Vidiniai techniniai raktai, pvz. `financial_risks`

## Dabartine komanda build patikrai

```powershell
& 'C:\Users\Rasa Zuikis\AppData\Local\Programs\Python\Python314\python.exe' -m PyInstaller --noconfirm --clean FeeHunt.spec
```

Jei build sustoja del `dist\FeeHunt` failu, pirmiausia uzdaryti veikianti `FeeHunt.exe`.

