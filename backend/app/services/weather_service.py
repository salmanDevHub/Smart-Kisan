"""
Weather service — backed by Open-Meteo (https://open-meteo.com), which is
free, requires no API key, and returns real live/forecast data. This is a
genuinely live source, so results are marked VERIFIED.
"""
from datetime import datetime, timezone
import httpx

from app.models import WeatherData, SourceMeta, DataStatus

# A small curated list of Pakistani cities with coordinates.
# Extend this freely — it's just lookup data, not a data source itself.
PAKISTAN_CITIES = {
    "multan": (30.1575, 71.5249),
    "lahore": (31.5497, 74.3436),
    "karachi": (24.8607, 67.0011),
    "islamabad": (33.6844, 73.0479),
    "faisalabad": (31.4504, 73.1350),
    "peshawar": (34.0151, 71.5249),
    "quetta": (30.1798, 66.9750),
    "vehari": (30.0453, 72.3489),
    "bahawalpur": (29.3956, 71.6836),
    "sargodha": (32.0836, 72.6711),
    "sialkot": (32.4945, 74.5229),
    "rahim yar khan": (28.4212, 70.2989),
}

WMO_CONDITIONS = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


async def get_weather(city: str) -> WeatherData:
    key = city.strip().lower()
    coords = PAKISTAN_CITIES.get(key)
    if not coords:
        return WeatherData(
            city=city,
            meta=SourceMeta(
                status=DataStatus.UNAVAILABLE,
                note=f"'{city}' is not in the supported city list yet.",
            ),
        )

    lat, lon = coords
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,"
                    "precipitation_probability,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "Asia/Karachi",
        "forecast_days": 4,
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        current = data.get("current", {})
        daily = data.get("daily", {})
        forecast = []
        for i, date in enumerate(daily.get("time", [])[1:], start=0):
            code = daily.get("weather_code", [None] * 10)[i + 1]
            forecast.append({
                "date": date,
                "condition": WMO_CONDITIONS.get(code, "Unknown"),
                "max_c": daily.get("temperature_2m_max", [None])[i + 1],
                "min_c": daily.get("temperature_2m_min", [None])[i + 1],
                "rain_probability_pct": daily.get("precipitation_probability_max", [None])[i + 1],
            })

        return WeatherData(
            city=city.title(),
            temperature_c=current.get("temperature_2m"),
            feels_like_c=current.get("apparent_temperature"),
            humidity_pct=current.get("relative_humidity_2m"),
            wind_kph=current.get("wind_speed_10m"),
            rain_probability_pct=current.get("precipitation_probability"),
            condition=WMO_CONDITIONS.get(current.get("weather_code"), "Unknown"),
            forecast_3day=forecast,
            meta=SourceMeta(
                status=DataStatus.VERIFIED,
                source="Open-Meteo",
                source_url="https://open-meteo.com",
                as_of=datetime.now(timezone.utc).isoformat(),
            ),
        )
    except Exception as e:
        return WeatherData(
            city=city,
            meta=SourceMeta(
                status=DataStatus.UNAVAILABLE,
                note=f"Weather fetch failed: {e}",
            ),
        )
