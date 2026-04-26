import json
import os
from datetime import datetime


def publish_to_website(post_text, article, language, dummy=True):
    if dummy:
        return _save_snippet(post_text, article, language)
    # Rigtig integration: WordPress REST API eller lignende
    raise NotImplementedError("Website-integration ikke aktiveret endnu.")


def _save_snippet(post_text, article, language):
    os.makedirs("output/website", exist_ok=True)

    # Gem JSON til brug for CMS/API
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    json_path = f"output/website/post_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "published_at": datetime.now().isoformat(),
            "language": language,
            "article_title": article.get("title", ""),
            "article_url": article.get("url", ""),
            "article_source": article.get("source", ""),
            "post_text": post_text,
        }, f, ensure_ascii=False, indent=2)

    # Opdater samlet feed-fil (bruges af hjemmesidens widget)
    feed_path = "output/website/feed.json"
    feed = []
    if os.path.exists(feed_path):
        with open(feed_path, encoding="utf-8") as f:
            feed = json.load(f)

    feed.insert(0, {
        "date": datetime.now().strftime("%d. %b %Y"),
        "language": language,
        "title": article.get("title", ""),
        "url": article.get("url", ""),
        "source": article.get("source", ""),
        "excerpt": post_text[:220].rsplit(" ", 1)[0] + "…",
    })
    feed = feed[:10]  # Behold kun de 10 seneste

    with open(feed_path, "w", encoding="utf-8") as f:
        json.dump(feed, f, ensure_ascii=False, indent=2)

    print(f"✓ Website-feed opdateret: {feed_path}")
    return feed_path
