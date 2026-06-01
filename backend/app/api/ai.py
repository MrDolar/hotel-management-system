from fastapi import APIRouter, Depends
import httpx
from app.core.config import get_settings

router = APIRouter(prefix="/api/ai", tags=["AI"])
settings = get_settings()
def _ok(): return settings.AI_API_KEY and settings.AI_API_KEY != "sk-your-api-key-here"

@router.post("/pricing")
async def smart_pricing(room_type: str, season: str = "normal"):
    if not _ok(): return {"suggestion": "AI not configured"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{settings.AI_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {settings.AI_API_KEY}"},
            json={"model": settings.AI_MODEL, "messages": [
                {"role": "system", "content": "Hotel pricing AI. Suggest optimal price."},
                {"role": "user", "content": f"Room type: {room_type}, Season: {season}"}
            ], "temperature": 0.5}, timeout=30)
        return {"suggestion": resp.json()["choices"][0]["message"]["content"]}

@router.post("/predict")
async def predict_occupancy(days: int = 30):
    if not _ok(): return {"prediction": "AI not configured"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{settings.AI_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {settings.AI_API_KEY}"},
            json={"model": settings.AI_MODEL, "messages": [
                {"role": "system", "content": "Hotel occupancy prediction AI."},
                {"role": "user", "content": f"Predict occupancy for next {days} days."}
            ], "temperature": 0.5}, timeout=30)
        return {"prediction": resp.json()["choices"][0]["message"]["content"]}

@router.post("/chat")
async def chat(message: str):
    if not _ok(): return {"response": "AI not configured"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{settings.AI_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {settings.AI_API_KEY}"},
            json={"model": settings.AI_MODEL, "messages": [
                {"role": "system", "content": "Hotel customer service AI."},
                {"role": "user", "content": message}
            ], "temperature": 0.7}, timeout=30)
        return {"response": resp.json()["choices"][0]["message"]["content"]}
