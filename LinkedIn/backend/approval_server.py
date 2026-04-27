import os
import queue
import threading
import webbrowser
from flask import Flask, request, redirect, jsonify, send_file

app = Flask(__name__)

_q = queue.Queue()
_state = {
    "candidates": [],
    "usp": {},
    "usp_index": 0,
    "language": "da",
    "pending_data": None,
    "post_ready": False,
}
_server_started = False
_port = 5001


def setup(candidates, usp, language, usp_index):
    while not _q.empty():
        try:
            _q.get_nowait()
        except queue.Empty:
            break
    _state["candidates"] = candidates
    _state["usp"] = usp
    _state["usp_index"] = usp_index
    _state["language"] = language
    _state["pending_data"] = None
    _state["post_ready"] = False


def set_pending(pending_data):
    _state["pending_data"] = pending_data
    _state["post_ready"] = True


def clear_pending():
    _state["pending_data"] = None
    _state["post_ready"] = False


def get_pending():
    return _state["pending_data"]


def next_action():
    return _q.get()


def start(port=5001):
    global _server_started, _port
    _port = port
    if not _server_started:
        t = threading.Thread(
            target=lambda: app.run(port=port, debug=False, use_reloader=False),
            daemon=True,
        )
        t.start()
        _server_started = True
    webbrowser.open(f"http://localhost:{port}")


def _fmt_date(published):
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(published)
        months = ["jan","feb","mar","apr","maj","jun","jul","aug","sep","okt","nov","dec"]
        return f"{dt.day}. {months[dt.month - 1]} {dt.year}"
    except Exception:
        return (published or "")[:10]


@app.route("/")
def selection_page():
    language = _state["language"]
    lang_flag = "🇩🇰" if language == "da" else "🇬🇧"
    lang_label = "Dansk" if language == "da" else "English"
    usp_text = _state["usp"].get(language, "")
    candidates = _state["candidates"]

    cards = ""
    for i, a in enumerate(candidates):
        pub = _fmt_date(a.get("published", ""))
        score = min(a.get("score", 0), 5)
        stars = "★" * score + "☆" * (5 - score)
        title = a["title"][:140]
        cards += f"""
        <div class="news-card">
          <div class="news-card-top">
            <span class="news-source">{a['source']}</span>
            <span class="news-date">{pub}</span>
          </div>
          <div class="news-title">{title}</div>
          <div class="news-card-bottom">
            <span class="news-score">{stars}</span>
            <a href="/select/article/{i}" class="btn-news">Brug denne →</a>
          </div>
        </div>"""

    no_news = "" if candidates else '<p class="no-news">Ingen nyheder fundet i dag — brug eget emne ovenfor.</p>'

    return f"""<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NBB — Vælg nyhed til ugens opslag</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f3f2ef; min-height: 100vh; padding: 32px 16px; }}
  .container {{ max-width: 680px; margin: 0 auto; }}
  .header {{ text-align: center; margin-bottom: 32px; }}
  .header h1 {{ font-size: 22px; color: #1a1a1a; font-weight: 700; }}
  .header p {{ color: #666; margin-top: 6px; font-size: 14px; }}
  .badge {{ display: inline-flex; align-items: center; gap: 6px; background: #e8f0fe; color: #1a56db; border-radius: 20px; padding: 4px 12px; font-size: 13px; font-weight: 500; margin-top: 10px; }}
  .card {{ background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; margin-bottom: 20px; }}
  .card-header {{ padding: 16px 20px; border-bottom: 1px solid #f0f0f0; font-weight: 600; color: #1a1a1a; font-size: 15px; }}
  .card-body {{ padding: 20px; }}
  .manual-input {{ width: 100%; padding: 12px 16px; border: 1.5px solid #d0d0d0; border-radius: 8px; font-size: 15px; font-family: inherit; resize: vertical; min-height: 64px; transition: border-color 0.15s; }}
  .manual-input:focus {{ outline: none; border-color: #0a66c2; }}
  .manual-hint {{ font-size: 13px; color: #888; margin-top: 8px; line-height: 1.5; }}
  .btn-manual {{ margin-top: 14px; width: 100%; padding: 13px; background: #0a66c2; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; transition: background 0.15s; }}
  .btn-manual:hover {{ background: #004182; }}
  .divider {{ text-align: center; color: #aaa; font-size: 13px; margin: 8px 0 20px; position: relative; }}
  .divider::before, .divider::after {{ content: ''; position: absolute; top: 50%; width: 44%; height: 1px; background: #e0e0e0; }}
  .divider::before {{ left: 0; }}
  .divider::after {{ right: 0; }}
  .section-label {{ font-size: 12px; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }}
  .news-card {{ background: white; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.07); padding: 16px 20px; margin-bottom: 12px; }}
  .news-card-top {{ display: flex; justify-content: space-between; margin-bottom: 8px; }}
  .news-source {{ font-size: 12px; font-weight: 600; color: #0a66c2; text-transform: uppercase; letter-spacing: 0.4px; }}
  .news-date {{ font-size: 12px; color: #aaa; }}
  .news-title {{ font-size: 15px; font-weight: 500; color: #1a1a1a; line-height: 1.45; margin-bottom: 12px; }}
  .news-card-bottom {{ display: flex; justify-content: space-between; align-items: center; }}
  .news-score {{ font-size: 13px; color: #f59e0b; letter-spacing: 1px; }}
  .btn-news {{ padding: 8px 16px; background: #f3f2ef; color: #1a1a1a; border-radius: 6px; font-size: 13px; font-weight: 600; text-decoration: none; transition: all 0.15s; border: 1px solid #e0e0e0; white-space: nowrap; }}
  .btn-news:hover {{ background: #0a66c2; color: white; border-color: #0a66c2; }}
  .usp-note {{ padding: 12px 16px; background: #f0fdf4; border-radius: 8px; border-left: 3px solid #16a34a; font-size: 13px; color: #166534; margin-top: 8px; }}
  .usp-note .label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #888; margin-bottom: 4px; }}
  .no-news {{ color: #999; font-size: 14px; text-align: center; padding: 24px 0; }}
  .lang-toggle {{ display: flex; gap: 8px; justify-content: center; margin-top: 14px; }}
  .lang-btn {{ padding: 8px 20px; border-radius: 20px; font-size: 14px; font-weight: 600; cursor: pointer; border: 2px solid #d0d0d0; background: white; color: #666; transition: all 0.15s; }}
  .lang-btn.active {{ background: #1a1a1a; color: white; border-color: #1a1a1a; }}
</style>
<script>
  var currentLang = '{language}';
  function setLang(lang) {{
    currentLang = lang;
    ['da','en','de','sv'].forEach(function(l) {{
      document.getElementById('btn-' + l).className = 'lang-btn' + (lang === l ? ' active' : '');
    }});
    document.querySelectorAll('.btn-news').forEach(function(a) {{
      a.href = a.href.split('?')[0] + '?lang=' + lang;
    }});
    document.getElementById('lang-field').value = lang;
  }}
</script>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>NBB — Ugens LinkedIn-opslag</h1>
    <p>Vælg en nyhed, eller skriv dit eget emne nedenfor</p>
    <div class="lang-toggle">
      <button id="btn-da" class="lang-btn{' active' if language == 'da' else ''}" onclick="setLang('da')">🇩🇰 Dansk</button>
      <button id="btn-en" class="lang-btn{' active' if language == 'en' else ''}" onclick="setLang('en')">🇬🇧 English</button>
      <button id="btn-de" class="lang-btn{' active' if language == 'de' else ''}" onclick="setLang('de')">🇩🇪 Deutsch</button>
      <button id="btn-sv" class="lang-btn{' active' if language == 'sv' else ''}" onclick="setLang('sv')">🇸🇪 Svenska</button>
    </div>
  </div>

  <div class="card">
    <div class="card-header">✏️ &nbsp;Eget emne eller begivenhed</div>
    <div class="card-body">
      <form action="/select/manual" method="POST">
        <input type="hidden" name="lang" id="lang-field" value="{language}">
        <textarea class="manual-input" name="input" placeholder="Fx: 'NBB deltager på Packtech-messen den 15. maj' — eller indsæt et link til en specifik nyhed"></textarea>
        <div class="manual-hint">Systemet skriver opslaget ud fra dit emne med denne uges budskab som omdrejningspunkt.</div>
        <button type="submit" class="btn-manual">Generer opslag →</button>
      </form>
    </div>
  </div>

  <div class="divider">eller vælg fra dagens fundne nyheder</div>

  <div class="section-label">Fundne nyheder ({len(candidates)})</div>
  {cards}
  {no_news}

  <div class="usp-note">
    <div class="label">Denne uges budskab</div>
    {usp_text}
  </div>
</div>
</body>
</html>"""


@app.route("/select/article/<int:idx>")
def select_article(idx):
    candidates = _state["candidates"]
    if idx < 0 or idx >= len(candidates):
        return redirect("/")
    lang = request.args.get("lang", _state["language"])
    if lang not in ("da", "en", "de", "sv"):
        lang = _state["language"]
    _q.put({"type": "selected", "article": candidates[idx], "language": lang})
    return redirect("/loading")


@app.route("/select/manual", methods=["POST"])
def select_manual():
    text = (request.form.get("input") or "").strip()
    if not text:
        return redirect("/")
    lang = request.form.get("lang", _state["language"])
    if lang not in ("da", "en", "de", "sv"):
        lang = _state["language"]
    _q.put({"type": "selected", "manual_text": text, "language": lang})
    return redirect("/loading")


@app.route("/loading")
def loading():
    return """<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NBB — Genererer opslag…</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f3f2ef; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
  .box { text-align: center; background: white; padding: 56px 48px; border-radius: 16px; box-shadow: 0 2px 16px rgba(0,0,0,0.1); max-width: 400px; }
  .spinner { width: 48px; height: 48px; border: 4px solid #e0e0e0; border-top-color: #0a66c2; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 24px; }
  @keyframes spin { to { transform: rotate(360deg); } }
  h2 { color: #1a1a1a; font-size: 20px; margin-bottom: 8px; }
  p { color: #888; font-size: 14px; line-height: 1.6; }
  .brand { margin-top: 32px; font-size: 11px; color: #ccc; font-weight: 600; letter-spacing: 1.5px; }
</style>
<script>
  (function poll() {
    fetch('/ready')
      .then(r => r.json())
      .then(d => { if (d.ready) { window.location.href = '/preview'; } else { setTimeout(poll, 1000); } })
      .catch(() => setTimeout(poll, 2000));
  })();
</script>
</head>
<body>
<div class="box">
  <div class="spinner"></div>
  <h2>Claude skriver dit opslag…</h2>
  <p>Det tager typisk 5–15 sekunder.<br>Siden opdaterer automatisk.</p>
  <div class="brand">NBB · NORDIC BIG BAG</div>
</div>
</body>
</html>"""


@app.route("/ready")
def ready():
    return jsonify({"ready": _state["post_ready"]})


@app.route("/image")
def image():
    path = (_state.get("pending_data") or {}).get("image_path", "")
    if path and os.path.exists(path):
        return send_file(os.path.abspath(path), mimetype="image/png")
    return "", 404


@app.route("/preview")
def preview():
    if not _state["pending_data"]:
        return redirect("/")

    pending = _state["pending_data"]
    post = pending.get("post_text", "")
    article = pending.get("article", {})
    language = pending.get("language", "da")
    usp = pending.get("usp", {})

    lang_flag = "🇩🇰" if language == "da" else "🇬🇧"
    lang_label = "Dansk" if language == "da" else "English"
    usp_text = usp.get(language, "")
    post_html = post.replace("\n", "<br>")

    if article.get("manual"):
        source_html = f"""
        <div class="news-source">
          <div class="label">Udgangspunkt</div>
          <div class="title">{article.get('title', '')}</div>
          <div class="meta">Manuelt angivet emne</div>
        </div>"""
    else:
        source_html = f"""
        <div class="news-source">
          <div class="label">Nyhed brugt som krog</div>
          <div class="title">{article.get('title', '')}</div>
          <div class="meta">{article.get('source', '')} · <a href="{article.get('url', '#')}" target="_blank" style="color:#0a66c2;">Læs artikel →</a></div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NBB — Godkend LinkedIn-opslag</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f3f2ef; min-height: 100vh; padding: 32px 16px; }}
  .container {{ max-width: 680px; margin: 0 auto; }}
  .header {{ text-align: center; margin-bottom: 32px; }}
  .header h1 {{ font-size: 22px; color: #1a1a1a; font-weight: 700; }}
  .header p {{ color: #666; margin-top: 6px; font-size: 14px; }}
  .badge {{ display: inline-flex; align-items: center; gap: 6px; background: #e8f0fe; color: #1a56db; border-radius: 20px; padding: 4px 12px; font-size: 13px; font-weight: 500; margin-top: 10px; }}
  .card {{ background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; margin-bottom: 20px; }}
  .card-header {{ padding: 16px 20px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; gap: 12px; }}
  .avatar {{ width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #0a66c2, #004182); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 18px; flex-shrink: 0; }}
  .profile-name {{ font-weight: 600; color: #1a1a1a; font-size: 15px; }}
  .profile-sub {{ color: #666; font-size: 13px; margin-top: 2px; }}
  .post-body {{ padding: 20px; font-size: 15px; line-height: 1.6; color: #1a1a1a; }}
  .news-source {{ margin: 0 20px 20px; padding: 12px 16px; background: #f8f9fa; border-radius: 8px; border-left: 3px solid #0a66c2; }}
  .news-source .label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #888; margin-bottom: 4px; }}
  .news-source .title {{ font-size: 14px; font-weight: 600; color: #1a1a1a; }}
  .news-source .meta {{ font-size: 12px; color: #888; margin-top: 4px; }}
  .usp-badge {{ margin: 0 20px 20px; padding: 10px 14px; background: #f0fdf4; border-radius: 8px; border-left: 3px solid #16a34a; font-size: 13px; color: #166534; }}
  .usp-badge .label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #888; margin-bottom: 4px; }}
  .actions {{ display: flex; gap: 12px; padding: 20px; border-top: 1px solid #f0f0f0; align-items: center; }}
  .btn-approve {{ flex: 1; padding: 14px; background: #0a66c2; color: white; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; border: none; text-decoration: none; display: block; text-align: center; transition: background 0.15s; }}
  .btn-approve:hover {{ background: #004182; }}
  .btn-back {{ padding: 14px 20px; color: #666; font-size: 14px; text-decoration: none; border-radius: 8px; transition: background 0.15s; white-space: nowrap; }}
  .btn-back:hover {{ background: #ebebeb; color: #1a1a1a; }}
  .info-row {{ display: flex; gap: 8px; padding: 12px 20px; border-top: 1px solid #f0f0f0; font-size: 12px; color: #888; flex-wrap: wrap; }}
  .info-pill {{ background: #f3f2ef; padding: 3px 10px; border-radius: 20px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>NBB — Godkend opslaget</h1>
    <p>Gennemse udkastet og godkend, eller gå tilbage og vælg en anden</p>
    <div class="badge">{lang_flag} {lang_label}</div>
  </div>

  <div class="card">
    <div class="card-header">
      <div class="avatar">N</div>
      <div>
        <div class="profile-name">NBB</div>
        <div class="profile-sub">Industriel emballage · Bigbags · Cirkulær økonomi</div>
      </div>
    </div>

    {source_html}

    <div class="post-body">{post_html}</div>

    <div style="margin: 0 20px 20px;">
      <img src="/image" alt="LinkedIn grafik" style="width:100%; border-radius:8px; display:block;">
    </div>

    <div class="usp-badge">
      <div class="label">Denne uges budskab</div>
      {usp_text}
    </div>

    <div class="info-row">
      <span class="info-pill">LinkedIn · NBB virksomhedsside</span>
      <span class="info-pill">{lang_flag} {lang_label}</span>
    </div>

    <div class="actions">
      <a href="/approve" class="btn-approve">✓ &nbsp;Godkend og publicer</a>
      <a href="/back" class="btn-back">← Vælg en anden</a>
    </div>
  </div>
</div>
</body>
</html>"""


@app.route("/approve")
def approve():
    _q.put({"type": "approved"})
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  body { font-family: -apple-system, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #f3f2ef; }
  .box { text-align: center; background: white; padding: 48px; border-radius: 16px; box-shadow: 0 2px 16px rgba(0,0,0,0.1); }
  .icon { font-size: 56px; margin-bottom: 16px; }
  h2 { color: #16a34a; font-size: 24px; }
  p { color: #666; margin-top: 8px; line-height: 1.6; }
</style></head>
<body><div class="box">
  <div class="icon">✅</div>
  <h2>Opslag godkendt!</h2>
  <p>Opslaget publiceres nu på NBBs LinkedIn-side.<br>Du kan lukke dette vindue.</p>
</div></body></html>"""


@app.route("/back")
def back():
    clear_pending()
    _q.put({"type": "back"})
    return redirect("/")
