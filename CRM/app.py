import os
import sys
import threading
import webbrowser
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file
import database

if getattr(sys, 'frozen', False):
    _templates = os.path.join(sys._MEIPASS, 'templates')
else:
    _templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=_templates)
app.secret_key = 'nbb-crm-2026'

MAANEDER = ['jan','feb','mar','apr','maj','jun','jul','aug','sep','okt','nov','dec']

AKTIVITET_INFO = {
    'opkald': ('📞', 'Opkald',  'badge-blue'),
    'mail':   ('📧', 'Mail',    'badge-lilla'),
    'møde':   ('🤝', 'Møde',   'badge-groen'),
    'tilbud': ('📋', 'Tilbud',  'badge-orange'),
    'ordre':  ('📦', 'Ordre',   'badge-blaa'),
    'note':   ('📝', 'Note',    'badge-graa'),
}

PRIORITET_INFO = {
    1: ('Høj',   'badge-roed'),
    2: ('Normal','badge-graa'),
    3: ('Lav',   'badge-groen'),
}

TILBUD_STATUS = {
    'udsendt':    ('Udsendt',    'badge-orange'),
    'forhandling':('Forhandling','badge-lilla'),
    'vundet':     ('Vundet',     'badge-groen'),
    'tabt':       ('Tabt',       'badge-roed'),
}


@app.template_filter('kr')
def format_kr(value):
    try:
        n = int(float(str(value)))
        return f"{n:,.0f} kr.".replace(',', '.')
    except Exception:
        return str(value) if value else ''


@app.template_filter('dato')
def format_dato(value):
    if not value:
        return ''
    try:
        dt = datetime.fromisoformat(str(value)[:16])
        return f"{dt.day}. {MAANEDER[dt.month-1]} {dt.year}"
    except Exception:
        return str(value)[:10]


@app.template_filter('dato_kort')
def format_dato_kort(value):
    if not value:
        return ''
    try:
        dt = datetime.fromisoformat(str(value)[:10])
        return f"{dt.day}. {MAANEDER[dt.month-1]}"
    except Exception:
        return str(value)[:10]


@app.context_processor
def global_context():
    return {
        'opkald_antal': database.hent_opkald_antal(),
        'aktivitet_info': AKTIVITET_INFO,
        'prioritet_info': PRIORITET_INFO,
        'tilbud_status': TILBUD_STATUS,
    }


# ── Dashboard ────────────────────────────────────────────────────────

@app.route('/')
def dashboard():
    stats = database.hent_dashboard_stats()
    ikke_kontaktet = database.hent_ikke_kontaktet(60)
    return render_template('dashboard.html', stats=stats, ikke_kontaktet=ikke_kontaktet)


# ── Kunder ──────────────────────────────────────────────────────────

@app.route('/kunder')
def kunder():
    soeg = request.args.get('q', '')
    sort = request.args.get('sort', 'navn')
    alle = database.hent_kunder(soeg, sort)
    return render_template('kunder.html', kunder=alle, soeg=soeg, sort=sort)


@app.route('/kunde/ny', methods=['GET', 'POST'])
def ny_kunde():
    if request.method == 'POST':
        id = database.opret_kunde(request.form)
        return redirect(url_for('kunde', id=id))
    return render_template('ny_kunde.html')


@app.route('/kunde/<int:id>')
def kunde(id):
    k = database.hent_kunde(id)
    if not k:
        return redirect(url_for('kunder'))
    return render_template('kunde.html',
        kunde=k,
        kontakter=database.hent_kontakter(id),
        aktiviteter=database.hent_aktiviteter(id),
        opkald=database.hent_opkald_for_kunde(id),
        tilbud=database.hent_tilbud_for_kunde(id),
        produkter=database.hent_produkter(id),
        today=datetime.now().strftime('%Y-%m-%dT%H:%M'),
    )


@app.route('/kunde/<int:id>/rediger', methods=['POST'])
def rediger_kunde(id):
    database.opdater_kunde(id, request.form)
    return redirect(url_for('kunde', id=id))


@app.route('/kunde/<int:id>/slet', methods=['POST'])
def slet_kunde(id):
    database.slet_kunde(id)
    return redirect(url_for('kunder'))


# ── Kontakter ───────────────────────────────────────────────────────

@app.route('/kunde/<int:id>/kontakt', methods=['POST'])
def tilfoej_kontakt(id):
    database.opret_kontakt(id, request.form)
    return redirect(url_for('kunde', id=id) + '#kontakter')


@app.route('/kontakt/<int:id>/rediger', methods=['POST'])
def rediger_kontakt(id):
    from database import get_db
    conn = get_db()
    kunde_id = conn.execute("SELECT kunde_id FROM kontaktpersoner WHERE id=?", (id,)).fetchone()['kunde_id']
    conn.close()
    database.opdater_kontakt(id, request.form)
    return redirect(url_for('kunde', id=kunde_id) + '#kontakter')


@app.route('/kontakt/<int:id>/slet', methods=['POST'])
def slet_kontakt(id):
    from database import get_db
    conn = get_db()
    kunde_id = conn.execute("SELECT kunde_id FROM kontaktpersoner WHERE id=?", (id,)).fetchone()
    conn.close()
    database.slet_kontakt(id)
    return redirect(url_for('kunde', id=kunde_id['kunde_id']) + '#kontakter')


# ── Aktiviteter ─────────────────────────────────────────────────────

@app.route('/kunde/<int:id>/aktivitet', methods=['POST'])
def tilfoej_aktivitet(id):
    database.opret_aktivitet(id, request.form)
    return redirect(url_for('kunde', id=id) + '#aktiviteter')


@app.route('/aktivitet/<int:id>/slet', methods=['POST'])
def slet_aktivitet(id):
    kunde_id = database.slet_aktivitet(id)
    return redirect(url_for('kunde', id=kunde_id) + '#aktiviteter')


# ── Opkaldsliste ────────────────────────────────────────────────────

@app.route('/kunde/<int:id>/opkald', methods=['POST'])
def tilfoej_opkald(id):
    database.opret_opkald(id, request.form)
    return redirect(url_for('opkaldsliste'))


@app.route('/opkaldsliste')
def opkaldsliste():
    opkald = database.hent_opkaldsliste()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('opkaldsliste.html', opkald=opkald, today=today)


@app.route('/opkaldsliste/<int:id>/udfort', methods=['POST'])
def marker_udfort(id):
    database.marker_opkald_udfort(id)
    tilbage = request.form.get('tilbage')
    if tilbage:
        return redirect(tilbage + '#aktiviteter')
    return redirect(url_for('opkaldsliste'))


# ── Tilbud / Pipeline ────────────────────────────────────────────────

@app.route('/pipeline')
def pipeline():
    alle, totaler = database.hent_pipeline()
    kolonner = ['udsendt', 'forhandling', 'vundet', 'tabt']
    grupper = {s: [] for s in kolonner}
    for t in alle:
        grupper.setdefault(t['status'], []).append(t)
    return render_template('pipeline.html', grupper=grupper, tilbud_status=TILBUD_STATUS, totaler=totaler)


@app.route('/kunde/<int:id>/tilbud', methods=['POST'])
def tilfoej_tilbud(id):
    database.opret_tilbud(id, request.form)
    return redirect(url_for('kunde', id=id) + '#tilbud')


@app.route('/tilbud/<int:id>/status', methods=['POST'])
def opdater_tilbud_status(id):
    ny_status = request.form.get('status')
    kunde_id = request.form.get('kunde_id')
    database.opdater_tilbud_status(id, ny_status)
    if kunde_id:
        return redirect(url_for('kunde', id=int(kunde_id)) + '#tilbud')
    return redirect(url_for('pipeline'))


@app.route('/tilbud/<int:id>/rediger', methods=['POST'])
def rediger_tilbud(id):
    kunde_id = database.opdater_tilbud(id, request.form)
    return redirect(url_for('kunde', id=kunde_id) + '#tilbud')


@app.route('/tilbud/<int:id>/slet', methods=['POST'])
def slet_tilbud(id):
    kunde_id = database.slet_tilbud(id)
    return redirect(url_for('kunde', id=kunde_id) + '#tilbud')


# ── Produkthukommelse ────────────────────────────────────────────────

@app.route('/kunde/<int:id>/produkt', methods=['POST'])
def tilfoej_produkt(id):
    database.opret_produkt(id, request.form)
    return redirect(url_for('kunde', id=id) + '#produkter')


@app.route('/produkt/<int:id>/slet', methods=['POST'])
def slet_produkt(id):
    kunde_id = database.slet_produkt(id)
    return redirect(url_for('kunde', id=kunde_id) + '#produkter')


# ── Backup ──────────────────────────────────────────────────────────

@app.route('/backup')
def backup():
    import shutil
    ts = datetime.now().strftime('%Y-%m-%d')
    dest = os.path.expanduser(f'~/Downloads/NBB-CRM-backup-{ts}.db')
    shutil.copy2(database.DB_PATH, dest)
    return redirect(request.referrer or url_for('dashboard'))


# ── Start ────────────────────────────────────────────────────────────

def aaben_browser():
    import time
    time.sleep(1.2)
    webbrowser.open('http://localhost:5002')


if __name__ == '__main__':
    database.init_db()
    if os.environ.get('DEMO', 'true').lower() == 'true':
        database.indlaes_demo_data()
    threading.Thread(target=aaben_browser, daemon=True).start()
    print("\n── NBB CRM ──────────────────────────────────────")
    print("  Åbner i browseren på http://localhost:5002")
    print("  Stop: tryk Ctrl+C i dette vindue")
    print("─────────────────────────────────────────────────\n")
    app.run(port=5002, debug=False)
