from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import news, weather, mandi, fertilizer, chat, marketplace, auth
from app.services.auth_service import init_db

app = FastAPI(
    title="Smart Kisan API",
    description="AI-powered digital agriculture assistant for Pakistani farmers.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this for production deployment
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    init_db()


app.include_router(news.router)
app.include_router(weather.router)
app.include_router(mandi.router)
app.include_router(fertilizer.router)
app.include_router(chat.router)
app.include_router(marketplace.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"status": "ok", "service": "Smart Kisan API"}


@app.get("/api/health")
async def health():
    return {"status": "healthy"}