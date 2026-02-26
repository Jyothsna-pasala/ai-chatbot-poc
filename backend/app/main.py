from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI(
    title="AI Helpdesk Backend",
    version="1.0.0"
)

app.include_router(chat_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "AI backend is running"}
