from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


class SignupRequest(BaseModel):
    name: str
    phone: str
    password: str
    city: str | None = None


class LoginRequest(BaseModel):
    phone: str
    password: str


@router.post("/signup")
async def signup(req: SignupRequest):
    result = auth_service.signup(req.name, req.phone, req.password, req.city)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/login")
async def login(req: LoginRequest):
    result = auth_service.login(req.phone, req.password)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result


@router.get("/me")
async def me(authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    user = auth_service.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Session expired ya invalid — dobara login karein.")
    return user
