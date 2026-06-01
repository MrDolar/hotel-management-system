"""AI Service"""
import json
import httpx
from app.core.config import get_settings

settings = get_settings()

class AIService:
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.base_url = settings.AI_BASE_URL
        self.model = settings.AI_MODEL
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = httpx.AsyncClient(base_url=self.base_url, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=30.0)
        return self._client

    def _is_configured(self):
        return bool(self.api_key and self.api_key != "sk-your-api-key-here")

    async def _chat(self, messages, temperature=0.7):
        if not self._is_configured():
            raise ValueError("AI not configured")
        resp = await self.client.post("/chat/completions", json={"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": 1000})
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    async def analyze(self, data, task):
        try:
            resp = await self._chat([{"role": "system", "content": "You are an AI assistant."}, {"role": "user", "content": f"Analyze: {data}\nTask: {task}\nReturn JSON."}])
            return json.loads(resp)
        except Exception as e:
            return {"error": str(e)}

    async def chat(self, message):
        try:
            return await self._chat([{"role": "user", "content": message}])
        except:
            return "AI service unavailable"

ai_service = AIService()
