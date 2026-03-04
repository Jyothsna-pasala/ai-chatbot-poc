from typing import Optional, List, Dict
from pydantic import BaseModel


class ChatContext(BaseModel):
    module: str
    channel: str


class ChatRequest(BaseModel):
    sessionId: str
    message: str
    userRole: str
    context: ChatContext


class ChatResponse(BaseModel):
    answer: str
    confidence: float
    tier: str
    severity: str
    kbReferences: List[Dict]
    needsEscalation: bool
    ticketId: Optional[str] = None
    guardrail: Dict