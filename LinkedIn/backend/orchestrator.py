import json
import os
import sys
from datetime import datetime

from dotenv import load_dotenv

from backend.config import APPROVAL_PORT, PENDING_FILE
from backend.news_collector import collect_news, article_from_topic, article_from_url
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
from backend.image_generator import generate as generate_image
from backend import approval_server


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
        print("⚠️  Ingen relevante nyheder fundet — du kan stadig bruge eget emne.\n")
        candidates = []
    else:
        candidates = [best] + fallbacks
        print(f"✓ Fandt {len(candidates)} relevante nyheder\n")

    approval_server.setup(candidates, usp, language, usp_index)

    print("🌐 Åbner godkendelsesside i browseren…")
    print(f"   (http://localhost:{APPROVAL_PORT})\n")
    approval_server.start(port=APPROVAL_PORT)

    pending_data = None

    while True:
        action = approval_server.next_action()

        if action["type"] == "selected":
            post_language = action.get("language", language)

            if "article" in action:
                article = action["article"]
                print(f"📰 Valgt nyhed: \"{article['title'][:65]}\"")
            else:
                text = action["manual_text"]
                print(f"✏️  Manuel input: \"{text[:65]}\"")
                if text.startswith(("http://", "https://")):
                    print("   Henter artikel fra URL…")
                    article = article_from_url(text)
                    if not article:
                        print("   ⚠️  Kunne ikke hente URL — bruger tekst som emne")
                        article = article_from_topic(text)
                else:
                    article = article_from_topic(text)

            lang_label = {"da": "Dansk", "en": "English", "de": "Deutsch", "sv": "Svenska"}.get(post_language, post_language)
            print(f"🌐 Sprog: {lang_label}")
            print("✍️  Claude skriver opslag…")
            post_text = write_post(article, usp, post_language)
            print("✓ Opslag skrevet")

            image_path = "state/pending_image.png"
            generate_image(article, post_language, usp_index, image_path)
            print("✓ Grafik genereret\n")

            pending_data = {
                "article": article,
                "post_text": post_text,
                "language": post_language,
                "usp": usp,
                "usp_index": usp_index,
                "image_path": image_path,
                "generated_at": datetime.now().isoformat(),
            }
            os.makedirs("state", exist_ok=True)
            with open(PENDING_FILE, "w", encoding="utf-8") as f:
                json.dump(pending_data, f, ensure_ascii=False, indent=2)

            approval_server.set_pending(pending_data)

        elif action["type"] == "back":
            print("↩️  Går tilbage — venter på nyt valg…\n")
            pending_data = None

        elif action["type"] == "approved":
            pending_data = approval_server.get_pending()
            if not pending_data:
                print("⚠️  Ingen afventende opslag — afslutter.")
                break

            article = pending_data["article"]
            print("✓ Godkendt — publicerer opslag…")
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

    print("\n── Færdig ───────────────────────────────────────\n")
