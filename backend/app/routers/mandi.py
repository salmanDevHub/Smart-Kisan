from fastapi import APIRouter, Query
from app.services import mandi_service
from app.models import CropPrice

router = APIRouter(prefix="/api/mandi", tags=["mandi"])


@router.get("/prices", response_model=list[CropPrice])
async def crop_prices(crop: str | None = None, city: str | None = None):
    return await mandi_service.get_crop_prices(crop=crop, city=city)


@router.get("/crops")
async def list_crops():
    return mandi_service.SUPPORTED_CROPS


@router.get("/markets")
async def list_markets():
    return mandi_service.SUPPORTED_MARKETS
