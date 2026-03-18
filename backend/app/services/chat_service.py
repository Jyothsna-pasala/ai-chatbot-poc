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
# from fastapi import APIRouter

# from app.models.schemas import ChatRequest, ChatResponse
# from app.services.chat_service import handle_chat


# # Create router
# router = APIRouter()


# # Chat endpoint
# @router.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(req: ChatRequest):

#     # Call chat service
#     result = handle_chat(
#         session_id=req.sessionId,
#         user_message=req.message
#     )

#     # Return structured response
#     return ChatResponse(
#         answer=result["answer"],
#         confidence=result["confidence"],
#         tier=result["tier"],
#         severity=result["severity"],
#         kbReferences=result["kbReferences"],
#         needsEscalation=result["needsEscalation"],
#         guardrail=result["guardrail"]
#     )



#//learn 4

# from app.services.vector_service import VectorService
# from app.services.guardrail_service import GuardrailService


# vector_service = VectorService()
# guardrail_service = GuardrailService()


# def handle_chat(session_id: str, user_message: str):

#     # Step 1 — Guardrail check
#     guardrail_result = guardrail_service.check(user_message)

#     if guardrail_result["blocked"]:

#         return {
#             "answer": "This request is restricted and cannot be answered.",
#             "confidence": 1.0,
#             "tier": "TIER_3",
#             "severity": "HIGH",
#             "kbReferences": [],
#             "needsEscalation": True,
#             "guardrail": guardrail_result
#         }


#     # Step 2 — KB search (RAG)
#     kb_result = vector_service.search(user_message)

#     return {
#         "answer": kb_result["answer"],
#         "confidence": 0.95,
#         "tier": kb_result["tier"],
#         "severity": kb_result["severity"],
#         "kbReferences": [
#             {
#                 "id": kb_result["id"],
#                 "title": kb_result["question"]
#             }
#         ],
#         "needsEscalation": False,
#         "guardrail": guardrail_result
#     }


#learn 5

# from app.services.vector_service import VectorService
# from app.services.guardrail_service import GuardrailService
# from app.services.ticket_service import TicketService


# vector_service = VectorService()
# guardrail_service = GuardrailService()
# ticket_service = TicketService()

#learn 6
# from app.services.service import (
#     ticket_service,
#     vector_service,
#     guardrail_service,
#     metrics_service,
#     memory_service
# )


# def handle_chat(session_id: str, user_message: str):

#     # 1️⃣ Record every conversation
#     metrics_service.record_chat()

#     # 2️⃣ Guardrail check
#     guardrail_result = guardrail_service.check(user_message)

#     if guardrail_result["blocked"]:

#         # Record metrics
#         metrics_service.record_guardrail()
#         metrics_service.record_escalation()
#         metrics_service.record_ticket("HIGH")

#         # Create ticket
#         ticket = ticket_service.create_ticket(
#             session_id=session_id,
#             issue=user_message,
#             severity="HIGH",
#             tier="TIER_3"
#         )

#         return {
#             "answer": "This request is restricted and has been escalated.",
#             "confidence": 1.0,
#             "tier": "TIER_3",
#             "severity": "HIGH",
#             "kbReferences": [],
#             "needsEscalation": True,
#             "ticketId": ticket["ticketId"],
#             "guardrail": guardrail_result
#         }

#     # 3️⃣ Vector Search (RAG)
#     kb_result = vector_service.search(user_message)

#     # 4️⃣ Escalate if severity HIGH
#     if kb_result["severity"] == "HIGH":

#         metrics_service.record_escalation()
#         metrics_service.record_ticket(kb_result["severity"])

#         ticket = ticket_service.create_ticket(
#             session_id=session_id,
#             issue=user_message,
#             severity=kb_result["severity"],
#             tier=kb_result["tier"]
#         )

#         return {
#             "answer": kb_result["answer"],
#             "confidence": 0.95,
#             "tier": kb_result["tier"],
#             "severity": kb_result["severity"],
#             "kbReferences": [
#                 {
#                     "id": kb_result["id"],
#                     "title": kb_result["question"]
#                 }
#             ],
#             "needsEscalation": True,
#             "ticketId": ticket["ticketId"],
#             "guardrail": guardrail_result
#         }

#     # 5️⃣ Normal response (no escalation)
#     return {
#         "answer": kb_result["answer"],
#         "confidence": 0.95,
#         "tier": kb_result["tier"],
#         "severity": kb_result["severity"],
#         "kbReferences": [
#             {
#                 "id": kb_result["id"],
#                 "title": kb_result["question"]
#             }
#         ],
#         "needsEscalation": False,
#         "ticketId": None,
#         "guardrail": guardrail_result
#     }

#learn 7
# from app.services.service import (
#     ticket_service,
#     vector_service,
#     guardrail_service,
#     metrics_service,
#     memory_service
# )


# def handle_chat(session_id: str, user_message: str):

#     # 1️⃣ Record conversation metric
#     metrics_service.record_chat()

#     # 2️⃣ Store message in session memory
#     memory_service.add_message(session_id, user_message)

#     # 3️⃣ Retrieve conversation history
#     history = memory_service.get_history(session_id)

#     # 4️⃣ Combine history into a single query
#     combined_query = " ".join(history)

#     # 5️⃣ Run guardrail check
#     guardrail_result = guardrail_service.check(user_message)

#     # 🚨 If request is blocked
#     if guardrail_result["blocked"]:

#         metrics_service.record_guardrail()
#         metrics_service.record_escalation()
#         metrics_service.record_ticket("HIGH")

#         ticket = ticket_service.create_ticket(
#             session_id=session_id,
#             issue=user_message,
#             severity="HIGH",
#             tier="TIER_3"
#         )

#         return {
#             "answer": "This request is restricted and has been escalated.",
#             "confidence": 1.0,
#             "tier": "TIER_3",
#             "severity": "HIGH",
#             "kbReferences": [],
#             "needsEscalation": True,
#             "ticketId": ticket["ticketId"],
#             "guardrail": guardrail_result
#         }

#     # 6️⃣ Run RAG search using conversation context
#     kb_result = vector_service.search(combined_query)

#     # 7️⃣ Escalation for high severity issues
#     if kb_result["severity"] == "HIGH":

#         metrics_service.record_escalation()
#         metrics_service.record_ticket(kb_result["severity"])

#         ticket = ticket_service.create_ticket(
#             session_id=session_id,
#             issue=user_message,
#             severity=kb_result["severity"],
#             tier=kb_result["tier"]
#         )

#         return {
#             "answer": kb_result["answer"],
#             "confidence": kb_result["confidence"],
#             "tier": kb_result["tier"],
#             "severity": kb_result["severity"],
#             "kbReferences": [
#                 {
#                     "id": kb_result["id"],
#                     "title": kb_result["question"]
#                 }
#             ],
#             "needsEscalation": True,
#             "ticketId": ticket["ticketId"],
#             "guardrail": guardrail_result
#         }

#     # 8️⃣ Normal response (no escalation)
#     return {
#         "answer": kb_result["answer"],
#         "confidence": kb_result["confidence"],
#         "tier": kb_result["tier"],
#         "severity": kb_result["severity"],
#         "kbReferences": [
#             {
#                 "id": kb_result["id"],
#                 "title": kb_result["question"]
#             }
#         ],
#         "needsEscalation": False,
#         "ticketId": None,
#         "guardrail": guardrail_result
#     }

#learn 8
# from app.services.service import (
#     ticket_service,
#     vector_service,
#     guardrail_service,
#     metrics_service,
# )


# # Conversation memory
# session_memory = {}


# def handle_chat(session_id: str, user_message: str):

#     # Record conversation metric
#     metrics_service.record_chat()

#     # Get previous conversation history
#     history = session_memory.get(session_id, [])

#     # Combine history with new message
#     combined_query = " ".join(history + [user_message])

#     # Save message in memory
#     history.append(user_message)
#     session_memory[session_id] = history[-5:]

#     # Guardrail check
#     guardrail_result = guardrail_service.check(user_message)

#     if guardrail_result["blocked"]:

#         metrics_service.record_guardrail()
#         metrics_service.record_escalation()
#         metrics_service.record_ticket("HIGH")

#         ticket = ticket_service.create_ticket(
#             session_id=session_id,
#             issue=user_message,
#             severity="HIGH",
#             tier="TIER_3"
#         )

#         return {
#             "answer": "This request is restricted and has been escalated.",
#             "confidence": 1.0,
#             "tier": "TIER_3",
#             "severity": "HIGH",
#             "kbReferences": [],
#             "needsEscalation": True,
#             "ticketId": ticket["ticketId"],
#             "guardrail": guardrail_result
#         }

#     # RAG search (Top-K retrieval)
#     kb_results = vector_service.search(combined_query)

#     # Best result
#     kb_result = kb_results[0]

#     # Escalation logic
#     needs_escalation = kb_result["severity"] == "HIGH"

#     ticket_id = None

#     if needs_escalation:

#         metrics_service.record_escalation()
#         metrics_service.record_ticket(kb_result["severity"])

#         ticket = ticket_service.create_ticket(
#             session_id=session_id,
#             issue=user_message,
#             severity=kb_result["severity"],
#             tier=kb_result["tier"]
#         )

#         ticket_id = ticket["ticketId"]

#     return {
#         "answer": kb_result["answer"],
#         "confidence": kb_result["confidence"],
#         "tier": kb_result["tier"],
#         "severity": kb_result["severity"],
#         "kbReferences": [
#             {
#                 "id": item["id"],
#                 "title": item["question"]
#             } for item in kb_results
#         ],
#         "needsEscalation": needs_escalation,
#         "ticketId": ticket_id,
#         "guardrail": guardrail_result
#     }

#learn 9

from app.services.service import (
    ticket_service,
    vector_service,
    guardrail_service,
    metrics_service,
    classification_service
)

# In-memory session storage
session_memory = {}


def handle_chat(session_id: str, user_message: str):

    # 1️⃣ Record conversation
    metrics_service.record_chat()

    # 2️⃣ Get session history
    history = session_memory.get(session_id, [])

    # 3️⃣ Combine history with current message
    combined_query = " ".join(history + [user_message])

    # 4️⃣ Store last 5 messages
    history.append(user_message)
    session_memory[session_id] = history[-5:]

    # 5️⃣ Guardrail check
    guardrail_result = guardrail_service.check(user_message)

    if guardrail_result["blocked"]:

        metrics_service.record_guardrail()
        metrics_service.record_escalation()
        metrics_service.record_ticket("HIGH")

        ticket = ticket_service.create_ticket(
            session_id=session_id,
            issue=user_message,
            severity="HIGH",
            tier="TIER_3"
        )

        return {
            "answer": "This request is restricted and has been escalated.",
            "confidence": 1.0,
            "tier": "TIER_3",
            "severity": "HIGH",
            "kbReferences": [],
            "needsEscalation": True,
            "ticketId": ticket["ticketId"],
            "guardrail": guardrail_result
        }

    # 6️⃣ Deterministic classification (Day 14)
    classification = classification_service.classify(user_message)
    tier = classification["tier"]
    severity = classification["severity"]

    # 7️⃣ RAG search (Top-K)
    kb_results = vector_service.search(combined_query)

    # 8️⃣ Pick best result
    kb_result = kb_results[0]

    # 9️⃣ Escalation logic
    needs_escalation = severity in ["HIGH", "CRITICAL"]

    ticket_id = None

    if needs_escalation:

        metrics_service.record_escalation()
        metrics_service.record_ticket(severity)

        ticket = ticket_service.create_ticket(
            session_id=session_id,
            issue=user_message,
            severity=severity,
            tier=tier
        )

        ticket_id = ticket["ticketId"]

    # 🔟 Final response
    return {
        "answer": kb_result["answer"],
        "confidence": kb_result["confidence"],
        "tier": tier,
        "severity": severity,
        "kbReferences": [
            {
                "id": item["id"],
                "title": item["question"]
            } for item in kb_results
        ],
        "needsEscalation": needs_escalation,
        "ticketId": ticket_id,
        "guardrail": guardrail_result
    }