# NBB CRM — Projekthukommelse

## Om virksomheden
NBB (Nordic Big Bag) — dansk virksomhed der sælger bigbags (FIBCs) til industrien med fokus på cirkulær økonomi og grøn omstilling. Ene-ejer og eneste ressource: én person driver det hele.

## Om brugeren
- Ikke-udvikler. Forklar altid i klart sprog uden teknisk jargon.
- Har tidligere arbejdet med SuperOffice (salgs-CRM) og kender værdien af et godt kundeoverblik.
- Arbejder i dag primært i Word og Excel — ingen struktureret kundedatabase endnu.
- Bruger Rackbeat til lagerstyring/administration, integreret med e-conomic (købsordrer, ordrebekræftelser, fakturaer).

## Problemet systemet skal løse
Ingen struktureret oversigt over kunder, kontaktpersoner, ordrehistorik og opfølgninger. Alt lever i Word, Excel og hovedet på ejeren. Det koster salg og relationer — specielt fordi den rigtige kontaktperson skal rammes på det rigtige tidspunkt.

## Hvad systemet skal kunne — prioriteret

### Kernefunktioner (fase 1)
- **Kundeoverblik** — ét skærmbillede med: kontaktperson, virksomhed, seneste ordre, igangværende ordre, noter fra telefonsnak og møder
- **Kontaktpersoner** — ikke bare info@virksomhed.dk, men den rigtige person med titel og direkte kontakt
- **Opkaldsliste** — hvilke kunder skal ringes til denne uge/dag
- **Historik** — log af telefonsamtaler, aftaler og tilbud per kunde

### Automatisering (fase 2)
- **Automail før opkald** — en kort, personlig mail der går ud inden telefonen ringer
- **Opfølgningsmail** — automatisk rykker når kunde ikke har svaret på tilbud inden X dage
- **Microsoft Kalender-integration** — aftalerne i CRM synkroniseres med Outlook-kalenderen

### Data og indsigt (fase 3)
- **Rackbeat-integration** — hent ordredata og analyser: hvilke kunder er mest profitable, hvilke sækketyper har størst omsætning, hvilke leverandører giver bedste priser
- **Branche-indsigt** — hvilke brancher fungerer bedst for NBB

## Vigtige principper
- **Enkelthed frem for features** — én person bruger systemet, det skal ikke kræve oplæring
- **Relationer er alt** — kunder køber tryghed hvis der er en relation, pris hvis ikke. Systemet skal understøtte relationsopbygning
- **Ingen spildt kontakt** — forkert person + forkert tidspunkt = spildt arbejde. Systemet skal hjælpe med at ramme rigtigt
- **Mobilvenligt** — ejeren er ikke altid ved en computer

## Teknisk kontekst
- Eksisterende systemer: Rackbeat + e-conomic (via integration)
- Mail: sandsynligvis Microsoft 365 / Outlook
- Kalender: Microsoft Kalender
- Platform: macOS

## Hvad der ikke er afklaret endnu
- Skal det være en webapplikation eller desktopapp?
- Skal det integrere direkte med Rackbeat API eller bare importere data?
- Hvad er den foretrukne mail-afsendelsesmetode (Outlook, SMTP, andet)?
- Budget/omkostninger for tredjeparts API'er

## Læs dette ved session-start
Stil brugeren spørgsmål om ovenstående uafklarede punkter inden der kodes noget. Start med at kortlægge hvilken fase der skal bygges først og hvilken teknisk løsning der passer til brugeren.
