# Valdymo centro testavimas — Antano pastebėjimai (2026-05-31)

Kontekstas: testuojama 🚦 Prenumeratų valdymo centro versija (vedlio eilė + statusai)
su realiomis Gmail dėžutėmis (Antano `lofotendreamss` + žmonos `rasyte7777a`).
DEV atrakinimas + testuotojų režimas įjungti. Serveris: http://localhost:8501

Žymėjimas: 🐞 bug · 🎯 tikslumo problema (nuoroda nuveda ne ten) · 🧭 UX/aiškumas ·
✅ veikia gerai · 💡 idėja

---

## Pastebėjimai

<!-- Čia kaupiami Antano komentarai testuojant. Kiekvienas su laiku/kategorija. -->

### 1. Žmonos dėžutė užversta šlamštu — sunku susigaudyti
🧭 / ✅ — Antanas testuodamas „pasiklysta tarp ją užpuolusio šlamšto". FeeHunt
„dirba iš peties" (teigiamai). Įžvalga: pats kūrėjas pasimeta žmonos dėžutės
triukšme → tai stipriausias įrodymas, kodėl FeeHunt reikalingas paprastam žmogui.
Galimas veiksmas: ar valdymo centras/rezultatai pakankamai *suvaldo* didelį kiekį
(grupavimas, prioritetai), kad vartotojas NEpasimestų. Sektina su konkrečiu ekranu.
(Antanas paminėjo ekrano kopiją, bet ji neatėjo — laukiu jos.)

### 2. Reklamų masinis valymas — 122 laiškai vienu veiksmu ✅
✅ — Reklaminių laiškų puslapyje vienu veiksmu į Gmail šiukšlinę perkelta **122**
laiškai, su „Atšaukti veiksmą" (undo). Po to puslapis rodo „Reklaminių laiškų
nerasta" — švaru. Antanas: „štai kiek pavyko vienu metu ištrinti." Stiprus valymo
ramsčio patvirtinimas: saugu (grįžtama) + galinga.

### 3. „Teach unwanted" užuomina JAU rodoma šiame puslapyje 💡
💡 — Po valymu rodoma: „Nematote kažkurio nepageidaujamo siuntėjo? ...pridėkite jį
į nepageidaujamų sąrašą, ir kitą skenavimą FeeHunt sutvarkys automatiškai →
Atidaryti Siuntėjų valdymą". T.y. [[feehunt-teach-unwanted-loop]] pamatas dar
labiau gyvas nei manyta — yra nuoroda. SPRAGA lieka tik *friction*: dabar reikia
eiti į Siuntėjų valdymą ir įvesti ranka; trūksta vieno paspaudimo TIESIAI ant
laiško kortelės („🚫 ir šito nenoriu"). Tai patikslina kitą feature'į.

### 4. Valymas saugus — svarbūs laiškai NEpaliesti ✅
✅ — Antanas patvirtino: 122 reklamos pašalintos „FeeHunt sistemos saugiai,
nepaliesta kitų svarbių laiškų". Patvirtina tikslumą (tik triukšmas) + apsaugą
(whitelist/protected senders veikia) + grįžtamumą (undo). Tai pamatinis
pasitikėjimo pažadas — vienas netyčia ištrintas svarbus laiškas sugriautų jį
visam laikui. Veikia kaip turi.

### 5. Antras skenas vis dar randa šiukšlių — kelių praėjimų valymas 🧭
🧭 / ✅ — Po pirmo valymo (122) antras skenavimas VĖL randa reklamų. Priežastis:
kiekvienas skenas apima ~200 naujausių laiškų (MAX_EMAILS_TO_SCAN). Labai
užkimštai dėžutei tai reiškia kelis praėjimus. Antanas: „FeeHunt vis dar valo
šiukšles." Teigiama: FeeHunt nuoseklus ir nepasiduoda, saugiai kapoja krūvą.
GALIMAS PATOBULINIMAS: heavy-inbox atveju apsvarstyti „gilų/tęstinį valymą"
(skenuoti kol švaru) arba aiškesnį „liko dar — skenuok dar kartą" progresą su
likusiu kiekiu, kad vartotojas suprastų, jog reikia kelių kartų, o ne kad „baigta".
Konkretus įrodymas, kad valymas tirpdo krūvą: reklamų skaičius per skenus
**147 → (ištrinta 122) → 48** žmonos dėžutėje. Aiškiai mažėja.

---

## Iš to kylantys veiksmai (punch-list)

<!-- Distiliuoti taisytini dalykai, kuriuos spręsim po testo. -->

### A. Skenavimo riba — SPRENDIMAS: palikti ~200, jokio bulk valymo
**Antano sprendimas (2026-05-31, svarbus):** ~200/kartą riba yra GERA SAVYBĖ, ne
trūkumas. Atmestas mano ankstesnis „gilus valymas vienu ypu" — jis efektyvus, bet
bedvasis: vienu paspaudimu ištrini viską ir uždarai → nelieka ryšio, nelieka
pajausto naudos. Porcijos + grįžimas = ritualas/santykis; vartotojas JAUČIA, kad
FeeHunt dirba už jį. Dvasia = [[feehunt-scan-signature-moment]].

Antanas svarstė net 100/kartą („atidžiau tikrina kiekvieną man"). Claude nuomonė:
palikti ~200 — su 100 tūkstančiams reikėtų 20+ praėjimų → rizika pavargti. Norimą
„dirba sunkiai už mane" jausmą duoti per PATIRTĮ, ne per skaičių (pvz. animacijoje
„peržiūriu 47 iš 200...", sustiprinti gaublio/radaro per-laiško triūsą).

REALUS DARBAS čia (vietoj bulk valymo): **pajaustas progresas**, kad multi-pass
jaustųsi kaip PERGALĖ, ne Sizifo darbas — mažėjantis skaičius, „dėžutė kvėpuoja
laisviau", sesijos suma („šįkart sutvarkei 122"). Tai vienintelis pavojus, nuo
kurio saugotis: kartojimas turi jaustis „laimiu", ne „niekada nesibaigia".

### B. Vartotojo pasirenkamas skenavimo kiekis (Antano idėja — DAROM)
**Antano sprendimas (2026-05-31), išsprendžia 100-vs-200 ginčą:** vietoj to, kad
MES nuspręstume skaičių, leisti VARTOTOJUI pasirinkti — pasirinkimo kortelė
50 / 100 / 200. Tai patobulinimas, ne kompromisas: tiesiogiai stiprina kontrolės
ramstį ([[feehunt-product-principles]]) + dalyvavimo jausmą; savaime prisitaiko
(tvarkinga dėžutė → 50, paskendusi → 200); lieka ritualo filosofijoje (riba ~200,
jokio bulk „deep clean" — žr. [[feehunt-scan-batch-is-deliberate]]).
**Įgyvendinimas:** MAX_EMAILS_TO_SCAN tampa konfigūruojamas (settings) per UI.
Detalės, kad būtų tobula:
- numatytasis pažymėtas (100 ar 200), kad nenorintis galvoti tiesiog skenuotų;
- jausmo etiketės, ne tik skaičiai: „⚡ Greitas žvilgsnis · 50 / 🔍 Įprastas · 100
  / 🧹 Gilesnis · 200";
- įsiminti pasirinkimą (settings), nerinkti kas kartą;
- subtili kortelė prie „Skenuoti" mygtuko (matoma, ne kelyje);
- riba ~200 (neleisti daugiau).
Mažas, elegantiškas, on-brand. Kandidatas iškart po valdymo centro commit'o.

### C. Pašalinti nuolatinį „Atšaukti veiksmą" undo mygtuką po masinio valymo
**Antano sprendimas (2026-05-31):** nuolatinis „Atšaukti veiksmą" mygtukas po
reklamų valymo yra perteklinis ir klaidinantis — sėja abejonę ir kerta pergalės
jausmą. Logika tvirta: (1) laiškai NEištrinami visam, tik perkeliami į Gmail
šiukšlinę (30 d.); (2) atkūrimo kelias jau egzistuoja — vartotojo Gmail šiukšlinė.
Tad atskiro in-app undo nereikia. ŠALINAM mygtuką.
**PATVIRTINTA (Antanas, 2026-05-31):** vietoj mygtuko — informacinis sakinys, kuris
yra FeeHunt RIBŲ pareiškimas, ne tik nuraminimas. Esmė: „Tavo laiškai perkelti į
Gmail šiukšlinę. FeeHunt nieko netrina visam, neperžengia ribų — gali pasitikrinti
ir susigrąžinti pats." Po kiekvieno veiksmo vartotojas mato, kad FeeHunt dirba
skaidriai ir negrįžtamai nieko nedaro → stiprina pasitikėjimą (ne abejonę).
Atitinka [[feehunt-product-principles]] (jokių nematomų veiksmų, vartotojas valdo).
NB: tai liečia masinio valymo undo; per-laiško veiksmų grįžimas (render_recent_
trash_undo / restore_trashed_email) — atskira, NELIEČIAM be atskiro sprendimo.
PADARYTA 2026-05-31: render_recent_trash_undo (app.py) — mygtukas pašalintas,
pridėtas safe_action.trash_reassurance sakinys EN+LT.

### D. Du „Skenuoti dar kartą" mygtukai švarioje dėžutėje — PADARYTA
🐞 — Kai nėra radinių (švari dėžutė), rodėsi DU rescan mygtukai: siauras viršutinis
(stulpelis [3,2] → tuščia kairė + siauras radaras) IR platus apatinis. Antanas
nori plataus. Pataisyta: show_dashboard_hero_action_layer (app.py ~4830) — siaurą
viršutinį rodom tik kai `has_findings`; švarioje dėžutėje lieka tik platus apatinis
(pilno pločio radaras, be tuščios kairės).
