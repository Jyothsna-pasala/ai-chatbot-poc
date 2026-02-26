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
