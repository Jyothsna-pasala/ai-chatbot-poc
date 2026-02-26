# # backend/app/services/chat_service.py
#//learn 1
# conversation_store = {}

# def handle_chat(session_id: str, user_message: str) -> str:
#     """
#     Handles chat logic and maintains memory.
#     """

#     # Get history for this session
#     history = conversation_store.get(session_id, [])

#     # Add user message
#     history.append(f"User: {user_message}")

#     # Save back to store
#     conversation_store[session_id] = history

#     # Build context-aware answer
#     answer = f"I received: '{user_message}'. Previous context: {history[:-1]}"

#     # Store assistant reply
#     history.append(f"Assistant: {answer}")

#     return answer


#//learn 2
# Chat memory store
# conversation_store = {}

# def get_history(session_id: str):

#     if session_id not in conversation_store:
#         conversation_store[session_id] = []

#     return conversation_store[session_id]


# def add_user_message(session_id: str, message: str):

#     history = get_history(session_id)

#     history.append({
#         "role": "user",
#         "message": message
#     })


# def add_assistant_message(session_id: str, message: str):

#     history = get_history(session_id)

#     history.append({
#         "role": "assistant",
#         "message": message
#     })


# def generate_answer(session_id: str, user_message: str):

#     history = get_history(session_id)

#     previous_messages = [msg["message"] for msg in history if msg["role"] == "user"]

#     answer = f"I received your message: '{user_message}'. Previous messages: {previous_messages}"

#     return answer


# def handle_chat(session_id: str, user_message: str):

#     add_user_message(session_id, user_message)

#     answer = generate_answer(session_id, user_message)

#     add_assistant_message(session_id, answer)

#     return answer

#//learn 3
from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import handle_chat


# Create router
router = APIRouter()


# Chat endpoint
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):

    # Call chat service
    result = handle_chat(
        session_id=req.sessionId,
        user_message=req.message
    )

    # Return structured response
    return ChatResponse(
        answer=result["answer"],
        confidence=result["confidence"],
        tier=result["tier"],
        severity=result["severity"],
        kbReferences=result["kbReferences"],
        needsEscalation=result["needsEscalation"],
        guardrail=result["guardrail"]
    )