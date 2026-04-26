import json
import os
from datetime import datetime
from backend.config import USPS, LANGUAGES, STATE_FILE


def _default_state():
    return {
        "usp_index": 0,
        "language_index": 0,
        "posts": [],
    }


def load_state():
    if not os.path.exists(STATE_FILE):
        return _default_state()
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_current_rotation(state):
    usp = USPS[state["usp_index"] % len(USPS)]
    lang = LANGUAGES[state["language_index"] % len(LANGUAGES)]
    return usp, lang


def advance_rotation(state):
    state["usp_index"] = (state["usp_index"] + 1) % len(USPS)
    state["language_index"] = (state["language_index"] + 1) % len(LANGUAGES)
    return state


def record_post(state, post_data, approved):
    state["posts"].append({
        "date": datetime.now().isoformat(),
        "approved": approved,
        "language": post_data.get("language"),
        "usp_index": post_data.get("usp_index"),
        "headline": post_data.get("article", {}).get("title", ""),
    })
    return state
