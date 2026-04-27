import sqlite3
import os
from datetime import datetime, date

DB_PATH = 'data/crm.db'


def get_db():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS kunder (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firmanavn TEXT NOT NULL,
            branche TEXT DEFAULT '',
            hjemmeside TEXT DEFAULT '',
            adresse TEXT DEFAULT '',
            noter TEXT DEFAULT '',
            konkurrent TEXT DEFAULT '',
            oprettet TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            opdateret TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS kontaktpersoner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kunde_id INTEGER NOT NULL REFERENCES kunder(id) ON DELETE CASCADE,
            navn TEXT NOT NULL,
            titel TEXT DEFAULT '',
            email TEXT DEFAULT '',
            telefon TEXT DEFAULT '',
            er_primaer INTEGER DEFAULT 0,
            noter TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS aktiviteter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kunde_id INTEGER NOT NULL REFERENCES kunder(id) ON DELETE CASCADE,
            type TEXT DEFAULT 'note',
            dato TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            beskrivelse TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS opkaldsliste (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kunde_id INTEGER NOT NULL REFERENCES kunder(id) ON DELETE CASCADE,
            planlagt_dato DATE DEFAULT (date('now')),
            prioritet INTEGER DEFAULT 2,
            note TEXT DEFAULT '',
            udfort INTEGER DEFAULT 0,
            oprettet TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS tilbud (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kunde_id INTEGER NOT NULL REFERENCES kunder(id) ON DELETE CASCADE,
            titel TEXT NOT NULL,
            belob TEXT DEFAULT '',
            status TEXT DEFAULT 'udsendt',
            dato_udsendt DATE DEFAULT (date('now')),
            opdateret TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            noter TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS kunde_produkter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kunde_id INTEGER NOT NULL REFERENCES kunder(id) ON DELETE CASCADE,
            saektype TEXT NOT NULL,
            specifikation TEXT DEFAULT '',
            sidst_pris TEXT DEFAULT '',
            noter TEXT DEFAULT ''
        );
    """)
    # Migration: tilføj konkurrent-felt til eksisterende databaser
    try:
        conn.execute("ALTER TABLE kunder ADD COLUMN konkurrent TEXT DEFAULT ''")
        conn.commit()
    except Exception:
        pass
    conn.commit()
    conn.close()


# ── Kunder ──────────────────────────────────────────────────────────

def hent_kunder(soeg='', sort='navn'):
    conn = get_db()
    extra = """
        (SELECT navn FROM kontaktpersoner WHERE kunde_id=k.id AND er_primaer=1 LIMIT 1) AS primaer_kontakt,
        (SELECT telefon FROM kontaktpersoner WHERE kunde_id=k.id AND er_primaer=1 LIMIT 1) AS primaer_telefon,
        (SELECT dato FROM aktiviteter WHERE kunde_id=k.id ORDER BY dato DESC LIMIT 1) AS sidst_aktivitet,
        (SELECT type FROM aktiviteter WHERE kunde_id=k.id ORDER BY dato DESC LIMIT 1) AS sidst_type,
        (SELECT COUNT(*) FROM opkaldsliste WHERE kunde_id=k.id AND udfort=0) AS ventende_opkald,
        (SELECT COUNT(*) FROM tilbud WHERE kunde_id=k.id AND status IN ('udsendt','forhandling')) AS aabne_tilbud,
        CAST(julianday('now') - julianday(
            (SELECT dato FROM aktiviteter WHERE kunde_id=k.id ORDER BY dato DESC LIMIT 1)
        ) AS INTEGER) AS dage_siden_kontakt
    """
    order = {
        'navn':   'k.firmanavn ASC',
        'sidst':  'dage_siden_kontakt DESC NULLS LAST',
        'branche':'k.branche ASC, k.firmanavn ASC',
    }.get(sort, 'k.firmanavn ASC')
    if soeg:
        rows = conn.execute(f"""
            SELECT k.*, {extra} FROM kunder k
            WHERE k.firmanavn LIKE ?
               OR EXISTS (SELECT 1 FROM kontaktpersoner WHERE kunde_id=k.id AND (navn LIKE ? OR email LIKE ?))
            ORDER BY {order}
        """, (f'%{soeg}%', f'%{soeg}%', f'%{soeg}%')).fetchall()
    else:
        rows = conn.execute(f"SELECT k.*, {extra} FROM kunder k ORDER BY {order}").fetchall()
    conn.close()
    return rows


def hent_kunde(id):
    conn = get_db()
    row = conn.execute("SELECT * FROM kunder WHERE id=?", (id,)).fetchone()
    conn.close()
    return row


def opret_kunde(data):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO kunder (firmanavn, branche, hjemmeside, adresse, noter, konkurrent) VALUES (?,?,?,?,?,?)",
        (data.get('firmanavn',''), data.get('branche',''), data.get('hjemmeside',''),
         data.get('adresse',''), data.get('noter',''), data.get('konkurrent',''))
    )
    id = cur.lastrowid
    conn.commit()
    conn.close()
    return id


def opdater_kunde(id, data):
    conn = get_db()
    conn.execute("""
        UPDATE kunder SET firmanavn=?, branche=?, hjemmeside=?, adresse=?, noter=?, konkurrent=?,
        opdateret=CURRENT_TIMESTAMP WHERE id=?
    """, (data.get('firmanavn',''), data.get('branche',''), data.get('hjemmeside',''),
          data.get('adresse',''), data.get('noter',''), data.get('konkurrent',''), id))
    conn.commit()
    conn.close()


def hent_dashboard_stats():
    conn = get_db()
    today = date.today().isoformat()
    pipeline_sum = conn.execute(
        "SELECT SUM(CAST(belob AS REAL)) FROM tilbud WHERE status IN ('udsendt','forhandling') AND belob != '' AND CAST(belob AS REAL) > 0"
    ).fetchone()[0] or 0
    stats = {
        'opkald_idag': conn.execute(
            "SELECT COUNT(*) FROM opkaldsliste WHERE planlagt_dato <= ? AND udfort=0", (today,)
        ).fetchone()[0],
        'aabne_tilbud': conn.execute(
            "SELECT COUNT(*) FROM tilbud WHERE status IN ('udsendt','forhandling')"
        ).fetchone()[0],
        'pipeline_sum': int(pipeline_sum),
        'vundet_maaned': conn.execute(
            "SELECT COUNT(*) FROM tilbud WHERE status='vundet' AND opdateret >= date('now','start of month')"
        ).fetchone()[0],
        'ikke_kontaktet': conn.execute("""
            SELECT COUNT(*) FROM kunder k WHERE
            CAST(julianday('now') - julianday(
                (SELECT dato FROM aktiviteter WHERE kunde_id=k.id ORDER BY dato DESC LIMIT 1)
            ) AS INTEGER) > 60
            OR NOT EXISTS (SELECT 1 FROM aktiviteter WHERE kunde_id=k.id)
        """).fetchone()[0],
        'kunder_total': conn.execute("SELECT COUNT(*) FROM kunder").fetchone()[0],
    }
    conn.close()
    return stats


def hent_ikke_kontaktet(dage=60):
    conn = get_db()
    rows = conn.execute(f"""
        SELECT k.id, k.firmanavn, k.branche,
            (SELECT navn FROM kontaktpersoner WHERE kunde_id=k.id AND er_primaer=1 LIMIT 1) AS primaer_kontakt,
            (SELECT telefon FROM kontaktpersoner WHERE kunde_id=k.id AND er_primaer=1 LIMIT 1) AS primaer_telefon,
            CAST(julianday('now') - julianday(
                (SELECT dato FROM aktiviteter WHERE kunde_id=k.id ORDER BY dato DESC LIMIT 1)
            ) AS INTEGER) AS dage_siden
        FROM kunder k
        WHERE dage_siden > {dage} OR dage_siden IS NULL
        ORDER BY dage_siden DESC
    """).fetchall()
    conn.close()
    return rows


def slet_kunde(id):
    conn = get_db()
    conn.execute("DELETE FROM kunder WHERE id=?", (id,))
    conn.commit()
    conn.close()


# ── Kontaktpersoner ─────────────────────────────────────────────────

def hent_kontakter(kunde_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM kontaktpersoner WHERE kunde_id=? ORDER BY er_primaer DESC, navn",
        (kunde_id,)
    ).fetchall()
    conn.close()
    return rows


def opret_kontakt(kunde_id, data):
    conn = get_db()
    er_primaer = 1 if data.get('er_primaer') else 0
    if er_primaer:
        conn.execute("UPDATE kontaktpersoner SET er_primaer=0 WHERE kunde_id=?", (kunde_id,))
    conn.execute(
        "INSERT INTO kontaktpersoner (kunde_id, navn, titel, email, telefon, er_primaer, noter) VALUES (?,?,?,?,?,?,?)",
        (kunde_id, data.get('navn',''), data.get('titel',''), data.get('email',''),
         data.get('telefon',''), er_primaer, data.get('noter',''))
    )
    conn.commit()
    conn.close()


def opdater_kontakt(id, data):
    conn = get_db()
    er_primaer = 1 if data.get('er_primaer') else 0
    if er_primaer:
        kunde_id = conn.execute("SELECT kunde_id FROM kontaktpersoner WHERE id=?", (id,)).fetchone()['kunde_id']
        conn.execute("UPDATE kontaktpersoner SET er_primaer=0 WHERE kunde_id=?", (kunde_id,))
    conn.execute("""
        UPDATE kontaktpersoner SET navn=?, titel=?, email=?, telefon=?, er_primaer=?, noter=? WHERE id=?
    """, (data.get('navn',''), data.get('titel',''), data.get('email',''),
          data.get('telefon',''), er_primaer, data.get('noter',''), id))
    conn.commit()
    conn.close()


def slet_kontakt(id):
    conn = get_db()
    conn.execute("DELETE FROM kontaktpersoner WHERE id=?", (id,))
    conn.commit()
    conn.close()


# ── Tilbud ──────────────────────────────────────────────────────────

def hent_tilbud_for_kunde(kunde_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM tilbud WHERE kunde_id=? ORDER BY dato_udsendt DESC", (kunde_id,)
    ).fetchall()
    conn.close()
    return rows


def hent_pipeline():
    conn = get_db()
    rows = conn.execute("""
        SELECT t.*, k.firmanavn,
            (SELECT navn FROM kontaktpersoner WHERE kunde_id=k.id AND er_primaer=1 LIMIT 1) AS kontakt_navn
        FROM tilbud t JOIN kunder k ON k.id=t.kunde_id
        ORDER BY t.dato_udsendt DESC
    """).fetchall()
    totaler = {}
    for s in ('udsendt','forhandling','vundet','tabt'):
        totaler[s] = conn.execute(
            "SELECT SUM(CAST(belob AS REAL)) FROM tilbud WHERE status=? AND belob != '' AND CAST(belob AS REAL) > 0", (s,)
        ).fetchone()[0] or 0
    conn.close()
    return rows, {k: int(v) for k, v in totaler.items()}


def opret_tilbud(kunde_id, data):
    conn = get_db()
    conn.execute(
        "INSERT INTO tilbud (kunde_id, titel, belob, status, dato_udsendt, noter) VALUES (?,?,?,?,?,?)",
        (kunde_id, data.get('titel',''), data.get('belob',''),
         data.get('status','udsendt'), data.get('dato_udsendt') or date.today().isoformat(),
         data.get('noter',''))
    )
    conn.commit()
    conn.close()


def opdater_tilbud_status(id, status):
    conn = get_db()
    conn.execute(
        "UPDATE tilbud SET status=?, opdateret=CURRENT_TIMESTAMP WHERE id=?", (status, id)
    )
    conn.commit()
    conn.close()


def opdater_tilbud(id, data):
    conn = get_db()
    kunde_id = conn.execute("SELECT kunde_id FROM tilbud WHERE id=?", (id,)).fetchone()['kunde_id']
    conn.execute("""
        UPDATE tilbud SET titel=?, belob=?, status=?, dato_udsendt=?, noter=?, opdateret=CURRENT_TIMESTAMP
        WHERE id=?
    """, (data.get('titel',''), data.get('belob',''), data.get('status','udsendt'),
          data.get('dato_udsendt') or date.today().isoformat(), data.get('noter',''), id))
    conn.commit()
    conn.close()
    return kunde_id


def slet_tilbud(id):
    conn = get_db()
    kunde_id = conn.execute("SELECT kunde_id FROM tilbud WHERE id=?", (id,)).fetchone()['kunde_id']
    conn.execute("DELETE FROM tilbud WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return kunde_id


# ── Produkthukommelse ────────────────────────────────────────────────

def hent_produkter(kunde_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM kunde_produkter WHERE kunde_id=? ORDER BY id", (kunde_id,)
    ).fetchall()
    conn.close()
    return rows


def opret_produkt(kunde_id, data):
    conn = get_db()
    conn.execute(
        "INSERT INTO kunde_produkter (kunde_id, saektype, specifikation, sidst_pris, noter) VALUES (?,?,?,?,?)",
        (kunde_id, data.get('saektype',''), data.get('specifikation',''),
         data.get('sidst_pris',''), data.get('noter',''))
    )
    conn.commit()
    conn.close()


def slet_produkt(id):
    conn = get_db()
    kunde_id = conn.execute("SELECT kunde_id FROM kunde_produkter WHERE id=?", (id,)).fetchone()['kunde_id']
    conn.execute("DELETE FROM kunde_produkter WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return kunde_id


# ── Aktiviteter ─────────────────────────────────────────────────────

def hent_aktiviteter(kunde_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM aktiviteter WHERE kunde_id=? ORDER BY dato DESC",
        (kunde_id,)
    ).fetchall()
    conn.close()
    return rows


def slet_aktivitet(id):
    conn = get_db()
    kunde_id = conn.execute("SELECT kunde_id FROM aktiviteter WHERE id=?", (id,)).fetchone()['kunde_id']
    conn.execute("DELETE FROM aktiviteter WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return kunde_id


def opret_aktivitet(kunde_id, data):
    conn = get_db()
    dato = data.get('dato') or datetime.now().strftime('%Y-%m-%dT%H:%M')
    conn.execute(
        "INSERT INTO aktiviteter (kunde_id, type, dato, beskrivelse) VALUES (?,?,?,?)",
        (kunde_id, data.get('type','note'), dato, data.get('beskrivelse',''))
    )
    conn.commit()
    conn.close()


# ── Opkaldsliste ────────────────────────────────────────────────────

def hent_opkaldsliste():
    conn = get_db()
    rows = conn.execute("""
        SELECT o.*, k.firmanavn,
            (SELECT navn FROM kontaktpersoner WHERE kunde_id=k.id AND er_primaer=1 LIMIT 1) AS kontakt_navn,
            (SELECT telefon FROM kontaktpersoner WHERE kunde_id=k.id AND er_primaer=1 LIMIT 1) AS kontakt_telefon,
            (SELECT email FROM kontaktpersoner WHERE kunde_id=k.id AND er_primaer=1 LIMIT 1) AS kontakt_email
        FROM opkaldsliste o JOIN kunder k ON k.id=o.kunde_id
        WHERE o.udfort=0 ORDER BY o.planlagt_dato ASC, o.prioritet ASC
    """).fetchall()
    conn.close()
    return rows


def hent_opkald_antal():
    conn = get_db()
    n = conn.execute("SELECT COUNT(*) FROM opkaldsliste WHERE udfort=0").fetchone()[0]
    conn.close()
    return n


def hent_opkald_for_kunde(kunde_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM opkaldsliste WHERE kunde_id=? AND udfort=0 ORDER BY planlagt_dato",
        (kunde_id,)
    ).fetchall()
    conn.close()
    return rows


def opret_opkald(kunde_id, data):
    conn = get_db()
    conn.execute(
        "INSERT INTO opkaldsliste (kunde_id, planlagt_dato, prioritet, note) VALUES (?,?,?,?)",
        (kunde_id, data.get('planlagt_dato') or date.today().isoformat(),
         int(data.get('prioritet', 2)), data.get('note',''))
    )
    conn.commit()
    conn.close()


def marker_opkald_udfort(id):
    conn = get_db()
    row = conn.execute("SELECT * FROM opkaldsliste WHERE id=?", (id,)).fetchone()
    if row:
        conn.execute("UPDATE opkaldsliste SET udfort=1 WHERE id=?", (id,))
        beskrivelse = "Opkald gennemført"
        if row['note']:
            beskrivelse += f" — {row['note']}"
        conn.execute(
            "INSERT INTO aktiviteter (kunde_id, type, dato, beskrivelse) VALUES (?, 'opkald', CURRENT_TIMESTAMP, ?)",
            (row['kunde_id'], beskrivelse)
        )
    conn.commit()
    conn.close()


# ── Demo-data ────────────────────────────────────────────────────────

def indlaes_demo_data():
    conn = get_db()
    if conn.execute("SELECT COUNT(*) FROM kunder").fetchone()[0] > 0:
        conn.close()
        return
    conn.close()

    demo = [
        ("Dansk Industri Holding A/S", "Industri & Produktion", "Industriparken 12, 2600 Glostrup",
         "Søren Madsen", "Indkøbschef", "sm@dih.dk", "+45 23 45 67 89",
         [("opkald","2026-04-20T10:30","Drøftede mulighed for ny ordre på 500 stk. Type A sække. Søren vender tilbage inden udgangen af april."),
          ("mail","2026-04-22T09:00","Sendte tilbud på 500 stk. Type A — afventer svar.")],
         ("2026-04-28", 1, "Følg op på tilbud sendt 22. april")),
        ("GreenPack Solutions ApS", "Emballage & Logistik", "Havnegade 4, 8000 Aarhus C",
         "Mette Christensen", "Sustainability Manager", "mc@greenpack.dk", "+45 31 22 44 55",
         [("møde","2026-04-15T14:00","Teams-møde om genanvendelige bigbags. Meget interesseret i cirkulær løsning. Sender specifikation.")],
         ("2026-04-30", 2, "Præsenter specifikation på cirkulær model")),
        ("Nordic Bulk Transport A/S", "Transport & Logistik", "Fredhøjvej 22, 7400 Herning",
         "Lars Eriksen", "Driftsleder", "le@nordicbulk.dk", "+45 40 33 22 11",
         [("note","2026-04-10T08:00","Ny potentiel kunde — fundet via netværk. Bruger i dag konkurrent. Første opkald endnu ikke foretaget.")],
         ("2026-05-05", 3, "Første opkald — introducer NBB og book møde")),
    ]

    for firma, branche, adresse, knavn, ktitel, kemail, ktlf, aktivs, opkald in demo:
        id = opret_kunde({'firmanavn': firma, 'branche': branche, 'adresse': adresse, 'hjemmeside': '', 'noter': ''})
        opret_kontakt(id, {'navn': knavn, 'titel': ktitel, 'email': kemail, 'telefon': ktlf, 'er_primaer': '1'})
        for type_, dato, besk in aktivs:
            opret_aktivitet(id, {'type': type_, 'dato': dato, 'beskrivelse': besk})
        dato, prio, note = opkald
        opret_opkald(id, {'planlagt_dato': dato, 'prioritet': str(prio), 'note': note})
