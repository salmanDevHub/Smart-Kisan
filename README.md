# Smart Kisan — AI Agriculture Platform for Pakistani Farmers


## Tech Stack
- **Frontend:** Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **Backend:** Python + FastAPI
- **Database:** SQLite (users/sessions)
- **AI:** Google Gemini API (grounded with live data)
- **Live data sources:** Open-Meteo (weather), RSS feeds (Dawn/Business Recorder/Tribune) for news

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # then add your GEMINI_API_KEY
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Open http://localhost:3000

## Data Honesty
Mandi crop prices and branded fertilizer prices show "No verified data" /
"Contact dealer for price" until a real data source (MANDI_API_URL,
FERTILIZER_API_URL in backend .env) is connected. No numbers are ever
fabricated — see comments in app/services/mandi_service.py and
fertilizer_service.py for how to wire in a real source.
