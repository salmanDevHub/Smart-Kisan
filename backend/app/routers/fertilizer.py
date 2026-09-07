from fastapi import APIRouter
from app.services import fertilizer_service
from app.models import FertilizerPrice

router = APIRouter(prefix="/api/fertilizer", tags=["fertilizer"])


@router.get("/prices", response_model=list[FertilizerPrice])
async def fertilizer_prices():
    return await fertilizer_service.get_fertilizer_prices()
