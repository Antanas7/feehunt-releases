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

### I. Masinio veiksmo mygtukas neatsistato po veiksmo — PATAISYTA 2026-05-31
🐞 — safe_bulk_action (app.py:3592) po sėkmingo veiksmo nustatydavo done_key=True ir
įstrigdavo „Atlikta" būsenoje (success+undo, return) → mygtukas negrįždavo,
reikėjo perkrauti puslapį, kad trintum kitą partiją. Antanas: „atrodo kaip
nebaigta funkcija, visi mygtukai po veiksmo turi grįžti į pradinę padėtį."
TAISYMAS: pašalinta sticky done-būsena; po veiksmo reset (confirm_key=False),
patvirtinimas confirm_success toast'u, ištrintiems — recent-trash „Gmail
šiukšlinėje" pranešimas. Mygtukas iškart vėl naudojamas. Vieno-laiško
show_safe_email_action paliktas (inline undo, C punktas; ne blokeris — laiškas
po trynimo dingsta). Pasiūlyta Antanui suvienodinti, jei norės.

### H. „Ar tai tikra?" skaičiaus nebuvo rezultatų santraukoje — PATAISYTA 2026-05-31
🧭 — Antanas: rezultatų santrauka rodė tik 3 metrikas (prenumeratos/rizikos,
reklaminiai, sutaupymas), be phishing/safety. Kai 29 laiškai nukrito į phishing,
santrauka rodė 0/0/$0 → painiava (laiškai pasislėpę kategorijoje, kuri neatsispindi
skaičiuose). TAISYMAS: dashboard rezultatų metrikos 3→4 stulpeliai, pridėta „Ar tai
tikra?" (safety_count = len phishing_risks) su help tekstu. dashboard.metric_safety
(+_help) EN+LT. app.py ~5528.
PATVIRTINTA realiu re-scan: prieš (18:17) reklaminiai 0 / phishing 29; po taisymų
(18:40) reklaminiai 37 / „Ar tai tikra?" 4. Marketingas grįžo į reklamas, phishing
liko tik tikri. G+H veikia.

### G. PHISHING false-positives ant marketingo (root cause!) — PATAISYTA 2026-05-31
🐞 svarbus — Žmonos dėžutės testas atskleidė: 8 nepageidaujami siuntėjai pateko į
skeną, BET phishing detektorius juos pažymėjo (29 phishing_risks, 0 promotional!),
todėl (1) nepateko į reklamas, (2) nepageidaujamų patikra praleidžiama (turbo
blokas reikalauja not phishing). Priežastis: `hidden_link` signalas (rodomas
domenas ≠ href domenas) ant marketingo klikų-sekimo (soundestlink, voyado,
agcocorp, mailmailmail, eclub...) — net bonprix vedė į PATĮ bonprix domeną.
TAISYMAS: (1) analyze_phishing(is_bulk) — masiniam paštui (List-Unsubscribe)
hidden_link signalas PRALEIDŽIAMAS (kiti signalai lieka — patikrinta, vardo/domeno
neatitikimas vis tiek pagaunamas); (2) +ESP domenai į baltą sąrašą; (3) main.py
sender_is_unwanted nugali phishing (vartotojo pasirinkimas → promotional, ne
phishing). Failai: phishing_detector.py, main.py. Laukia Antano re-scan patvirtinimo.

### E. Nepageidaujami siuntėjai (user-valdoma) — PADARYTA 2026-05-31
PADARYTA: vartotojo „Nepageidaujami siuntėjai" sąrašas (rules["unwanted_senders"]).
main.py load_unwanted_senders() skaito jį; skeneris ATPAŽĮSTA tų siuntėjų laiškus
kaip reklamą (sender_is_unwanted → is_promotional), NE blokuoja/NE trina (cleanup
blacklist lieka tuščias). UI: naujas laukas Cleanup Rules puslapyje (po whitelist),
naudoja esamus senders.blocked_* raktus. Perrašyti pasenę tekstai (page_lead,
protected_caption, blocked_caption) — iš „blokuoti/auto-trash" į „atpažinti kaip
šlamštas". config DEFAULT_RULES + unwanted_senders. Patikrinta: compile + match +
round-trip. Laukia Antano gyvo testo su žmonos dėžute (zoo.no, hjemsol, europris...).

### E0 (orig). Siuntėjų valdyme nebėra kur pridėti NEPAGEIDAUJAMŲ siuntėjų (svarbu)
🧭/💡 — Antanas: „valdymo centre nebeliko kur pridėti nepageidaujamų sąrašo, o tai
svarbi funkcija." Patvirtinta kode: `promo_senders` backend veikia
(email_matches_user_unwanted_rule, app.py:2666), naudojamas valyme, BET nebėra UI
lauko jį pildyti — Siuntėjų valdyme liko tik whitelist + advanced (kategorijos,
rezultatai). PLUS puslapio tekstas (senders.page_lead) pasenęs — žada „kuriuos
blokuoti, ir kas turi atsitikti su blokuojamais laiškais", bet blokavimo skyriaus
nėra. Tai = [[feehunt-teach-unwanted-loop]] iš kitos pusės.
ANTANO PATIKSLINIMAS (svarbu, mes buvom sumaišę): BLOKUOJAMI = blokuoti siuntėją
pašto dėžutėje (Gmail darbas, sąmoningai pašalinta). NEPAGEIDAUJAMI = siuntėjai,
kurių FeeHunt neaptinka; vartotojas įdeda, kad KITĄ SKENĄ būtų ATPAŽINTI kaip
reklamos/šlamštas (kategorizavimo pagalba) — vartotojas paskui valo įprastai.
Tai NE blokavimas ir NE prieštarauja [[feehunt-no-block-senders]].
ĮGYVENDINIMAS (A, teisingai): (1) UI laukas „Nepageidaujami siuntėjai" Siuntėjų
valdyme; (2) pajungti į SKENAVIMO atpažinimą (feehunt_analyzer/main.py), kad tų
siuntėjų laiškai patektų į Reklaminius — NE auto-trinti (dabartinis promo_senders
kelias TRINA → pajungti prie kategorizavimo / naujas raktas); (3) sutvarkyti
pasenusį senders.page_lead tekstą. Sprendimas: laukiama Antano „darom A".
REALUS PAVYZDYS (žmonos dėžutė, kpj.): užsilikęs šlamštas, kurio detekcija
nepagavo — norvegiškos parduotuvės ZOO.no, HJEMSOL, Sunkost, Europris,
Møbelringen, bonprix, Valtra (rabatt/-50%/tilbud), kai kurie kartojasi. Idealus
„nepageidaujami siuntėjai" use-case: raktažodžiais visų parduotuvių/kalbų
nepagausi, vartotojas pažįsta savo šlamštą.

### F. Detekcijos precizijos pavyzdžiai iš tos pačios kpj. (atskira nuo E)
🎯 — Tame pačiame žmonos inbox screenshot'e: (1) Emigrantas.tv „priminimas apie
netrukus nustosiantį galioti transliacijų paketą" → tikėtina PRENUMERATA (mokamas
TV paketas), ne tik šlamštas — FeeHunt turėtų matyti kaip prenumeratą.
(2) Ferratum Norge „betaling av fakturan din er fortsatt ikke mottatt" (sąskaita
neapmokėta) → MOKĖJIMŲ/finansų signalas, galbūt „Mokėjimų kontrolė". Kandidatai
detekcijos pagerinimui (LT/NO frazės).

### D. Du „Skenuoti dar kartą" mygtukai švarioje dėžutėje — PADARYTA
🐞 — Kai nėra radinių (švari dėžutė), rodėsi DU rescan mygtukai: siauras viršutinis
(stulpelis [3,2] → tuščia kairė + siauras radaras) IR platus apatinis. Antanas
nori plataus. Pataisyta: show_dashboard_hero_action_layer (app.py ~4830) — siaurą
viršutinį rodom tik kai `has_findings`; švarioje dėžutėje lieka tik platus apatinis
(pilno pločio radaras, be tuščios kairės).
