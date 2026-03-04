from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.tickets import router as ticket_router
from app.api.metrics import router as metrics_router

app = FastAPI(
    title="AI Helpdesk Backend",
    version="1.0.0"
)

#routes
app.include_router(chat_router, prefix="/api")
app.include_router(ticket_router, prefix="/api")
app.include_router(metrics_router, prefix="/api")

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "AI backend is running"
    }