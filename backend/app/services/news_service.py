"""
News service — pulls real items from public RSS feeds of Pakistani news
outlets that cover agriculture/business. We do NOT invent headlines; if a
feed is unreachable it is simply skipped and the overall status reflects
whatever was actually retrieved.

Categorisation is a simple keyword heuristic over the real headline/summary
text — it never changes the underlying facts, only labels them.
"""
from datetime import datetime, timezone
import feedparser
import httpx

from app.models import NewsItem

FEEDS = [
    {"url": "https://www.dawn.com/feeds/business", "source": "Dawn Business"},
    {"url": "https://www.brecorder.com/feeds/business-finance", "source": "Business Recorder"},
    {"url": "https://tribune.com.pk/feed/business", "source": "Express Tribune Business"},
]

CATEGORY_KEYWORDS = {
    "Fertilizer": ["fertilizer", "fertiliser", "urea", "dap", "sona urea", "fauji fertilizer"],
    "Weather": ["rain", "monsoon", "flood", "heatwave", "drought", "weather", "cyclone"],
    "Crops": ["wheat", "cotton", "rice", "sugarcane", "maize", "crop", "harvest", "sowing"],
    "Policy": ["subsidy", "policy", "ministry", "government", "notification", "SBP", "budget"],
    "Import/Export": ["import", "export", "tariff", "customs", "shipment"],
    "Pest/Disease": ["pest", "locust", "disease", "blight", "infestation"],
    "Market": ["market", "mandi", "price", "rate"],
}


def _categorize(text: str) -> str:
    lowered = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            return category
    return "General Agriculture"


AGRI_FILTER_KEYWORDS = [
    "wheat", "cotton", "rice", "sugarcane", "maize", "crop", "agri", "farm",
    "fertilizer", "fertiliser", "urea", "dap", "mandi", "harvest", "sowing",
    "pesticide", "irrigation", "locust", "livestock", "kissan", "kisan",
]


async def get_agriculture_news(limit: int = 20) -> list[NewsItem]:
    items: list[NewsItem] = []

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        for feed in FEEDS:
            try:
                resp = await client.get(feed["url"], headers={"User-Agent": "SmartKisan/1.0"})
                resp.raise_for_status()
                parsed = feedparser.parse(resp.text)
            except Exception:
                continue  # this source is skipped, not faked

            for entry in parsed.entries:
                title = getattr(entry, "title", "").strip()
                summary_raw = getattr(entry, "summary", "") or getattr(entry, "description", "")
                combined = f"{title} {summary_raw}".lower()

                if not any(kw in combined for kw in AGRI_FILTER_KEYWORDS):
                    continue  # keep the feed focused on agriculture-relevant items

                published = getattr(entry, "published", None)
                link = getattr(entry, "link", "")

                # Plain-text summary trimmed to a short length — this is a
                # direct excerpt of the source's own summary field, not an
                # AI paraphrase (an AI summarizer can be wired in later via
                # ai_service.summarize()).
                clean_summary = summary_raw.replace("\n", " ").strip()
                if len(clean_summary) > 220:
                    clean_summary = clean_summary[:217] + "..."

                items.append(NewsItem(
                    title=title,
                    summary=clean_summary or "(no summary available from source)",
                    published=published,
                    category=_categorize(combined),
                    source=feed["source"],
                    source_url=link,
                ))

    return items[:limit]
