import json
import os
import sys
from datetime import datetime

from dotenv import load_dotenv

from backend.config import APPROVAL_PORT, PENDING_FILE
from backend.news_collector import collect_news
from backend.post_writer import write_post
from backend.state_manager import (
    advance_rotation,
    get_current_rotation,
    load_state,
    record_post,
    save_state,
)
from backend.linkedin_client import post_to_linkedin
from backend.website_publisher import publish_to_website
from backend import approval_server


def _present_article(article, usp, language, usp_index, attempt, dummy_mode):
    print(f"✍️  Claude skriver opslag (forsøg {attempt})…")
    post_text = write_post(article, usp, language)
    print("✓ Opslag skrevet\n")

    pending_data = {
        "article": article,
        "post_text": post_text,
        "language": language,
        "usp": usp,
        "usp_index": usp_index,
        "generated_at": datetime.now().isoformat(),
    }
    os.makedirs("state", exist_ok=True)
    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(pending_data, f, ensure_ascii=False, indent=2)

    print("🌐 Åbner godkendelsesside i browseren…")
    print(f"   (http://localhost:{APPROVAL_PORT})\n")

    # Genstart approval-serveren med frisk tilstand ved hvert forsøg
    approval_server._decision["action"] = None
    approval_server._shutdown_event.clear()
    approval_server._pending.clear()
    decision = approval_server.start(PENDING_FILE, port=APPROVAL_PORT)

    return decision, pending_data


def run():
    load_dotenv()
    dummy_mode = os.getenv("DUMMY_MODE", "true").lower() == "true"

    print("\n── NBB LinkedIn-system ──────────────────────────")
    print(f"  Kører: {datetime.now().strftime('%d. %b %Y %H:%M')}")
    print(f"  Tilstand: {'dummy (ingen rigtige integrationer)' if dummy_mode else 'produktion'}")
    print("─────────────────────────────────────────────────\n")

    state = load_state()
    usp, language = get_current_rotation(state)
    usp_index = state["usp_index"]

    print(f"📍 Sprog denne uge: {'Dansk' if language == 'da' else 'English'}")
    print(f"📍 Budskab denne uge: {usp[language][:60]}…\n")

    print("🔍 Søger efter relevante nyheder…")
    best, fallbacks = collect_news()

    if not best:
        print("⚠️  Ingen relevante nyheder fundet. Prøv igen senere.")
        sys.exit(1)

    candidates = [best] + fallbacks
    print(f"✓ Fandt {len(candidates)} relevante nyheder\n")

    for attempt, article in enumerate(candidates, start=1):
        print(f"📰 Nyhed {attempt}/{len(candidates)}: \"{article['title'][:65]}\"")
        print(f"   Kilde: {article['source']} (score: {article['score']})\n")

        decision, pending_data = _present_article(
            article, usp, language, usp_index, attempt, dummy_mode
        )

        if decision == "approved":
            print("\n✓ Godkendt — publicerer opslag…")
            post_to_linkedin(
                pending_data["post_text"], article, language, usp_index, dummy=dummy_mode
            )
            publish_to_website(
                pending_data["post_text"], article, language, dummy=dummy_mode
            )
            state = advance_rotation(state)
            state = record_post(state, pending_data, approved=True)
            save_state(state)
            print("✓ Rotations-tilstand opdateret til næste uge")
            break
        else:
            state = record_post(state, pending_data, approved=False)
            save_state(state)
            if attempt < len(candidates):
                print(f"\n✗ Afvist — henter næstbedste nyhed ({attempt + 1}/{len(candidates)})…\n")
            else:
                print("\n✗ Alle nyheder afvist — ingen opslag denne uge.")

    print("\n── Færdig ───────────────────────────────────────\n")
