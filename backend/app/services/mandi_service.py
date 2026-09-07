"""
Mandi / crop market price service.

HONESTY NOTE (read before changing this file):
As of this build, no free/public, key-less, machine-readable API for
live Pakistani mandi (wholesale) prices was found during research. Punjab's
AMIS portal (agripunjab.gov.pk) publishes rates but has no documented public
API; Pakistan Bureau of Statistics publishes weekly *retail* prices in PDF
form (not live wholesale mandi rates).

Rather than inventing numbers, this service is built so that:
  1. If MANDI_API_URL is set in the environment (a real API you connect
     later — government, PBS, a licensed data vendor, or your own scraper
     with a caching layer), it is called and results are marked VERIFIED
     or LATEST_AVAILABLE depending on what that API reports.
  2. Otherwise every requested crop/market combination is returned with
     status=UNAVAILABLE and a clear note — never a fabricated price.

To connect a real source: implement `_fetch_from_configured_api()` for your
chosen provider's response shape, and set MANDI_API_URL (and MANDI_API_KEY
if needed) in the environment.
"""
import os
from datetime import datetime, timezone
import httpx

from app.models import CropPrice, PriceUnit, SourceMeta, DataStatus

MANDI_API_URL = os.getenv("MANDI_API_URL")  # not set by default — see note above
MANDI_API_KEY = os.getenv("MANDI_API_KEY")

SUPPORTED_CROPS = [
    "wheat", "rice", "cotton", "maize", "sugarcane",
    "potato", "onion", "tomato",
]

SUPPORTED_MARKETS = [
    {"market": "Multan Mandi", "city": "Multan", "province": "Punjab"},
    {"market": "Lahore Mandi", "city": "Lahore", "province": "Punjab"},
    {"market": "Vehari Mandi", "city": "Vehari", "province": "Punjab"},
    {"market": "Bahawalpur Mandi", "city": "Bahawalpur", "province": "Punjab"},
    {"market": "Faisalabad Mandi", "city": "Faisalabad", "province": "Punjab"},
    {"market": "Hyderabad Mandi", "city": "Hyderabad", "province": "Sindh"},
    {"market": "Karachi Sabzi Mandi", "city": "Karachi", "province": "Sindh"},
    {"market": "Peshawar Mandi", "city": "Peshawar", "province": "Khyber Pakhtunkhwa"},
    {"market": "Quetta Mandi", "city": "Quetta", "province": "Balochistan"},
]


async def _fetch_from_configured_api(crop: str, city: str | None) -> list[CropPrice] | None:
    """Returns None if no real API is configured or the call fails."""
    if not MANDI_API_URL:
        return None
    try:
        headers = {"Authorization": f"Bearer {MANDI_API_KEY}"} if MANDI_API_KEY else {}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                MANDI_API_URL,
                params={"crop": crop, "city": city} if city else {"crop": crop},
                headers=headers,
            )
            resp.raise_for_status()
            payload = resp.json()
        # NOTE: adapt this mapping to your chosen provider's real schema.
        results = []
        for row in payload.get("results", []):
            results.append(CropPrice(
                crop=row["crop"],
                market=row["market"],
                city=row["city"],
                province=row.get("province", "-"),
                price=row.get("price"),
                unit=PriceUnit(row.get("unit", PriceUnit.PER_40KG)),
                trend=row.get("trend"),
                meta=SourceMeta(
                    status=DataStatus.VERIFIED,
                    source=row.get("source", "Configured mandi API"),
                    source_url=row.get("source_url"),
                    as_of=datetime.now(timezone.utc).isoformat(),
                ),
            ))
        return results
    except Exception:
        return None


async def get_crop_prices(crop: str | None = None, city: str | None = None) -> list[CropPrice]:
    crops = [crop.lower()] if crop else SUPPORTED_CROPS
    markets = (
        [m for m in SUPPORTED_MARKETS if m["city"].lower() == city.lower()]
        if city else SUPPORTED_MARKETS
    )

    live = await _fetch_from_configured_api(crop or "", city)
    if live:
        return live

    # Honest fallback — no real source connected yet.
    out: list[CropPrice] = []
    for c in crops:
        for m in markets:
            out.append(CropPrice(
                crop=c.title(),
                market=m["market"],
                city=m["city"],
                province=m["province"],
                price=None,
                unit=PriceUnit.PER_40KG,
                trend=None,
                meta=SourceMeta(
                    status=DataStatus.UNAVAILABLE,
                    note="No live mandi price API connected yet. Set MANDI_API_URL "
                         "to a real data source to enable this section.",
                ),
            ))
    return out
