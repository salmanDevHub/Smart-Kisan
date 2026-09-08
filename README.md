# Smart Kisan — AI Agriculture Platform for Pakistani Farmers

An AI-powered digital agriculture platform that brings mandi crop prices, weather
forecasts, a fertilizer marketplace, agriculture news, and an AI chat assistant
together in one dashboard for Pakistani farmers.

## Tech Stack

- **Frontend:** Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **Backend:** Python + FastAPI
- **Database:** SQLite (users/sessions)
- **AI:** OpenRouter (OpenAI-compatible API), grounded with live data — never
  invents prices or forecasts
- **Live data sources:** Open-Meteo (weather), RSS feeds (Dawn/Business
  Recorder/Tribune) for news

## Features

- **Dashboard** — daily market, weather & AI advisory summary at a glance
- **Market Prices** — mandi crop price intelligence (per-city, per-commodity)
- **Fertilizer Marketplace** — Daraz/OLX-style catalog of real Pakistani
  fertilizer companies (FFC, Engro, Fatima Fertilizer, Pak Arab, Sitara,
  and more) and their actual product lines, organized by category
  (Nitrogenous, Phosphatic, Potassic, NPK Blend, Micronutrient & Bio)
- **Weather** — localized forecast via Open-Meteo
- **AI Assistant** — chat in Roman Urdu, Urdu, or English; answers are
  grounded in live data status, so it says "unavailable" instead of guessing
- **News & Alerts** — curated agriculture news feed
- **Accounts** — signup/login for personalized access

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # then add your OPENROUTER_API_KEY
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```


## Data Honesty

Mandi crop prices and branded fertilizer prices show "unavailable" until a
real live data source (`MANDI_API_URL`, `FERTILIZER_API_URL` in backend
`.env`) is connected — no numbers are ever fabricated. The Fertilizer
Marketplace lists real companies and real product names so farmers can still
browse and find a dealer, even before a live pricing feed is wired in. See
comments in `app/services/mandi_service.py` and `app/services/
fertilizer_service.py` for how to connect a real source.
