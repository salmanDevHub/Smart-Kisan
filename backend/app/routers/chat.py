from fastapi import APIRouter
from app.services import ai_service
from app.models import ChatRequest

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("")
async def chat(req: ChatRequest):
    reply = await ai_service.ask_assistant(req)
    return {"reply": reply}
