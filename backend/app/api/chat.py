# Simple in-memory store (temporary)
conversation_store = {}

# from fastapi import APIRouter
# from app.models.schemas import ChatRequest, ChatResponse

# router = APIRouter()

# @router.post("/api/chat", response_model=ChatResponse)
# async def chat_endpoint(req: ChatRequest):
#     return ChatResponse(
#         answer="This is a placeholder response from Day 1 backend.",
#         confidence=0.50
#     )


# @router.post("/api/chat", response_model=ChatResponse)
# async def chat_endpoint(req: ChatRequest):

#     # 1) Get previous messages for this session
#     history = conversation_store.get(req.sessionId, [])

#     # 2) Add new user message to history
#     history.append(f"User: {req.message}")

#     # 3) Save back to store
#     conversation_store[req.sessionId] = history

#     # 4) Create a context-aware reply (simple for now)
#     answer = f"I see your message: '{req.message}'. " \
#               f"You previously said: {history[:-1]}"

#     # 5) Add assistant reply to history
#     history.append(f"Assistant: {answer}")

#     return ChatResponse(
#         answer=answer,
#         confidence=0.70
#     )

from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import handle_chat

router = APIRouter()

@router.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):

    answer = handle_chat(
        session_id=req.sessionId,
        user_message=req.message
    )

    return ChatResponse(
        answer=answer,
        confidence=0.75
    )

