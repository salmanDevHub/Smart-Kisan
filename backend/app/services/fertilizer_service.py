"""
Fertilizer price service — same honesty contract as mandi_service.py.
No free/public API for live Pakistani/Indian fertilizer (Urea/DAP/NP/SOP/MOP)
prices was found. This is architected to plug into a real source
(FERTILIZER_API_URL) later; until then, every item is UNAVAILABLE, never
a guessed number — but we still list the real companies and their real
product names so the UI has something meaningful to show per-brand.
"""
import os
from datetime import datetime, timezone
import httpx

from app.models import FertilizerPrice, PriceUnit, SourceMeta, DataStatus

FERTILIZER_API_URL = os.getenv("FERTILIZER_API_URL")
FERTILIZER_API_KEY = os.getenv("FERTILIZER_API_KEY")

# Real companies + their real product/brand names (Pakistan + India).
# No prices here on purpose — see honesty contract above. Add a real
# price feed via FERTILIZER_API_URL when one is available, or replace
# `price=None` below with numbers you manually verify and keep updated
# yourself (in that case also switch status to DataStatus.LATEST_AVAILABLE
# and fill in `as_of` with the date you checked).
TRACKED_PRODUCTS: list[dict] = [
    # --- Pakistan ---
    {"name": "Urea", "brand": "Engro Urea", "company": "Engro Fertilizers", "country": "Pakistan"},
    {"name": "DAP", "brand": "Engro DAP", "company": "Engro Fertilizers", "country": "Pakistan"},
    {"name": "NPK", "brand": "Engro Zarkhez NP", "company": "Engro Fertilizers", "country": "Pakistan"},
    {"name": "Urea", "brand": "Sona Urea", "company": "Fauji Fertilizer Company (FFC)", "country": "Pakistan"},
    {"name": "DAP", "brand": "FFC Sona DAP", "company": "Fauji Fertilizer Company (FFC)", "country": "Pakistan"},
    {"name": "DAP", "brand": "FFBL DAP", "company": "Fauji Fertilizer Bin Qasim (FFBL)", "country": "Pakistan"},
    {"name": "Urea", "brand": "Fatima Urea", "company": "Fatima Fertilizer", "country": "Pakistan"},
    {"name": "DAP", "brand": "Fatimafos DAP", "company": "Fatima Fertilizer", "country": "Pakistan"},
    {"name": "NPK", "brand": "Fatima NP", "company": "Fatima Fertilizer", "country": "Pakistan"},
    {"name": "Urea", "brand": "Pak Arab Urea", "company": "Pak Arab Fertilizers", "country": "Pakistan"},
    {"name": "SOP", "brand": "Ansaar Sulphate", "company": "Ansaar Management (SOP)", "country": "Pakistan"},
    # --- India ---
    {"name": "Urea", "brand": "IFFCO Urea", "company": "IFFCO", "country": "India"},
    {"name": "DAP", "brand": "IFFCO DAP", "company": "IFFCO", "country": "India"},
    {"name": "NPK", "brand": "IFFCO NPK", "company": "IFFCO", "country": "India"},
    {"name": "DAP", "brand": "Gromor DAP", "company": "Coromandel International", "country": "India"},
    {"name": "NPK", "brand": "Gromor NPK", "company": "Coromandel International", "country": "India"},
    {"name": "Urea", "brand": "Chambal Urea", "company": "Chambal Fertilizers", "country": "India"},
    {"name": "Urea", "brand": "Kisan Urea", "company": "National Fertilizers Ltd (NFL)", "country": "India"},
    {"name": "NPK", "brand": "Suphala NPK", "company": "RCF (Rashtriya Chemicals & Fertilizers)", "country": "India"},
    {"name": "Urea", "brand": "RCF Urea", "company": "RCF (Rashtriya Chemicals & Fertilizers)", "country": "India"},
    {"name": "Urea", "brand": "Nagarjuna Urea", "company": "Nagarjuna Fertilizers", "country": "India"},
]


async def _fetch_from_configured_api() -> list[FertilizerPrice] | None:
    if not FERTILIZER_API_URL:
        return None
    try:
        headers = {"Authorization": f"Bearer {FERTILIZER_API_KEY}"} if FERTILIZER_API_KEY else {}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(FERTILIZER_API_URL, headers=headers)
            resp.raise_for_status()
            payload = resp.json()
        results = []
        for row in payload.get("results", []):
            prev = row.get("previous_price")
            price = row.get("price")
            change_pct = (
                round((price - prev) / prev * 100, 2)
                if price is not None and prev not in (None, 0) else None
            )
            results.append(FertilizerPrice(
                name=row["name"],
                brand=row.get("brand"),
                price=price,
                previous_price=prev,
                change_pct=change_pct,
                city=row.get("city"),
                unit=PriceUnit(row.get("unit", PriceUnit.PER_BAG_50KG)),
                meta=SourceMeta(
                    status=DataStatus.VERIFIED,
                    source=row.get("source", "Configured fertilizer API"),
                    source_url=row.get("source_url"),
                    as_of=datetime.now(timezone.utc).isoformat(),
                ),
            ))
        return results
    except Exception:
        return None


async def get_fertilizer_prices() -> list[FertilizerPrice]:
    live = await _fetch_from_configured_api()
    if live:
        return live

    return [
        FertilizerPrice(
            name=item["name"],
            brand=f'{item["brand"]} ({item["company"]}, {item["country"]})',
            price=None,
            previous_price=None,
            change_pct=None,
            meta=SourceMeta(
                status=DataStatus.UNAVAILABLE,
                note="No live fertilizer price API connected yet. Set "
                     "FERTILIZER_API_URL to a real data source to enable pricing.",
            ),
        )
        for item in TRACKED_PRODUCTS
    ]