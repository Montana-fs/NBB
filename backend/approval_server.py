import json
import os
import threading
import webbrowser
from flask import Flask, request, redirect, url_for

app = Flask(__name__)
_decision = {"action": None}
_pending = {}
_shutdown_event = threading.Event()


def load_pending(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    _pending.update(data)


def get_decision():
    return _decision["action"]


def wait_for_decision():
    _shutdown_event.wait()
    return _decision["action"]


@app.route("/")
def preview():
    post = _pending.get("post_text", "")
    article = _pending.get("article", {})
    language = _pending.get("language", "da")
    usp = _pending.get("usp", {})

    lang_flag = "🇩🇰" if language == "da" else "🇬🇧"
    lang_label = "Dansk" if language == "da" else "English"
    usp_text = usp.get(language, "")

    post_html = post.replace("\n", "<br>")

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
  .actions {{ display: flex; gap: 12px; padding: 20px; border-top: 1px solid #f0f0f0; }}
  .btn {{ flex: 1; padding: 14px; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; border: none; transition: all 0.15s; text-align: center; text-decoration: none; display: block; }}
  .btn-approve {{ background: #0a66c2; color: white; }}
  .btn-approve:hover {{ background: #004182; }}
  .btn-reject {{ background: white; color: #cc0000; border: 2px solid #cc0000; }}
  .btn-reject:hover {{ background: #fff5f5; }}
  .info-row {{ display: flex; gap: 8px; padding: 12px 20px; border-top: 1px solid #f0f0f0; font-size: 12px; color: #888; }}
  .info-pill {{ background: #f3f2ef; padding: 3px 10px; border-radius: 20px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>NBB — Ugentligt LinkedIn-opslag</h1>
    <p>Gennemse udkastet og godkend eller afvis med ét klik</p>
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

    <div class="news-source">
      <div class="label">Nyhed brugt som krog</div>
      <div class="title">{article.get('title', '')}</div>
      <div class="meta">{article.get('source', '')} · <a href="{article.get('url', '#')}" target="_blank" style="color:#0a66c2;">Læs artikel →</a></div>
    </div>

    <div class="post-body">{post_html}</div>

    <div class="usp-badge">
      <div class="label">Denne uges budskab</div>
      {usp_text}
    </div>

    <div class="info-row">
      <span class="info-pill">LinkedIn · NBB virksomhedsside</span>
      <span class="info-pill">Planlagt: Tirsdag</span>
      <span class="info-pill">{lang_flag} {lang_label}</span>
    </div>

    <div class="actions">
      <a href="/approve" class="btn btn-approve">✓ &nbsp;Godkend og post</a>
      <a href="/reject" class="btn btn-reject">✕ &nbsp;Afvis</a>
    </div>
  </div>
</div>
</body>
</html>"""


@app.route("/approve")
def approve():
    _decision["action"] = "approved"
    _shutdown_event.set()
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
body {{ font-family: -apple-system, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #f3f2ef; }}
.box {{ text-align: center; background: white; padding: 48px; border-radius: 16px; box-shadow: 0 2px 16px rgba(0,0,0,0.1); }}
.icon {{ font-size: 56px; margin-bottom: 16px; }}
h2 {{ color: #16a34a; font-size: 24px; }}
p {{ color: #666; margin-top: 8px; }}
</style></head>
<body><div class="box">
<div class="icon">✅</div>
<h2>Opslag godkendt!</h2>
<p>Opslaget er nu publiceret på NBBs LinkedIn-side.<br>Du kan lukke dette vindue.</p>
</div></body></html>"""


@app.route("/reject")
def reject():
    _decision["action"] = "rejected"
    _shutdown_event.set()
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
body {{ font-family: -apple-system, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #f3f2ef; }}
.box {{ text-align: center; background: white; padding: 48px; border-radius: 16px; box-shadow: 0 2px 16px rgba(0,0,0,0.1); }}
.icon {{ font-size: 56px; margin-bottom: 16px; }}
h2 {{ color: #cc0000; font-size: 24px; }}
p {{ color: #666; margin-top: 8px; }}
</style></head>
<body><div class="box">
<div class="icon">🚫</div>
<h2>Opslag afvist</h2>
<p>Opslaget er ikke publiceret.<br>Systemet genererer et nyt udkast næste uge.<br>Du kan lukke dette vindue.</p>
</div></body></html>"""


def start(pending_path, port=5001):
    load_pending(pending_path)
    server = threading.Thread(
        target=lambda: app.run(port=port, debug=False, use_reloader=False),
        daemon=True,
    )
    server.start()
    webbrowser.open(f"http://localhost:{port}")
    return wait_for_decision()
