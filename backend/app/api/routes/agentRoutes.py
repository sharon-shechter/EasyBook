from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.agent.chat_agent import chatbot_conversation
from app.utilities.token import get_current_user

router = APIRouter()

@router.post("/chat")
def chat_with_agent(
    request_data: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    content = request_data.get("content")
    user_id = int(current_user.get("sub"))
    response = chatbot_conversation(db, user_id, content)
    return response
