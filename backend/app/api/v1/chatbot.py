from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chat")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    # Placeholder: echo message
    return ChatResponse(reply=f"Echo: {req.message}")
