from fastapi import APIRouter, Query
from app.services import news_service
from app.models import NewsItem

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("", response_model=list[NewsItem])
async def list_news(limit: int = Query(20, ge=1, le=50)):
    return await news_service.get_agriculture_news(limit=limit)
