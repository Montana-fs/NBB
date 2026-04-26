import feedparser
import re
from datetime import datetime, timezone
from backend.config import RSS_FEEDS, KEYWORDS


def _score_article(entry):
    text = (
        getattr(entry, "title", "") + " " +
        getattr(entry, "summary", "") + " " +
        getattr(entry, "description", "")
    ).lower()
    return sum(1 for kw in KEYWORDS if kw.lower() in text)


def _clean_html(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()


def collect_news():
    candidates = []

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url, request_headers={"User-Agent": "NBB-NewsBot/1.0"})
            for entry in feed.entries[:10]:
                score = _score_article(entry)
                if score == 0:
                    continue
                candidates.append({
                    "score": score,
                    "title": _clean_html(getattr(entry, "title", "")),
                    "summary": _clean_html(getattr(entry, "summary", getattr(entry, "description", ""))[:800]),
                    "url": getattr(entry, "link", ""),
                    "source": feed.feed.get("title", url),
                    "published": getattr(entry, "published", datetime.now(timezone.utc).isoformat()),
                })
        except Exception:
            continue

    if not candidates:
        return None, []

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[0], candidates[1:5]
