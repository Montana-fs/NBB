# Hvad koster det at have systemet kørende?

## Oversigt

| Komponent | Hvad | Pris/måned |
|---|---|---|
| **Claude API** | AI skriver opslaget (ca. 1.000 tokens/opslag) | ~**2–5 kr.** |
| **Nyhedsindsamling** | RSS-feeds (gratis, ingen API nøgle) | **0 kr.** |
| **LinkedIn API** | Officiel post-adgang via LinkedIn Developer | **0 kr.** |
| **Hosting** | Virksomheden har allerede server (C) | **0 kr. ekstra** |
| **Email godkendelse** | Via eksisterende email-konto (SMTP) | **0 kr.** |
| **I alt** | | **~2–5 kr./måned** |

---

## Detaljeret breakdown

### Claude API (Anthropic)
Systemet kalder Claude én gang per uge for at skrive opslaget.

- Model: Claude Sonnet 4.6
- Input: ~800 tokens (nyhed + instruktioner)
- Output: ~300 tokens (LinkedIn-opslaget)
- Pris per kald: ~$0,003 USD ≈ **0,02 kr.**
- Per måned (4 opslag): **< 0,10 kr.**

Med prompt caching (allerede implementeret) genbruges systeminstruktionerne,
hvilket reducerer token-forbrug med op til 90% på gentagende kald.

**Realistisk månedspris inkl. test og fejlsøgning: 2–5 kr.**

### Nyhedsindsamling
RSS-feeds fra Altinget, Packaging News, Circular Online m.fl. er gratis og kræver
ingen API-nøgle. Systemet henter dem direkte.

Alternativt kan NewsAPI.org bruges (gratis op til 100 kald/dag på dev-plan).

### LinkedIn API
LinkedIns officielle API til virksomhedssider er gratis for grundlæggende publicering.
Kræver en LinkedIn Developer App (gratis at oprette) og én-gangs-godkendelse.

### Hosting
Da virksomheden allerede har server (option C fra opstartsmødet), er der ingen
ekstra hosting-udgift. Systemet kører som en planlagt opgave (cron job) på serveren.

---

## Sammenligning

| Alternativ | Pris/måned | Hvad du får |
|---|---|---|
| Social media manager (ekstern) | 5.000–15.000 kr. | Manuelt arbejde, møder, brief |
| SaaS automatisering (Buffer, Hootsuite AI) | 300–800 kr. | Generisk indhold, ingen branchen |
| **Dette system** | **2–5 kr.** | Branchen, dit produkt, din stemme |

---

## Opskalering

Systemet er bygget til at skalere uden ekstra omkostninger:

- **Flere opslag per uge:** dobler ikke prisen — kun API-kald stiger minimalt
- **Web-publicering (fase 2):** ingen ekstra infrastruktur nødvendig
- **Flere platforme (Twitter/X, Facebook):** tilføjes med få timers arbejde
- **Daglig nyhedsovervågning:** stadig under 10 kr./måned i API-kald

---

*Alle priser er vejledende og baseret på april 2026-prislister.
Anthropic-priser opdateres løbende — se platform.anthropic.com for aktuelle satser.*
