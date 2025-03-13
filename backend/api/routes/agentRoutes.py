from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database.database import get_db
from backend.agent.chat_agent import chatbot_conversation

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: Optional[int] = None
    content: str

@router.post("/chat")
def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
    response = chatbot_conversation(db, request.user_id, request.content)
    return response
