# NBB — Automatisk LinkedIn-tilstedeværelse med AI

## Hvad er dette?

Dette er et færdigbygget system der holder NBB synlig på LinkedIn — uden at du bruger tid på det.

Systemet finder selv relevante nyheder om emballage, bigbags og cirkulær økonomi. Det bruger dem som afsæt til at skrive et professionelt LinkedIn-opslag, der løfter NBB som aktør inden for grøn omstilling. Du modtager udkastet, godkender det med ét klik — og systemet poster det selv.

**Resultat:** Ét ugentligt LinkedIn-opslag, konsekvent, troværdigt og branchen, uden at det koster dig tid.

---

## Sådan virker det i praksis

```
Mandag aften (automatisk):
  → Systemet scanner nyhedskilder
  → Finder den mest relevante nyhed om bigbags / cirkulær økonomi
  → Claude AI skriver et LinkedIn-opslag med nyheden som krog og NBB som aktøren

Tirsdag morgen (du modtager en mail):
  → Du åbner mailen
  → Ser udkastet — formateret som det vil se ud på LinkedIn
  → Klikker: "Godkend og post" eller "Afvis"
  → Intet mere

Tirsdag formiddag (automatisk):
  → Opslaget publiceres til NBBs LinkedIn-virksomhedsside
```

Ingen login. Ingen apps. Ét klik.

---

## Hvad indholdet handler om

Systemet varierer indholdet fra uge til uge, så det aldrig gentager sig selv. Det roterer mellem syv vinkler på NBBs styrker:

1. Kvalitet og holdbarhed i industrielle miljøer
2. Produktion med genanvendte råmaterialer
3. Den cirkulære model — indsaml, genanvend, genbrugeri produktion
4. Specialtilpasning til kundens specifikke krav
5. NBB som dansk, lokal samarbejdspartner
6. Grøn emballage til konkurrencedygtig pris
7. Ekspertrådgivning om den rette løsning

Opslaget skrives skiftevis på dansk og engelsk for at nå en bredere målgruppe.

Tonen er altid professionel og sober. Systemet provokerer aldrig, nævner ikke konkurrenter og holder sig til det faglige.

---

## Hvad forventes af dig

**Nu — inden systemet kører fuldt ud:**

- [ ] Oprette en gratis API-konto hos Anthropic (det firma bag Claude AI) og tilføje et engangsindskud på ca. 35 kr.
- [ ] Oprette en LinkedIn Developer App (gratis) — tager ca. 10 minutter med vejledning
- [ ] Godkende at systemet må poste på vegne af NBBs LinkedIn-virksomhedsside

**Løbende — når det kører:**

- Åbne én mail om ugen (tirsdag morgen)
- Klikke godkend eller afvis
- Det er alt

---

## Hvad koster det

| Post | Engangsudgift | Månedlig udgift |
|---|---|---|
| API-kredit til Claude AI (AI-skrivning) | ~35 kr. | ~0,20 kr. |
| LinkedIn Developer App | 0 kr. | 0 kr. |
| Nyhedsindsamling | 0 kr. | 0 kr. |
| Hosting (eksisterende server) | 0 kr. | 0 kr. |
| **I alt** | **~35 kr.** | **~0,20 kr.** |

Engangsindskuddet på 35 kr. rækker til ca. 14 år ved dette forbrug.

**Den reelle månedlige driftsudgift er under 25 øre.**

Til sammenligning koster en ekstern social media manager typisk 5.000–15.000 kr. om måneden for samme type indhold.

---

## Næste skridt for at køre systemet fuldt ud

Systemet er bygget og testet. Det mangler kun tre korte opsætninger:

**Trin 1 — Giv AI'en adgang (30 minutter)**
Opret en konto på platform.anthropic.com, tilføj 35 kr. i kredit og indsæt nøglen i systemets konfigurationsfil. Her guides du igennem det.

**Trin 2 — Giv systemet adgang til LinkedIn (30 minutter)**
Opret en gratis LinkedIn Developer App på linkedin.com/developers. Kopiér to koder (Access Token og Company ID) ind i konfigurationsfilen. Her guides du igennem det.

**Trin 3 — Sæt det på autopilot (5 minutter)**
En enkelt kommando på jeres server sørger for at systemet kører automatisk hver tirsdag. Herefter kræver det ingen opmærksomhed.

**Total opsætningstid: ca. 1–1,5 time med vejledning.**

---

## Hvad er det naturlige næste skridt for produktet?

Systemet er bygget så det nemt kan udvides. Her er de oplagte trin efter LinkedIn kører:

### Fase 2 — Automatisk web-indhold
Det samme opslag der publiceres på LinkedIn kan automatisk tilføjes som en nyhed eller blogpost på NBBs hjemmeside. Ingen ekstra arbejde — samme indhold, endnu en kanal.

*Kræver: adgang til hjemmesidens CMS eller hosting. Teknisk arbejde: 3–5 timer.*

### Fase 3 — Daglig nyhedsovervågning
I stedet for ét ugentligt opslag kan systemet overvåge nyheder dagligt og kun sende udkast videre, når der er en nyhed der er ekstraordinært relevant. Fuld kontrol, men uden faste intervaller.

*Kræver: ingen ny infrastruktur. Teknisk arbejde: 1–2 timer.*

### Fase 4 — Automatisk kundebrev / nyhedsbrev
Den nyhed og det opslag systemet producerer kan pakkes ind i et simpelt nyhedsbrev, der automatisk sendes til NBBs eksisterende kunder eller emner. LinkedIn bygger synlighed udadtil — nyhedsbrevet fastholder relationer indadtil.

*Kræver: liste over modtagere og en gratis e-mailplatform (fx Mailchimp). Teknisk arbejde: 2–3 timer.*

---

## Hvad er bygget

```
NBB/
  run.py                    → Start systemet med én kommando
  backend/
    news_collector.py       → Indsamler og scorer nyheder fra 9 kilder
    post_writer.py          → Claude AI skriver opslaget
    approval_server.py      → Godkendelsessiden du ser i browseren/mailen
    linkedin_client.py      → Publicerer til LinkedIn
    state_manager.py        → Husker hvilken vinkel og sprog der er brugt
    config.py               → Alle indstillinger samlet ét sted
  docs/
    VISION.md               → Projektets formål og principper
    OMKOSTNINGER.md         → Detaljeret omkostningsoversigt
    INSTALL.md              → Teknisk installationsvejledning
```

---

*Systemet er bygget i april 2026. Spørgsmål: tony.andersen@zentura.dk*
