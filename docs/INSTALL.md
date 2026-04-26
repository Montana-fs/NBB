# Installation

## Krav
- Python 3.9 eller nyere
- Internetforbindelse (til nyhedsindsamling og Claude API)

## Trin-for-trin

### 1. Installer afhængigheder
```bash
pip3 install -r requirements.txt
```

### 2. Opret miljø-fil
```bash
cp .env.example .env
```
Åbn `.env` og udfyld din `ANTHROPIC_API_KEY`.
(Resten udfyldes når rigtige integrationer aktiveres.)

### 3. Test kørslen
```bash
python run.py
```

Systemet vil:
1. Søge efter relevante nyheder
2. Skrive et LinkedIn-opslag med Claude
3. Åbne en godkendelsesside i din browser
4. Gemme det godkendte opslag i `output/`

---

## Automatisk ugentlig kørsel (cron — Linux/macOS)

For at systemet kører automatisk hver tirsdag kl. 08:00:

```bash
crontab -e
```

Tilføj linjen:
```
0 8 * * 2 cd /sti/til/NBB && python3 run.py >> logs/nbb.log 2>&1
```

Opret log-mappe:
```bash
mkdir -p logs
```

---

## Aktivering af rigtige integrationer

### LinkedIn API
1. Gå til linkedin.com/developers og opret en app
2. Bed om `w_member_social` og `w_organization_social` adgang
3. Kopiér Access Token og Company ID til `.env`
4. Sæt `DUMMY_MODE=false` i `.env`

### Email godkendelse (i stedet for browser)
Udfyld SMTP-felterne i `.env` med dit eksisterende mail-setup.
Systemet sender da en mail med godkend/afvis-link i stedet for at åbne browser.
