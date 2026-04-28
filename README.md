# NBB — Nordic Big Bag

Privat repo med automatiserings- og CRM-værktøjer til NBB.

## Indhold

### CRM/
Lokalt CRM-system bygget i Flask + SQLite. Kører i browseren på din Mac, ingen internet nødvendigt.

**Funktioner:**
- Dashboard med nøgletal (opkald, åbne tilbud, pipeline-værdi, churn-advarsel)
- Kundeoversigt med søgning og sortering
- Kundekort med kontakter, aktivitetslog og noter
- Tilbuds-pipeline (Udsendt → Forhandling → Vundet → Tabt)
- Opkaldsliste med prioritet og automatisk aktivitetslog
- Produkthukommelse per kunde (sækketype, spec, sidst pris)
- Konkurrent-felt per kunde
- Backup-knap (kopierer database til Downloads)

**Start:** Dobbeltklik på `CRM/start.command`

### LinkedIn/
Automatisering af LinkedIn-opslag for NBB. Finder relevante nyheder, skriver opslag med Claude AI, genererer brandede grafik og poster til LinkedIn.

**Sprog:** Dansk

**Start:** Se `LinkedIn/docs/INSTALL.md`

## Krav

- macOS
- Python 3 ([python.org](https://www.python.org) hvis ikke installeret)
- Anthropic API-nøgle (kun LinkedIn-modulet)
