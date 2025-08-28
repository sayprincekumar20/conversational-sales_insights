# app/services/llm_service.py
import requests
from app.config import settings

class LLMService:
    def __init__(self):
        self.groq_url = settings.GROQ_API_URL
        self.groq_key = settings.GROQ_API_KEY
        self.langgraph_url = settings.LANGGRAPH_API_URL
        self.langgraph_key = settings.LANGGRAPH_API_KEY

    def _groq_call(self, messages, max_tokens=512, temperature=0):
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": settings.GROQ_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        resp = requests.post(self.groq_url, json=payload, headers=headers, timeout=30)

        # fallback for /responses
        if resp.status_code == 404 and "/chat/completions" in self.groq_url:
            fallback_url = self.groq_url.replace("/chat/completions", "/responses")
            resp = requests.post(fallback_url, json=payload, headers=headers, timeout=30)

        resp.raise_for_status()
        data = resp.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        elif "output_text" in data:
            return data["output_text"].strip()
        else:
            raise RuntimeError(f"Unexpected Groq API response: {data}")

    def prompt_to_sql(self, prompt: str) -> dict:
        if self.langgraph_url:
            headers = {"Content-Type": "application/json"}
            if self.langgraph_key:
                headers["Authorization"] = f"Bearer {self.langgraph_key}"
            resp = requests.post(self.langgraph_url, json={"prompt": prompt}, headers=headers, timeout=30)
            resp.raise_for_status()
            return resp.json()

        sql = self._groq_call(
            [{"role": "system", "content": settings.SYSTEM_SQL},
             {"role": "user", "content": prompt}],
            max_tokens=512, temperature=0
        )
        return {"sql": sql}

    def generate_insight(self, prompt: str, data: list) -> str:
        return self._groq_call(
            [{"role": "system", "content": settings.INSIGHT_SYSTEM},
             {"role": "user", "content": f"Question: {prompt}\n\nData: {data[:10]}"}],
            max_tokens=200,
            temperature=0.2
        )
