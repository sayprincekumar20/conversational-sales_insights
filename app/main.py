from fastapi import FastAPI
from app.routes import chatbot
from app.database import init_db
from app.config import settings
import requests

app = FastAPI(title="Conversational Sales Insights")

app.include_router(chatbot.router)

@app.on_event("startup")
async def startup_event():
    print("✅ Using Groq model:", settings.GROQ_MODEL)
    print("✅ GROQ_API_KEY loaded?", bool(settings.GROQ_API_KEY))

    # Test endpoint
    try:
        headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
        resp = requests.get(settings.GROQ_API_URL.replace("/chat/completions", ""), headers=headers)
        print("Groq endpoint test:", resp.status_code, resp.text[:200])
    except Exception as e:
        print("Groq connectivity failed:", e)

    init_db()




