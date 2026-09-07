"""
AI Agriculture Assistant — OpenRouter (OpenAI-compatible), grounded with
whatever real data the platform currently has (weather, mandi prices,
fertilizer prices, news).

Grounding rule: the system prompt explicitly forbids the model from
presenting UNAVAILABLE data as if it were current/live. The model is told
what is verified vs. unavailable for this specific query before it answers.

No API key is configured by default (per project setup) — OPENROUTER_API_KEY
must be set in the environment for this to work. Until then, the endpoint
returns a clear, honest "not configured" message instead of failing oddly
or pretending to answer.
"""
import os
import httpx

from app.models import ChatRequest
from app.services import weather_service, mandi_service, fertilizer_service

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# "openrouter/free" auto-picks a currently-working free model, so this
# doesn't break every time a specific model gets deprecated. Override in
# .env with OPENROUTER_MODEL if you want a specific model instead.
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are Smart Kisan's AI agriculture assistant for Pakistani farmers.
Rules you must always follow:
1. Answer in the same language style the farmer used (Urdu, Roman Urdu, or English).
2. You will be given a CONTEXT block with live data status for weather/mandi/fertilizer.
   If a data point's status is "unavailable", you MUST tell the farmer that specific
   data isn't available right now instead of guessing or inventing a number.
3. Never invent prices, rates, or statistics. Only state numbers that appear in CONTEXT.
4. Keep answers short, practical, and in simple language a farmer with limited
   technical background can understand.
5. For agronomy questions (pests, disease symptoms, spray timing) you may use general
   agricultural knowledge, but say plainly this is general guidance, not a substitute
   for local agriculture extension office advice for serious problems.
"""


async def _build_context(city: str | None) -> str:
    parts = []
    if city:
        w = await weather_service.get_weather(city)
        if w.meta.status.value == "unavailable":
            parts.append(f"WEATHER ({city}): unavailable — {w.meta.note}")
        else:
            parts.append(
                f"WEATHER ({city}): {w.condition}, {w.temperature_c}°C, "
                f"rain probability {w.rain_probability_pct}%, status=verified, "
                f"source={w.meta.source}"
            )

    fert = await fertilizer_service.get_fertilizer_prices()
    fert_status = fert[0].meta.status.value if fert else "unavailable"
    parts.append(f"FERTILIZER PRICES: status={fert_status}"
                  + ("" if fert_status == "verified" else " — no live source connected yet"))

    crops = await mandi_service.get_crop_prices(city=city)
    crop_status = crops[0].meta.status.value if crops else "unavailable"
    parts.append(f"MANDI CROP PRICES: status={crop_status}"
                  + ("" if crop_status == "verified" else " — no live source connected yet"))

    return "\n".join(parts)


async def ask_assistant(req: ChatRequest) -> str:
    if not OPENROUTER_API_KEY:
        return (
            "AI assistant is not configured. " 
        )

    context = await _build_context(req.city)
    history_msgs = [
        {"role": "user" if m.role == "user" else "assistant", "content": m.content}
        for m in req.history[-6:]
    ]

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"CONTEXT:\n{context}"},
        *history_msgs,
        {"role": "user", "content": req.message},
    ]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # Optional but recommended by OpenRouter for attribution:
        "HTTP-Referer": "https://smart-kisan.local",
        "X-Title": "Smart Kisan",
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(OPENROUTER_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI assistant se jawab lene mein masla hai: {e}"