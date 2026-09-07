from fastapi import APIRouter, Query
from app.data.fertilizer_catalog import COMPANIES, PRODUCTS, ALL_CATEGORIES

router = APIRouter(prefix="/api/marketplace", tags=["marketplace"])


@router.get("/companies")
async def list_companies():
    return COMPANIES


@router.get("/categories")
async def list_categories():
    return ALL_CATEGORIES


@router.get("/products")
async def list_products(
    company_id: str | None = None,
    category: str | None = None,
    search: str | None = None,
):
    results = PRODUCTS
    if company_id:
        results = [p for p in results if p.company_id == company_id]
    if category:
        results = [p for p in results if p.category == category]
    if search:
        s = search.lower()
        results = [
            p for p in results
            if s in p.name.lower() or s in p.description.lower()
        ]
    # attach company name for convenience
    company_lookup = {c.id: c.name for c in COMPANIES}
    return [
        {**p.model_dump(), "company_name": company_lookup.get(p.company_id, "Unknown")}
        for p in results
    ]
