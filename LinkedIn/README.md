# NBB LinkedIn-automatisering

Automatiserer LinkedIn-opslag for NBB (Nordic Big Bag). Finder relevante nyheder fra industrien, skriver et professionelt opslag med Claude AI, genererer et branded grafik og poster direkte til LinkedIn.

## Hvad det gør

1. Henter 5 aktuelle nyheder fra relevante RSS-feeds (eller modtager manuelt emne/URL)
2. Viser nyhederne til godkendelse i en browser-UI
3. Skriver et LinkedIn-opslag på valgt sprog (🇩🇰 🇬🇧 🇩🇪 🇸🇪)
4. Genererer et branded NBB-grafik
5. Viser opslaget til endelig godkendelse
6. Poster til LinkedIn

## Krav

- Python 3
- Anthropic API-nøgle
- LinkedIn adgangstoken

## Installation

Se `docs/INSTALL.md` for trin-for-trin guide.

## Filer

```
LinkedIn/
├── run.py                  # Start herfra
├── backend/
│   ├── orchestrator.py     # Hoved-logik
│   ├── approval_server.py  # Browser-UI (Flask)
│   ├── news_collector.py   # RSS + manuel input
│   ├── post_writer.py      # Claude AI opslag-skrivning
│   ├── image_generator.py  # Branded grafik
│   ├── linkedin_client.py  # LinkedIn API
│   └── config.py           # USPs og indstillinger
├── docs/
│   ├── INSTALL.md
│   └── VISION.md
└── NBB_LinkedIn_Demo.html  # Selvstændig demo-fil
```
