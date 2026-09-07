from fastapi import APIRouter, Query
from app.services import weather_service
from app.models import WeatherData

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("", response_model=WeatherData)
async def get_weather(city: str = Query("Multan")):
    return await weather_service.get_weather(city)


@router.get("/cities")
async def list_cities():
    return sorted(weather_service.PAKISTAN_CITIES.keys())
