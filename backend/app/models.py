"""
Shared data models for Smart Kisan.

DATA QUALITY CONTRACT (see project spec):
Every "live" data item must carry:
  - status: one of DataStatus
  - source: where it came from (or None if unavailable)
  - source_url: link to source (or None)
  - as_of: ISO timestamp of when this data point was recorded (or None)
Nothing is ever fabricated. If a live fetch fails, status becomes
UNAVAILABLE and no numeric value is invented.
"""
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel


class DataStatus(str, Enum):
    VERIFIED = "verified"                # freshly fetched from a live source this request
    LATEST_AVAILABLE = "latest_available" # fetched, but source itself is not real-time (e.g. weekly PDF)
    UNAVAILABLE = "unavailable"           # no reliable source could be reached


class SourceMeta(BaseModel):
    status: DataStatus
    source: Optional[str] = None
    source_url: Optional[str] = None
    as_of: Optional[str] = None
    note: Optional[str] = None


class NewsItem(BaseModel):
    title: str
    summary: str
    published: Optional[str] = None
    category: str
    source: str
    source_url: str


class WeatherData(BaseModel):
    city: str
    temperature_c: Optional[float] = None
    feels_like_c: Optional[float] = None
    humidity_pct: Optional[float] = None
    wind_kph: Optional[float] = None
    rain_probability_pct: Optional[float] = None
    condition: Optional[str] = None
    forecast_3day: list[dict[str, Any]] = []
    meta: SourceMeta


class PriceUnit(str, Enum):
    PER_40KG = "40kg"
    PER_100KG = "100kg"
    PER_MAUND = "maund (37.32kg)"
    PER_KG = "kg"
    PER_BAG_50KG = "50kg bag"


class CropPrice(BaseModel):
    crop: str
    market: str
    city: str
    province: str
    price: Optional[float] = None
    unit: PriceUnit
    trend: Optional[str] = None  # "up" | "down" | "flat" | None
    meta: SourceMeta


class FertilizerPrice(BaseModel):
    name: str
    brand: Optional[str] = None
    price: Optional[float] = None
    previous_price: Optional[float] = None
    change_pct: Optional[float] = None
    city: Optional[str] = None
    unit: PriceUnit = PriceUnit.PER_BAG_50KG
    meta: SourceMeta


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []
    city: Optional[str] = None
