import json
import os
from datetime import datetime
from backend.config import OUTPUT_DIR


def post_to_linkedin(post_text, article, language, usp_index, dummy=True):
    if dummy:
        return _save_locally(post_text, article, language, usp_index)
    # Rigtig LinkedIn-integration tilføjes her når vi er klar
    raise NotImplementedError("LinkedIn-integration ikke aktiveret endnu.")


def _save_locally(post_text, article, language, usp_index):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"{OUTPUT_DIR}/post_{timestamp}.json"

    data = {
        "posted_at": datetime.now().isoformat(),
        "language": language,
        "usp_index": usp_index,
        "article": article,
        "post_text": post_text,
        "status": "approved_dummy",
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Opslag gemt lokalt: {filename}")
    return filename
